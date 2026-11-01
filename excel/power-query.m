// Excel / Power BI: Data > Get Data > From Other Sources > Blank Query > Advanced Editor.
// Paste this, change Base, then Close & Load. Refresh any time for the latest rates.
let
    Base = "USD",
    Source = Json.Document(Web.Contents("https://allratestoday.com/api/open/latest/" & Base)),
    Rates = Record.ToTable(Source[rates]),
    Renamed = Table.RenameColumns(Rates, {{"Name", "Currency"}, {"Value", "Rate"}}),
    Typed = Table.TransformColumnTypes(Renamed, {{"Rate", type number}}),
    WithDate = Table.AddColumn(Typed, "Date", each Source[date], type text)
in
    WithDate
