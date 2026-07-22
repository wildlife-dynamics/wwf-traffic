# WWF Traffic Workflow

This guide walks you through loading, configuring, and running the WWF Traffic Workflow, which processes user-uploaded wildlife trafficking incident reports, filters them to incidents within a 30km buffer of the Greater Virunga Landscape (GVL) boundary, and produces an interactive dashboard of trafficking trends by species, incident category, and country.

---

## What it produces

The workflow delivers, for each run:

- **Summary stat widgets** — Total Incidents, Incidents This Year vs Last Year, Most Trafficked Species, Total Suspects Arrested, Total Suspects Convicted, Conviction Rate, and Total Seizures of Ivory (kg)
- An **Incidents Map** — point map of trafficking incidents coloured by incident category, overlaid on the GVL boundary
- A **Species Map** — point map of trafficking incidents coloured by mapped species group, overlaid on the GVL boundary
- An **Incidents by Species chart** — time-series bar chart of incident counts per year, broken down by species
- An **Incidents by Category chart** — time-series bar chart of incident counts per year, broken down by incident category
- A **Summary Table** — filterable/sortable table of individual incidents (date, category, role, species)
- A **per-group CSV export** of the full processed incident dataset

All widgets are grouped by whichever grouping strategy you configure (Species or Country of Incident, or one combined view if left blank) and assembled into a single dashboard.

---

## Requirements

- **Three CSV exports from the TRAFFIC dataset**, uploaded together, all sharing a common `Report ID` column used to merge them. This workflow reads columns spread across multiple files — no single export contains everything it needs:
  - An **incident/case file** — `Report ID`, `Category of Incident`, `Country of Incident`, `Date of Incident`, `Outcome`, `Number of People Arrested`, `Number of People Charged`, `Number of People Fined`, `Number of People Imprisoned`
  - A **species/commodity file** — `Report ID`, `Full Scientific Name`, `Item / Commodity Type`, `Count`, `Weight`, `Unit of Weight`, `Kingdom`, `Phylum`, `Class`, `Order`, `Family`, `Common Name`
  - A **trade-route/location file** — `Report ID`, `Role`, `Order in Trade Route`, `Country`, `Latitude`, `Longitude`

  > `Category of Incident`, `Country of Incident`, and `Date of Incident` appear in more than one of the three files. After merging, only the version from the first-loaded file is kept (internally suffixed `_x`) — make sure that file's values are the ones you want retained for those three columns.

> The GVL 30km buffer boundary is downloaded automatically from Dropbox at runtime — no local copy is required.

---

## 1. Load the Workflow

In the workflow runner, go to **Workflow Templates** and click **Add Workflow Template**. Paste this repository's URL into the **Github Link** field, then click **Add Template**:

```
https://github.com/wildlife-dynamics/wwf-traffic.git
```

Once added, it appears in the **Workflow Templates** list as **wwf-traffic**. Click it to open the workflow configuration form.

---

## 2. Configure the Workflow

### Workflow Details and Time Range

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run (required) |
| Workflow Description | Optional notes to differentiate this run from others |

**Time range**

| Field | Description |
|-------|-------------|
| Timezone | Select the local timezone (e.g. `Africa/Nairobi UTC+03:00`) |
| Since | Start date and time — incidents from this point are included |
| Until | End date and time of the analysis window |

### Grouping Strategy

Choose how the dashboard should be split into separate views:

| Option | Description |
|--------|-------------|
| Species | One dashboard view per mapped species group (e.g. Elephant, Hippo, Gorilla) |
| Country | One dashboard view per country of incident |
| *(left blank)* | All data appears in a single combined view (default) |

Only these two grouping fields are available — the underlying grouper type also supports temporal and spatial grouping, but both are disabled for this workflow.

### Basemap Layers

Two stacked ArcGIS tile layers form the background of both maps. Pre-filled with sensible defaults, but the URL, opacity, and max zoom of each layer are editable.

| Layer | Default Opacity | Max Zoom |
|-------|------------------|----------|
| ESRI World Topographic Map | `1.0` | `20` |
| ESRI World Imagery | `0.5` | `20` |

### Load Traffic CSV Files

Upload the CSV file(s) containing your trafficking incident reports — see [Requirements](#requirements) for the three files needed. All files are merged on the `Report ID` column, so every file must include it.

### Select Color Palette

Choose a colour palette used to colour incidents by category and by species on the maps and charts. Pick a named Matplotlib colormap (defaults to `tab10`) or define a custom list of hex colours.

---

## 3. Run the Workflow

Once submitted, the runner will:

1. Merge the uploaded CSV files on `Report ID`, then retain and rename the relevant columns to a standard schema.
2. For records with more than one trade-route location (Origin/Transit/Destination), retain a single representative row per report, species, and commodity.
3. Convert numeric fields (count, weight, arrest/charge/fine/imprisonment counts, latitude, longitude) from text to numeric values, then convert the records to a point GeoDataFrame.
4. Download the GVL 30km buffer boundary from Dropbox and reproject it to `EPSG:4326`.
5. Spatially join incidents against the GVL boundary (keeping only incidents that fall within it), then additionally restrict to incidents where `Country of Incident` is Rwanda, Uganda, or Congo, Democratic Republic of The.
6. Map scientific names to simplified species groups (e.g. Elephantidae/Loxodonta → Elephant, Manidae → Pangolin) and map raw incident categories to short labels (Seizure, Poaching, Smuggling, Human-Wildlife Conflict, Enforcement).
7. Add a temporal index and decompose the incident date into year and month; split the dataset into groups per the configured grouping strategy.
8. Aggregate incidents per year (overall, by species), sum arrests and imprisonments per year, and compute an overall conviction rate (total imprisoned / total arrested, as a percent).
9. Filter to ivory-related commodities (Ivory Pieces - Raw, Ivory - Worked, Tusk) and sum seizure weight per year.
10. Render the incidents-by-species and incidents-by-category time-series bar charts.
11. Build the GVL boundary layer plus incident and species scatterplot layers, compute a map zoom/extent from the data, and render the Incidents Map and Species Map.
12. Render the filterable summary table (date, category, role, species) and persist the full processed dataset as CSV.
13. Assemble all summary stat widgets, maps, charts, and the table into the final dashboard, merging per-group views where applicable.
14. Save all outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

### Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`:

| File / suffix | Description |
|--------|-------------|
| `..._incidents_by_species.html` | Time-series bar chart of incidents per year, by species |
| `..._incidents_by_category.html` | Time-series bar chart of incidents per year, by incident category |
| `..._incidents_by_species.html` | Interactive **Species Map** coloured by species group |
| `..._incidents_by_category.html` | Interactive **Incidents Map** coloured by incident category |
| `..._summary_table_of_incidents.html` | Filterable/sortable summary table of individual incidents |
| `<group>.csv` | Full processed incident dataset for that group (all mapped/renamed columns) |

> The two charts and the two maps are persisted in pairs that share the exact same filename suffix (`incidents_by_species` and `incidents_by_category`, respectively) — this is a naming quirk in the current workflow, not a collision on disk, since each file is additionally prefixed with a content hash. Distinguish them by opening the file or by widget title on the dashboard rather than by suffix alone.

One set of files is produced per grouped view (e.g. per species or per country) if a grouping strategy is configured. The final dashboard bundles all of the above, along with the summary stat widgets (Total Incidents, Incidents YoY, Most Trafficked Species, Total Arrested, Total Convicted, Conviction Rate, Total Ivory Seized), into a single interactive view.

> A per-year conviction rate (`add_conviction_rate`) is also computed internally but its result is never persisted or wired into the dashboard — the **Conviction Rate** widget is instead computed separately as a single all-time ratio (total imprisoned ÷ total arrested).
