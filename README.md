# WWF Traffic Workflow — User Guide

This guide walks you through configuring and running the WWF Traffic workflow, which processes user-uploaded wildlife trafficking incident reports, filters them to incidents within a 30km buffer of the Greater Virunga Landscape (GVL) boundary, and produces an interactive dashboard of trafficking trends by species, incident category, and country.

---

## Overview

The workflow delivers, for each run:

- **Summary stat widgets** — Total Incidents, Incidents This Year vs Last Year, Most Frequently Trafficked Flagship Species, Total Suspects Arrested, Total Suspects Convicted, Conviction Rate, and Total Seizures of Ivory (kg)
- An **Incidents Map** — point map of trafficking incidents coloured by incident category, overlaid on the GVL boundary
- A **Species Map** — point map of trafficking incidents coloured by mapped species group, overlaid on the GVL boundary
- An **Incidents by Species chart** — time-series bar chart of incident counts per year, broken down by species
- An **Incidents by Category chart** — time-series bar chart of incident counts per year, broken down by incident category
- A **Summary Table** — filterable/sortable table of individual incidents (date, category, role, species)

All widgets are grouped by whichever grouping strategy you configure (Species or Country of Incident, or one combined view if left blank) and assembled into a single dashboard.

---

## Prerequisites

Before running the workflow, ensure you have:

- One or more **CSV exports of trafficking incident reports** to upload, all sharing a common `Report ID` column used to merge them
- The uploaded data includes (or can be mapped to) the following source columns: `Report ID`, `Category of Incident_x`, `Country of Incident_x`, `Date of Incident_x`, `Full Scientific Name`, `Item / Commodity Type`, `Count`, `Weight`, `Unit of Weight`, `Kingdom`, `Phylum`, `Class`, `Order`, `Family`, `Common Name`, `Role`, `Order in Trade Route`, `Country`, `Latitude`, `Longitude`, `Outcome`, `Number of People Arrested`, `Number of People Charged`, `Number of People Fined`, `Number of People Imprisoned`

> The GVL 30km buffer boundary is downloaded automatically from Dropbox at runtime — no local copy is required.

---

## Step-by-Step Configuration

### Step 1 — Add the Workflow Template

In the Ecoscope app, navigate to the **Workflow Templates** tab and click **Add Workflow Template**. In the **Github Link** field, paste the repository URL:

```
https://github.com/wildlife-dynamics/wwf-traffic.git
```

Then click **Add Template** to register the template.

---

### Step 2 — Select the Workflow

Go to **Workflow Templates**. The newly added template appears as the **wwf-traffic** card. Click the card to open the workflow configuration form.

---

### Step 3 — Set Workflow Details and Time Range

**Set workflow details**

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run (required) |
| Workflow Description | Optional notes to differentiate this run from others |

**Time range**

| Field | Description |
|-------|-------------|
| Timezone | Select the local timezone (e.g. `Africa/Nairobi (UTC+03:00)`) |
| Since | Start date and time — incidents from this point are included |
| Until | End date and time of the analysis window |

---

### Step 4 — Configure Grouping Strategy

Choose how the dashboard should be split into separate views:

| Option | Description |
|--------|-------------|
| Species | One dashboard view per mapped species group (e.g. Elephant, Hippo, Gorilla) |
| Country | One dashboard view per country of incident |
| *(blank)* | All data appears in a single combined view |

---

### Step 5 — Configure Basemaps

Select the tile layers to use as base layers under the incident and species maps. The first layer selected is the bottommost. Defaults to **Terrain** and **Satellite** (50% opacity) if left unset.

---

### Step 6 — Load Traffic CSV Files

Upload the CSV file(s) containing your trafficking incident reports. All files are merged on the `Report ID` column, so every file must include it.

---

### Step 7 — Select Color Palette

Choose a colour palette used to colour incidents by category and by species on the maps and charts. You can pick a named Matplotlib colormap (defaults to `tab10`) or define a custom list of hex colours.

---

## Running the Workflow

Once submitted, the runner will:

1. Merge the uploaded CSV files on `Report ID`, then retain and rename the relevant columns to a standard schema.
2. For records with more than one trade-route location (Origin/Transit/Destination), retain a single representative row per report, species, and commodity.
3. Convert numeric fields (count, weight, arrest/charge/fine/imprisonment counts, latitude, longitude) from text to numeric values, then convert the records to a point GeoDataFrame.
4. Download the GVL 30km buffer boundary from Dropbox and reproject it to `EPSG:4326`.
5. Spatially join incidents against the GVL boundary, keeping only incidents that fall within it.
6. Map scientific names to simplified species groups (e.g. Elephantidae/Loxodonta → Elephant, Manidae → Pangolin) and map raw incident categories to short labels (Seizure, Poaching, Smuggling, Human-Wildlife Conflict, Enforcement).
7. Add a temporal index and decompose the incident date into year and month; split the dataset into groups per the configured grouping strategy.
8. Aggregate incidents per year (overall, by species), sum arrests and imprisonments per year, and compute a conviction rate (imprisoned / arrested, as a percent).
9. Filter to ivory-related commodities (Ivory Pieces - Raw, Ivory - Worked, Tusk) and sum seizure weight per year.
10. Render the incidents-by-species and incidents-by-category time-series bar charts.
11. Build the GVL boundary layer plus incident and species scatterplot layers, compute a map zoom/extent from the data, and render the Incidents Map and Species Map.
12. Render the filtered summary table (date, category, role, species).
13. Assemble all summary stat widgets, maps, charts, and the table into the final dashboard, merging per-group views where applicable.
14. Save all outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

---

## Output Files

All outputs are written as HTML files to `$ECOSCOPE_WORKFLOWS_RESULTS/`, named `<content-hash>_<suffix>.html`:

| Suffix | Description |
|--------|-------------|
| `..._incidents_by_species.html` | Time-series bar chart of incidents per year, by species |
| `..._incidents_by_category.html` | Time-series bar chart of incidents per year, by incident category |
| `..._incidents_by_category.html` (map) | Interactive Incidents Map coloured by incident category |
| `..._incidents_by_species.html` (map) | Interactive Species Map coloured by species group |
| `..._summary_table_of_incidents.html` | Filterable/sortable summary table of individual incidents |

One file is produced per grouped view (e.g. per species or per country) if a grouping strategy is configured. The final dashboard bundles all of the above, along with the summary stat widgets (Total Incidents, Incidents YoY, Most Trafficked Species, Total Arrested, Total Convicted, Conviction Rate, Total Ivory Seized), into a single interactive view.
