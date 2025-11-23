Imports System.Threading.Tasks
Imports System.Windows

Class MainWindow

    Private _api As ApiClient

    Private Sub Window_Loaded(sender As Object, e As RoutedEventArgs)
        Dim baseUrl As String = "http://localhost:8000"
        _api = New ApiClient(baseUrl)
    End Sub

    Private Async Sub btnLoadTestbeds_Click(sender As Object, e As RoutedEventArgs)
        Await LoadTestbedsAsync()
    End Sub

    Private Async Sub btnCreateTestbed_Click(sender As Object, e As RoutedEventArgs)
        Await CreateTestbedAsync()
    End Sub

    Private Async Function LoadTestbedsAsync() As Task
        Try
            lstTestbeds.Items.Clear()

            Dim testbeds = Await _api.GetTestbedsAsync()

            If testbeds Is Nothing OrElse testbeds.Count = 0 Then
                lstTestbeds.Items.Add("(No testbeds found)")
            Else
                For Each tb In testbeds
                    Dim display = $"[{tb.Id}] {tb.Name} ({tb.Location})"
                    lstTestbeds.Items.Add(display)
                Next
            End If
        Catch ex As Exception
            MessageBox.Show(
                $"Error loading testbeds:{Environment.NewLine}{ex.Message}",
                "Error",
                MessageBoxButton.OK,
                MessageBoxImage.[Error]
            )
        End Try
    End Function

    Private Async Function CreateTestbedAsync() As Task
        Dim name = txtName.Text.Trim()
        Dim location = txtLocation.Text.Trim()
        Dim description = txtDescription.Text.Trim()

        If String.IsNullOrWhiteSpace(name) Then
            MessageBox.Show(
                "Name is required.",
                "Validation",
                MessageBoxButton.OK,
                MessageBoxImage.Warning
            )
            Exit Function
        End If

        Dim newTb As New TestbedCreate With {
            .Name = name,
            .Location = location,
            .Description = description
        }

        Try
            Dim created = Await _api.CreateTestbedAsync(newTb)

            MessageBox.Show(
                $"Created testbed ID {created.Id}: {created.Name}",
                "Success",
                MessageBoxButton.OK,
                MessageBoxImage.Information
            )

            Await LoadTestbedsAsync()

            txtName.Clear()
            txtLocation.Clear()
            txtDescription.Clear()
        Catch ex As Exception
            MessageBox.Show(
                $"Error creating testbed:{Environment.NewLine}{ex.Message}",
                "Error",
                MessageBoxButton.OK,
                MessageBoxImage.[Error]
            )
        End Try
    End Function

    Private Async Sub lstTestbeds_MouseDoubleClick(sender As Object, e As System.Windows.Input.MouseButtonEventArgs)
        Dim selected = TryCast(lstTestbeds.SelectedItem, String)
        If String.IsNullOrEmpty(selected) Then
            Return
        End If

        Dim idStart = selected.IndexOf("["c)
        Dim idEnd = selected.IndexOf("]"c)

        If idStart = -1 OrElse idEnd = -1 OrElse idEnd <= idStart + 1 Then
            MessageBox.Show("Could not parse Testbed ID from selection.",
                            "Parse Error",
                            MessageBoxButton.OK,
                            MessageBoxImage.Warning)
            Return
        End If

        Dim idSubstring = selected.Substring(idStart + 1, idEnd - idStart - 1)
        Dim testbedId As Integer
        If Not Integer.TryParse(idSubstring, testbedId) Then
            MessageBox.Show("Selected Testbed ID is not a valid integer.",
                            "Parse Error",
                            MessageBoxButton.OK,
                            MessageBoxImage.Warning)
            Return
        End If

        Try
            Dim configs = Await _api.GetConfigsForTestbedAsync(testbedId)

            If configs Is Nothing OrElse configs.Count = 0 Then
                MessageBox.Show("No configs found for this testbed.",
                                "Configs",
                                MessageBoxButton.OK,
                                MessageBoxImage.Information)
                Return
            End If

            Dim sb As New System.Text.StringBuilder()
            sb.AppendLine($"Testbed {testbedId} configurations:")
            sb.AppendLine()

            For Each cfg In configs
                sb.AppendLine($"Config {cfg.Id}: {cfg.Name}")
                If Not String.IsNullOrWhiteSpace(cfg.SoftwareVersion) Then
                    sb.AppendLine($"  Version: {cfg.SoftwareVersion}")
                End If
                If Not String.IsNullOrWhiteSpace(cfg.OS) Then
                    sb.AppendLine($"  OS: {cfg.OS}")
                End If
                If cfg.IsCurrentConfig Then
                    sb.AppendLine("  (Current Config)")
                End If

                Dim runs = Await _api.GetRunsForConfigAsync(cfg.Id)
                If runs Is Nothing OrElse runs.Count = 0 Then
                    sb.AppendLine("  Runs: (none)")
                Else
                    sb.AppendLine("  Runs:")
                    For Each run In runs
                        Dim op = If(String.IsNullOrWhiteSpace(run.[Operator]), "(no operator)", run.[Operator])
                        sb.AppendLine($"    - Run {run.Id}: {run.Result} by {op}")
                    Next
                End If

                sb.AppendLine()
            Next

            MessageBox.Show(sb.ToString(),
                            "Configs & Runs",
                            MessageBoxButton.OK,
                            MessageBoxImage.Information)

        Catch ex As Exception
            MessageBox.Show(
                $"Error fetching configs/runs:{Environment.NewLine}{ex.Message}",
                "Error",
                MessageBoxButton.OK,
                MessageBoxImage.[Error]
            )
        End Try
    End Sub
    Private Async Sub btnCreateConfig_Click(sender As Object, e As RoutedEventArgs)
        ' We need a selected testbed to know which testbed_id to use
        Dim selected = TryCast(lstTestbeds.SelectedItem, String)
        If String.IsNullOrEmpty(selected) Then
            MessageBox.Show("Select a testbed first before creating a config.",
                            "Validation",
                            MessageBoxButton.OK,
                            MessageBoxImage.Warning)
            Exit Sub
        End If

        ' Parse the testbed ID from "[id] Name (Location)"
        Dim idStart = selected.IndexOf("["c)
        Dim idEnd = selected.IndexOf("]"c)
        If idStart = -1 OrElse idEnd = -1 OrElse idEnd <= idStart + 1 Then
            MessageBox.Show("Could not parse Testbed ID from selection.",
                            "Parse Error",
                            MessageBoxButton.OK,
                            MessageBoxImage.Warning)
            Exit Sub
        End If

        Dim idSubstring = selected.Substring(idStart + 1, idEnd - idStart - 1)
        Dim testbedId As Integer
        If Not Integer.TryParse(idSubstring, testbedId) Then
            MessageBox.Show("Selected Testbed ID is not a valid integer.",
                            "Parse Error",
                            MessageBoxButton.OK,
                            MessageBoxImage.Warning)
            Exit Sub
        End If

        Dim name = txtConfigName.Text.Trim()
        Dim version = txtConfigSoftwareVersion.Text.Trim()
        Dim os = txtConfigOS.Text.Trim()
        Dim notes = txtConfigNotes.Text.Trim()
        Dim isCurrent = chkConfigIsCurrent.IsChecked.GetValueOrDefault(False)

        If String.IsNullOrWhiteSpace(name) Then
            MessageBox.Show("Config name is required.",
                            "Validation",
                            MessageBoxButton.OK,
                            MessageBoxImage.Warning)
            Exit Sub
        End If

        Dim cfg As New SimulationConfigCreate With {
            .TestbedId = testbedId,
            .Name = name,
            .SoftwareVersion = version,
            .OS = os,
            .Notes = notes,
            .IsCurrentConfig = isCurrent
        }

        Try
            Dim created = Await _api.CreateSimulationConfigAsync(cfg)

            MessageBox.Show(
                $"Created config ID {created.Id} for Testbed {created.TestbedId}:{Environment.NewLine}{created.Name}",
                "Config Created",
                MessageBoxButton.OK,
                MessageBoxImage.Information
            )

            ' Optionally clear inputs
            txtConfigName.Clear()
            txtConfigSoftwareVersion.Clear()
            txtConfigOS.Clear()
            txtConfigNotes.Clear()
            chkConfigIsCurrent.IsChecked = False

        Catch ex As Exception
            MessageBox.Show(
                $"Error creating config:{Environment.NewLine}{ex.Message}",
                "Error",
                MessageBoxButton.OK,
                MessageBoxImage.[Error]
            )
        End Try
    End Sub
    Private Async Sub btnCreateRun_Click(sender As Object, e As RoutedEventArgs)
        Dim configIdText = txtRunConfigId.Text.Trim()
        Dim configId As Integer
        If Not Integer.TryParse(configIdText, configId) Then
            MessageBox.Show("Config ID must be a valid integer.",
                            "Validation",
                            MessageBoxButton.OK,
                            MessageBoxImage.Warning)
            Exit Sub
        End If

        Dim result = txtRunResult.Text.Trim()
        Dim op = txtRunOperator.Text.Trim()
        Dim notes = txtRunNotes.Text.Trim()

        If String.IsNullOrWhiteSpace(result) Then
            MessageBox.Show("Result is required (e.g. PASS, FAIL, IN_PROGRESS).",
                            "Validation",
                            MessageBoxButton.OK,
                            MessageBoxImage.Warning)
            Exit Sub
        End If

        Dim run As New TestRunCreate With {
            .SimulationConfigId = configId,
            .Result = result,
            .[Operator] = op,
            .Notes = notes
        }

        Try
            Dim created = Await _api.CreateTestRunAsync(run)

            MessageBox.Show(
                $"Created run ID {created.Id} for Config {created.SimulationConfigId}:{Environment.NewLine}Result: {created.Result}",
                "Run Created",
                MessageBoxButton.OK,
                MessageBoxImage.Information
            )

            ' Optionally clear fields
            txtRunConfigId.Clear()
            txtRunResult.Clear()
            txtRunOperator.Clear()
            txtRunNotes.Clear()

        Catch ex As Exception
            MessageBox.Show(
                $"Error creating run:{Environment.NewLine}{ex.Message}",
                "Error",
                MessageBoxButton.OK,
                MessageBoxImage.[Error]
            )
        End Try
    End Sub

End Class
