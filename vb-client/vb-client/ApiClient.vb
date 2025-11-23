Imports System.Net.Http
Imports System.Text
Imports System.Text.Json
Imports System.Threading.Tasks

Public Class ApiClient
    Private ReadOnly _httpClient As HttpClient
    Private ReadOnly _baseUrl As String

    Public Sub New(baseUrl As String)
        _httpClient = New HttpClient()
        _baseUrl = baseUrl.TrimEnd("/"c)
    End Sub


    ' GET /testbeds -> List(Of TestbedRead)
    Public Async Function GetTestbedsAsync() As Task(Of List(Of TestbedRead))
        Dim url As String = $"{_baseUrl}/testbeds"

        Dim response As HttpResponseMessage = Await _httpClient.GetAsync(url)
        response.EnsureSuccessStatusCode()

        Dim json As String = Await response.Content.ReadAsStringAsync()

        Dim options As New JsonSerializerOptions With {
            .PropertyNameCaseInsensitive = True
        }

        Dim testbeds = JsonSerializer.Deserialize(Of List(Of TestbedRead))(json, options)
        If testbeds Is Nothing Then
            Return New List(Of TestbedRead)()
        End If

        Return testbeds
    End Function


    ' POST /testbeds -> TestbedRead
    Public Async Function CreateTestbedAsync(newTestbed As TestbedCreate) As Task(Of TestbedRead)
        Dim url As String = $"{_baseUrl}/testbeds"

        Dim options As New JsonSerializerOptions With {
            .PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        }

        Dim body As String = JsonSerializer.Serialize(newTestbed, options)
        Dim content As New StringContent(body, Encoding.UTF8, "application/json")

        Dim response As HttpResponseMessage = Await _httpClient.PostAsync(url, content)
        response.EnsureSuccessStatusCode()

        Dim responseJson As String = Await response.Content.ReadAsStringAsync()

        Dim readOptions As New JsonSerializerOptions With {
            .PropertyNameCaseInsensitive = True
        }

        Dim created = JsonSerializer.Deserialize(Of TestbedRead)(responseJson, readOptions)
        Return created
    End Function


    ' GET /configs?testbed_id=123
    Public Async Function GetConfigsForTestbedAsync(testbedId As Integer) As Task(Of List(Of SimulationConfigRead))
        Dim url As String = $"{_baseUrl}/configs?testbed_id={testbedId}"

        Dim response = Await _httpClient.GetAsync(url)
        response.EnsureSuccessStatusCode()

        Dim json = Await response.Content.ReadAsStringAsync()

        Dim options As New JsonSerializerOptions With {
            .PropertyNameCaseInsensitive = True
        }

        Dim configs = JsonSerializer.Deserialize(Of List(Of SimulationConfigRead))(json, options)
        If configs Is Nothing Then
            Return New List(Of SimulationConfigRead)()
        End If

        Return configs
    End Function


    ' GET /runs?simulation_config_id=456
    Public Async Function GetRunsForConfigAsync(configId As Integer) As Task(Of List(Of TestRunRead))
        Dim url As String = $"{_baseUrl}/runs?simulation_config_id={configId}"

        Dim response = Await _httpClient.GetAsync(url)
        response.EnsureSuccessStatusCode()

        Dim json = Await response.Content.ReadAsStringAsync()

        Dim options As New JsonSerializerOptions With {
            .PropertyNameCaseInsensitive = True
        }

        Dim runs = JsonSerializer.Deserialize(Of List(Of TestRunRead))(json, options)
        If runs Is Nothing Then
            Return New List(Of TestRunRead)()
        End If

        Return runs
    End Function

    ' POST /configs -> SimulationConfigRead
    Public Async Function CreateSimulationConfigAsync(cfg As SimulationConfigCreate) As Task(Of SimulationConfigRead)
        Dim url As String = $"{_baseUrl}/configs"

        Dim options As New JsonSerializerOptions With {
            .PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        }

        Dim body As String = JsonSerializer.Serialize(cfg, options)
        Dim content As New StringContent(body, Encoding.UTF8, "application/json")

        Dim response = Await _httpClient.PostAsync(url, content)
        response.EnsureSuccessStatusCode()

        Dim responseJson = Await response.Content.ReadAsStringAsync()

        Dim readOptions As New JsonSerializerOptions With {
            .PropertyNameCaseInsensitive = True
        }

        Dim created = JsonSerializer.Deserialize(Of SimulationConfigRead)(responseJson, readOptions)
        Return created
    End Function

    ' POST /runs -> TestRunRead
    Public Async Function CreateTestRunAsync(run As TestRunCreate) As Task(Of TestRunRead)
        Dim url As String = $"{_baseUrl}/runs"

        Dim options As New JsonSerializerOptions With {
            .PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        }

        Dim body As String = JsonSerializer.Serialize(run, options)
        Dim content As New StringContent(body, Encoding.UTF8, "application/json")

        Dim response = Await _httpClient.PostAsync(url, content)
        response.EnsureSuccessStatusCode()

        Dim responseJson = Await response.Content.ReadAsStringAsync()

        Dim readOptions As New JsonSerializerOptions With {
            .PropertyNameCaseInsensitive = True
        }

        Dim created = JsonSerializer.Deserialize(Of TestRunRead)(responseJson, readOptions)
        Return created
    End Function
End Class
