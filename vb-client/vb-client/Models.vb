Imports System.Text.Json.Serialization


Public Class TestbedRead
    <JsonPropertyName("id")>
    Public Property Id As Integer

    <JsonPropertyName("name")>
    Public Property Name As String

    <JsonPropertyName("location")>
    Public Property Location As String

    <JsonPropertyName("description")>
    Public Property Description As String
End Class


Public Class TestbedCreate
    <JsonPropertyName("name")>
    Public Property Name As String

    <JsonPropertyName("location")>
    Public Property Location As String

    <JsonPropertyName("description")>
    Public Property Description As String
End Class


Public Class SimulationConfigRead
    <JsonPropertyName("id")>
    Public Property Id As Integer

    <JsonPropertyName("testbed_id")>
    Public Property TestbedId As Integer

    <JsonPropertyName("name")>
    Public Property Name As String

    <JsonPropertyName("software_version")>
    Public Property SoftwareVersion As String

    <JsonPropertyName("os")>
    Public Property OS As String

    <JsonPropertyName("notes")>
    Public Property Notes As String

    <JsonPropertyName("is_current_config")>
    Public Property IsCurrentConfig As Boolean
End Class


Public Class SimulationConfigCreate
    <JsonPropertyName("testbed_id")>
    Public Property TestbedId As Integer

    <JsonPropertyName("name")>
    Public Property Name As String

    <JsonPropertyName("software_version")>
    Public Property SoftwareVersion As String

    <JsonPropertyName("os")>
    Public Property OS As String

    <JsonPropertyName("notes")>
    Public Property Notes As String

    <JsonPropertyName("is_current_config")>
    Public Property IsCurrentConfig As Boolean
End Class


Public Class TestRunRead
    <JsonPropertyName("id")>
    Public Property Id As Integer

    <JsonPropertyName("simulation_config_id")>
    Public Property SimulationConfigId As Integer

    <JsonPropertyName("result")>
    Public Property Result As String    ' e.g. "PASS", "FAIL", "IN_PROGRESS"

    <JsonPropertyName("operator")>
    Public Property [Operator] As String

    <JsonPropertyName("notes")>
    Public Property Notes As String
End Class

Public Class TestRunCreate
    <JsonPropertyName("simulation_config_id")>
    Public Property SimulationConfigId As Integer

    <JsonPropertyName("result")>
    Public Property Result As String

    <JsonPropertyName("operator")>
    Public Property [Operator] As String

    <JsonPropertyName("notes")>
    Public Property Notes As String
End Class