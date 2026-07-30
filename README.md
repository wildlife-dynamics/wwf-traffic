# WWF Traffic Workflow

This guide walks you through loading, configuring, and running the WWF Traffic Workflow, which connects directly to the TRAFFIC Wildlife Trade Portal to download wildlife trafficking incident reports for a configured time range, filters them to incidents within a 30km buffer of the Greater Virunga Landscape (GVL) boundary, and produces an interactive dashboard of trafficking trends by species, incident category, and country.

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

All widgets are grouped by whichever grouping strategy you configure (Species or Country, or one combined view if left blank) and assembled into a single dashboard.

---

## Requirements

- **A Wildlife Trade Portal account.** The workflow logs in to [wildlifetradeportal.org](https://www.wildlifetradeportal.org/) on your behalf using the same email and password you use to sign in there, and downloads the incidents recorded within your configured time range. No manual CSV export/upload is required.
- *(Optional)* **An additional local CSV file** of incident records if you want to merge your own data with what's retrieved from the portal (see [Load Extra Data](#load-extra-data)).

> Behind the scenes, the workflow downloads three portal export types — an incident/case export, a species/commodity export, and a trade-route/location export — and merges them on a shared `Report ID` column. This happens automatically; you don't need to configure it unless you want to change which export types are downloaded (see [Download Traffic Portal Incidents](#download-traffic-portal-incidents)).
>
> `Category of Incident`, `Country of Incident`, and `Date of Incident` appear in more than one of the three portal exports. After merging, only the version from the first-downloaded export is kept (internally suffixed `_x`).

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

### Workflow Details

A name and description to help you tell this run apart from others later (for example when comparing different date ranges or filters). These are only used for your own reference and have no effect on the data retrieved.

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run (required) |
| Workflow Description | Optional notes to differentiate this run from others |

### Connect to Traffic Portal

Connect to the TRAFFIC Wildlife Trade Portal. Use the same email and password you used when signing up on [wildlifetradeportal.org](https://www.wildlifetradeportal.org/).

| Field | Description |
|-------|-------------|
| Email | Your Wildlife Trade Portal login email |
| Password | Your Wildlife Trade Portal login password |

> The workflow drives a real browser session against the portal to log in and export data, the same way you would manually — nothing about your account is stored beyond this run.

### Time Range

The time range set here is used to retrieve incidents data from the Wildlife Trade Portal — only incidents recorded within this window will be included in the report.

| Field | Description |
|-------|-------------|
| Timezone | Select the local timezone (e.g. `Africa/Nairobi UTC+03:00`) |
| Since | Start date and time — incidents from this point are included |
| Until | End date and time of the analysis window |

### Grouping Strategy

Choose how incidents should be split into separate maps, charts, and tables:

| Option | Description |
|--------|-------------|
| Species | One dashboard view per mapped species group (e.g. Elephant, Hippo, Gorilla) |
| Country | One dashboard view per country of incident |
| *(left blank)* | All data appears in a single combined view (default) |

Only these two grouping fields are available — the underlying grouper type also supports temporal and spatial grouping, but both are disabled for this workflow.

### Basemap Layers

The background map tile layers used when rendering the incident and species maps in this report. The defaults provide topographic and satellite imagery; only change these if you need a different base map source.

| Layer | Default Opacity | Max Zoom |
|-------|------------------|----------|
| ESRI World Topographic Map | `1.0` | `20` |
| ESRI World Imagery | `0.5` | `20` |

### Download Traffic Portal Incidents

Controls which incident export files are downloaded from the Wildlife Trade Portal and the justification text required by the portal's own export form. These are advanced fields — the defaults work for a standard run:

| Field | Description |
|-------|-------------|
| Export Types | Which portal export files to download. Defaults to all three: **Incident Data Only**, **Incident Summary + Species**, **Incident Summary + Locations** — all three are needed for the merge described in [Requirements](#requirements), so leave this at the default unless you have a specific reason to change it. |
| Reason | Justification text required by the portal's own export form (defaults to `Research on incidents`) |

### Load Extra Data

*(Optional)* Path to an additional local CSV file of incident records to merge with the data retrieved from the Wildlife Trade Portal. Leave blank if you only want data from the portal.

### Select Color Palette

The color palette used to visually distinguish species and incident categories across the charts and maps in this report. Pick a named Matplotlib colormap (defaults to `tab10`) or define a custom list of hex colours.

---

## 3. Run the Workflow

Once submitted, the runner will:

1. Log in to the Wildlife Trade Portal with your email and password, then search and export incidents recorded within your configured time range, downloading the requested export file(s).
2. Merge the downloaded (and, if provided, your extra local) CSV files on `Report ID`, then retain and rename the relevant columns to a standard schema.
3. For records with more than one trade-route location (Origin/Transit/Destination), retain a single representative row per report, species, and commodity.
4. Convert numeric fields (count, weight, arrest/charge/fine/imprisonment counts, latitude, longitude) from text to numeric values, then convert the records to a point GeoDataFrame.
5. Download the GVL 30km buffer boundary from Dropbox and reproject it to `EPSG:4326`.
6. Spatially join incidents against the GVL boundary (keeping only incidents that fall within it), then additionally restrict to incidents where `Country of Incident` is Rwanda, Uganda, or Congo, Democratic Republic of The.
7. Map scientific names to simplified species groups (e.g. Elephantidae/Loxodonta → Elephant, Manidae → Pangolin) and map raw incident categories to short labels (Seizure, Poaching, Smuggling, Human-Wildlife Conflict, Enforcement).
8. Add a temporal index and decompose the incident date into year and month; split the dataset into groups per the configured grouping strategy.
9. Aggregate incidents per year (overall, by species), sum arrests and imprisonments per year, and compute an overall conviction rate (total imprisoned / total arrested, as a percent).
10. Filter to ivory-related commodities (Ivory Pieces - Raw, Ivory - Worked, Tusk) and sum seizure weight per year.
11. Render the incidents-by-species and incidents-by-category time-series bar charts.
12. Build the GVL boundary layer plus incident and species scatterplot layers, compute a map zoom/extent from the data, and render the Incidents Map and Species Map.
13. Render the filterable summary table (date, category, role, species) and persist the full processed dataset as CSV.
14. Assemble all summary stat widgets, maps, charts, and the table into the final dashboard, merging per-group views where applicable.
15. Save all outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

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
