"""
Generate the WWF Traffic Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: wwf_traffic_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from datetime import date

OUTPUT_FILE = "wwf_traffic_technical_guide.pdf"

# ── Colour palette (same as STE Mapbook) ─────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=24, leading=30, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=12, leading=16, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=14, leading=18, textColor=GREEN_DARK,
                  spaceBefore=16, spaceAfter=5, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=11, leading=15, textColor=GREEN_MID,
                  spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=9.5, leading=13, textColor=SLATE,
                  spaceBefore=7, spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=5, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=13, textColor=SLATE,
                  spaceAfter=2, leftIndent=14, firstLineIndent=-10)
CELL     = _style("Cell", fontSize=8.5, leading=12, textColor=SLATE,
                  spaceAfter=0, spaceBefore=0)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():
    return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)

def p(text, style=BODY):       return Paragraph(text, style)
def h1(text):                  return Paragraph(text, H1)
def h2(text):                  return Paragraph(text, H2)
def h3(text):                  return Paragraph(text, H3)
def sp(n=6):                   return Spacer(1, n)
def bullet(text):              return Paragraph(f"• {text}", BULLET)
def note(text):                return Paragraph(f"<b>Note:</b> {text}", NOTE)
def c(text):                   return Paragraph(text, CELL)   # table cell paragraph


def make_table(data, col_widths):
    """Build a table where every cell value is already a Paragraph (use c())."""
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  GREEN_DARK),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",           (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",    (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 6),
        ("TOPPADDING",     (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


# ── Page template ─────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN_DARK)
    canvas.rect(0, 0, w, 22, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5*cm, 7, "WWF Traffic — Technical Guide")
    canvas.drawRightString(w - 1.5*cm, 7, f"Page {doc.page}")
    canvas.setFillColor(AMBER)
    canvas.rect(0, h - 4, w, 4, fill=1, stroke=0)
    canvas.restoreState()


# ── Build story ───────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="WWF Traffic — Technical Guide",
        author="Ecoscope",
    )

    story = []

    # ── Cover ─────────────────────────────────────────────────────────────────
    story += [
        sp(60),
        p("WWF Traffic", TITLE),
        p("Technical Guide", SUBTITLE),
        sp(8),
        hr(),
        p("Wildlife Trafficking Incident Analysis — Methodology &amp; Calculation Reference", META),
        p(f"Version 1.0  ·  Generated {date.today().strftime('%B %d, %Y')}", META),
        hr(),
        PageBreak(),
    ]

    # ── 1. Overview ───────────────────────────────────────────────────────────
    story += [
        h1("1. Overview"), hr(),
        p(
            "The <b>WWF Traffic</b> workflow logs in to the <b>TRAFFIC Wildlife Trade "
            "Portal</b> (wildlifetradeportal.org) on the user's behalf, downloads wildlife "
            "trafficking incident export CSVs for a configured time range, filters the "
            "resulting incidents to a 30 km buffer of the <b>Greater Virunga Landscape "
            "(GVL)</b> boundary, and produces an interactive dashboard of trafficking "
            "trends by species, incident category, and country."
        ),
        p(
            "Unlike the EarthRanger-connected workflows in this fleet, WWF Traffic has no "
            "EarthRanger data source. Instead, a lightweight REST client (&sect;2.1) "
            "authenticates directly against the portal's API, searches by date range, "
            "species, and country, and exports the matching incidents as CSV — the user "
            "only supplies portal credentials (or an access token) and a time range, with "
            "no manual export/upload step and no browser required. An optional local CSV "
            "can still be merged in for supplementary records "
            "(&sect;3.8), and the only other network dependency is a one-time download of "
            "the GVL boundary file from Dropbox."
        ),
        note(
            "This workflow currently has no <code>test-cases.yaml</code> in the repository. "
            "CI's test-case validation step will fail until one is added — see the "
            "Troubleshooting page."
        ),
    ]

    # ── 2. Dependencies ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("2. Dependencies &amp; Prerequisites"), hr(),

        h2("2.1 Traffic Portal Connection &amp; Download"),
        p(
            "<code>connect_to_portal</code> builds a <code>WildlifeTradePortalIO</code> "
            "REST client — a small <code>requests</code>-based wrapper around the portal's "
            "(unofficial, reverse-engineered) JSON API, not a browser. It accepts either an "
            "<code>access_token</code> (advanced) or a <code>username</code>/<code>"
            "password</code> pair entered on the workflow's own config form — there is no "
            "platform-managed named connection for the Traffic Portal yet, so credentials "
            "are regular form fields rather than an env-var-backed connection. "
            "<code>server</code>, <code>timeout</code>, and <code>verify</code> (whether a "
            "supplied token is validated immediately via a lightweight account lookup) round "
            "out the advanced fields."
        ),
        p(
            "The resulting client is passed to <code>export_search_results</code> along "
            "with the workflow's configured <code>time_range</code>, <code>species</code> "
            "and <code>countries</code> filters, and a <code>save_to</code> path "
            "(<code>ECOSCOPE_WORKFLOWS_RESULTS</code>). It runs the whole search-then-export "
            "pipeline in one call: paginate through every incident matching the filters "
            "(<code>date_from</code>/<code>date_till</code> sent as plain ISO "
            "<code>YYYY-MM-DD</code>), collect their <code>Unique_ID</code>s, then request a "
            "server-side export job for those IDs and download each resulting file via a "
            "presigned S3 URL."
        ),
        p(
            "<code>countries</code> defaults to <b>Rwanda</b>, <b>Uganda</b>, and "
            "<b>Congo, Democratic Republic of The</b> — restricting the search itself, not "
            "just the local filter in &sect;3.5. This matters for pagination: without a "
            "country filter, the search has to walk through every incident worldwide in the "
            "requested time range before the true count for these three countries is known, "
            "which for a wide/unfiltered time range can mean the search never reaches far "
            "enough back to surface older Virunga-region incidents at all. Scoping the "
            "search server-side means the full requested history for the region is reachable "
            "in far fewer requests."
        ),
        make_table(
            [
                [c("Export type"),                        c("Toggle"),               c("Downloaded filename pattern")],
                [c("Incident (always included)"),         c("&mdash;"),              c("wtp_export_incident_&lt;id&gt;_&lt;timestamp&gt;.csv")],
                [c("Species/commodity"),                  c("include_species"),      c("wtp_export_species_&lt;id&gt;_&lt;timestamp&gt;.csv")],
                [c("Trade-route/location"),               c("include_locations"),    c("wtp_export_locations_&lt;id&gt;_&lt;timestamp&gt;.csv")],
            ],
            [5*cm, 4*cm, 7*cm],
        ),
        sp(4),
        p(
            "Both toggles default to <code>true</code> in this workflow's <code>spec.yaml</code> "
            "— all three files are needed for the merge described in &sect;2.2, so disabling "
            "either one will cause the downstream column-presence check in &sect;3.1 to "
            "fail. The default justification text is <code>\"Research and analysis of "
            "wildlife trade incidents in the Virunga region for conservation purposes.\"</code> "
            "(<code>reason</code>)."
        ),
        p(
            "<code>sub_page_size</code> controls how many rows are requested per underlying "
            "API page (client default 100 if left blank) — it is purely a batching size, "
            "<i>not</i> a cap on the total result set. Every incident matching the filters is "
            "always fetched, walking every page regardless of how many that turns out to be. "
            "If the portal responds with an HTTP 429 (rate limited), the client automatically "
            "waits (honoring a <code>Retry-After</code> header when present, otherwise an "
            "exponential backoff) and retries — up to 5 times by default — before raising."
        ),
        p(
            "The downloaded file paths feed directly into <code>load_and_merge_csvs."
            "file_paths</code> (&sect;2.2) — there is no separate manual upload step in "
            "this workflow's config form."
        ),

        sp(4), h2("2.2 Input Data — Three Merged CSV Exports"),
        p(
            "<code>load_and_merge_csvs</code> takes the list of file paths returned by the "
            "download step (&sect;2.1) and merges them sequentially on <code>Report ID</code>. "
            "The workflow's retained columns span three functional groups of data that, in "
            "the TRAFFIC portal export, come from separate files:"
        ),
        make_table(
            [
                [c("File role"),                c("Key columns used")],
                [c("Incident / case file"),      c("Category of Incident, Country of Incident, Date of Incident, "
                                                     "Outcome, Number of People Arrested/Charged/Fined/Imprisoned")],
                [c("Species / commodity file"),  c("Full Scientific Name, Item / Commodity Type, Count, Weight, "
                                                     "Unit of Weight, Kingdom, Phylum, Class, Order, Family, Common Name")],
                [c("Trade-route / location file"), c("Role, Order in Trade Route, Country, Latitude, Longitude")],
            ],
            [4.5*cm, 11.5*cm],
        ),
        sp(4),
        p(
            "<code>Category of Incident</code>, <code>Country of Incident</code>, and "
            "<code>Date of Incident</code> appear in more than one file. After the merge, "
            "pandas suffixes the duplicated columns (<code>_x</code>, <code>_y</code>, "
            "&hellip;); <code>map_columns</code> retains only the "
            "<code>_x</code> variant of each (i.e. the value from whichever file was "
            "loaded first) and renames it to a standard lowercase/snake_case schema "
            "(e.g. <code>category_of_incident</code>, <code>country_of_incident</code>, "
            "<code>date_of_incident</code>)."
        ),

        sp(4), h2("2.3 Grouping Strategy"),
        p(
            "<code>set_groupers</code> is restricted via <code>rjsf-overrides</code> to only "
            "<b>ValueGrouper</b> fields (temporal and spatial grouping are disabled for this "
            "workflow), and further restricted to exactly two grouping columns:"
        ),
        make_table(
            [
                [c("Grouper"),             c("Index name"),         c("Effect")],
                [c("Species"),             c("category"),           c("One dashboard view per mapped species group")],
                [c("Country"),             c("country"),            c("One dashboard view per country")],
            ],
            [3.5*cm, 4.5*cm, 8*cm],
        ),
        sp(4),
        p(
            "Left blank, the workflow produces a single combined view. The selectable "
            "<code>index_name</code> values changed from <code>common_group</code>/"
            "<code>country_of_incident</code> to <code>category</code>/<code>country</code> "
            "in this revision of <code>spec.yaml</code> — the dropdown labels shown to the "
            "user (Species / Country) are unchanged."
        ),

        sp(4), h2("2.4 GVL 30 km Buffer Boundary"),
        p(
            "<code>fetch_and_persist_file</code> downloads <code>gvl_30km_buffer.parquet</code> "
            "from Dropbox (<code>overwrite_existing: true</code>, 3 retries) and loads it via "
            "<code>load_df</code>. It is reprojected to <b>EPSG:4326</b> "
            "(<code>reproject_gdf</code>) before being used both for the spatial join "
            "(&sect;3.5) and as a static map layer (&sect;4)."
        ),

        sp(4), h2("2.5 Base Map Tile Layers"),
        make_table(
            [
                [c("Layer"),                        c("Opacity"), c("Max zoom")],
                [c("ESRI World Topographic Map"),   c("100 %"),   c("20")],
                [c("ESRI World Imagery"),           c("50 %"),    c("20")],
            ],
            [10*cm, 2.5*cm, 4*cm],
        ),

        sp(4), h2("2.6 Colour Palette"),
        p(
            "<code>set_color_palette</code> defaults to the Matplotlib <b>tab10</b> named "
            "colormap, but accepts a custom list of hex colours instead. The chosen palette "
            "is applied twice via <code>apply_cmap</code> — once to "
            "<code>category_of_incident</code> (output column "
            "<code>incident_colors</code>) and once to <code>common_group</code> (output "
            "column <code>species_colors</code>), both as RGBA tuples at full alpha."
        ),
    ]

    # ── 3. Data Ingestion ─────────────────────────────────────────────────────
    story += [
        sp(4), h1("3. Data Ingestion Pipeline"), hr(),

        h2("3.1 Column Mapping"),
        p(
            "After the CSV merge, <code>map_columns</code> retains 23 columns (see &sect;2.2) "
            "and renames them to snake_case (<code>raise_if_not_found: true</code> — the "
            "run fails immediately if any expected column is missing from the merged data)."
        ),

        sp(4), h2("3.2 Trade Route De-duplication"),
        p(
            "A trafficking incident may involve multiple trade-route locations "
            "(Origin, Transit, Destination). <code>extract_trade_route</code> retains a "
            "single representative row per (<code>report_id</code>, "
            "<code>full_scientific_name</code>, <code>commodity_type</code>) combination, "
            "using the <code>role</code> column to identify route roles and "
            "<code>order_in_trade_route</code> to determine which row to keep when more "
            "than one location is present."
        ),

        sp(4), h2("3.3 Numeric Conversion &amp; Geometry"),
        p(
            "<code>convert_column_values_to_numeric</code> coerces <code>count</code>, "
            "<code>weight</code>, the four arrest/charge/fine/imprisonment count columns, "
            "and <code>latitude</code>/<code>longitude</code> from text to numeric types. "
            "<code>df_to_point_gdf</code> then builds point geometries from "
            "<code>latitude</code>/<code>longitude</code> in <b>EPSG:4326</b>."
        ),

        sp(4), h2("3.4 Spatial Join Against the GVL Boundary"),
        p(
            "<code>spatial_join</code> performs an inner, <code>within</code>-predicate join "
            "between the incident points and the reprojected GVL 30 km buffer, dropping any "
            "incident that falls outside the buffer."
        ),

        sp(4), h2("3.5 Country Restriction"),
        p(
            "<code>filter_row_values</code> additionally restricts "
            "<code>country_of_incident</code> to exactly three values: <b>Rwanda</b>, "
            "<b>Uganda</b>, and <b>Congo, Democratic Republic of The</b>. This runs "
            "<i>after</i> the spatial join, so an incident can pass the 30 km buffer test "
            "geometrically but still be dropped here if its "
            "<code>country_of_incident</code> text doesn't exactly match one of these three "
            "strings."
        ),

        sp(4), h2("3.6 Species &amp; Category Mapping"),
        p(
            "<code>add_mapped_column_value</code> maps <code>full_scientific_name</code> to "
            "a simplified <code>common_group</code> label (e.g. Elephantidae/Loxodonta → "
            "Elephant, Manidae → Pangolin, Hippopotamus amphibius → Hippo) and "
            "<code>category_of_incident</code> to a short <code>incident_category</code> "
            "label (Seizure, Poaching, Smuggling, Human-Wildlife Conflict, Enforcement). "
            "Both mappings use <code>keep_unmapped: true</code> — a value not covered by "
            "the mapping table passes through as its original text rather than being "
            "dropped."
        ),

        sp(4), h2("3.7 Temporal Index"),
        p(
            "<code>add_temporal_index</code> keys the dataset to <code>date_of_incident</code>, "
            "grouped by the configured grouper. <code>decompose_datetime</code> then extracts "
            "<code>year</code> and <code>month</code> components (prefixed "
            "<code>incident_</code>, e.g. <code>incident_year</code>) for the time-series "
            "aggregations in &sect;6."
        ),

        sp(4), h2("3.8 Optional Local Data Merge"),
        p(
            "<code>load_extra_data</code> (task <code>load_df</code>) optionally loads a "
            "user-supplied local CSV of additional incident records — its <code>file_path</code> "
            "is left unbound in <code>spec.yaml</code> so it remains a plain config-form "
            "field, unlike every other input in this pipeline, which is now sourced "
            "automatically from the Traffic Portal download (&sect;2.1). "
            "<code>merge_traffic_xlsx</code> then merges it against the temporal-indexed "
            "portal dataset from &sect;3.7, and the merged result is re-converted to a "
            "point GeoDataFrame before colour mapping (&sect;2.6)."
        ),
    ]

    # ── 4. Static Map Layers ──────────────────────────────────────────────────
    story += [
        sp(4), h1("4. Static Map Layers"), hr(),
        p(
            "One static layer — the GVL boundary — is composited onto both the Incidents "
            "Map and the Species Map."
        ),

        h2("4.1 GVL Boundary Layer"),
        make_table(
            [
                [c("Property"),      c("Value")],
                [c("Fill"),          c("None (outline only)")],
                [c("Line colour"),   c("Black (0, 0, 0)")],
                [c("Line width"),    c("1.25 px (min 1, max 5)")],
                [c("Opacity"),       c("45 %")],
                [c("Legend"),        c("&ldquo;GVL Boundary (30km buffer)&rdquo;")],
            ],
            [4.5*cm, 11.5*cm],
        ),
    ]

    # ── 5. Map Outputs ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("5. Map Outputs — Methodology"), hr(),

        h2("5.1 Incidents Map"),
        p(
            "<code>create_scatterplot_layer</code> renders each incident as a point coloured "
            "by <code>incident_colors</code> (from &sect;2.6), at 2.35 px radius and 75 % "
            "opacity with stroked outlines. Combined with the GVL boundary layer, auto-zoomed "
            "to the incident extent (max zoom 12 for view-state calculation, 10 for the "
            "rendered map), and persisted as HTML."
        ),

        sp(4), h2("5.2 Species Map"),
        p(
            "Identical construction to the Incidents Map, but points are coloured by "
            "<code>species_colors</code> instead of <code>incident_colors</code> — same "
            "radius, opacity, and stroke settings."
        ),

        sp(4), h2("5.3 Filename Suffix Collision"),
        note(
            "The Incidents Map is persisted with <code>filename_suffix: incidents_by_category</code> "
            "— the exact same suffix used by the incidents-by-category bar chart (&sect;6.1). "
            "Likewise, the Species Map uses <code>filename_suffix: incidents_by_species</code>, "
            "the same suffix as the incidents-by-species bar chart. This is a naming quirk "
            "in <code>spec.yaml</code>, not a runtime collision — each persisted file is "
            "additionally prefixed with a content hash — but it means the suffix alone "
            "cannot distinguish a map file from a chart file."
        ),
    ]

    # ── 6. Charts ─────────────────────────────────────────────────────────────
    story += [
        sp(4), h1("6. Charts"), hr(),

        h2("6.1 Incidents by Species / by Category"),
        p(
            "Two <code>draw_time_series_bar_chart</code> calls share the same x-axis "
            "(<code>date_of_incident</code>, bucketed yearly), y-axis "
            "(<code>report_id</code>, counted), and colour column "
            "(<code>species_colors</code> — used for <i>both</i> charts, even the "
            "by-category one). They differ only in the <code>category</code> field: "
            "<code>common_group</code> for the species chart, "
            "<code>incident_category</code> for the category chart."
        ),
    ]

    # ── 7. Summary Metrics ────────────────────────────────────────────────────
    story += [
        sp(4), h1("7. Summary Metrics"), hr(),

        h2("7.1 Per-Year Aggregations"),
        p(
            "<code>aggregate_by</code> computes, per group and per "
            "<code>incident_year</code>: total incident count "
            "(<code>no_of_incidents</code>), incident count by "
            "<code>incident_year</code> &times; <code>common_group</code>, total people "
            "arrested (sum), and total people imprisoned (sum)."
        ),

        sp(4), h2("7.2 Conviction Rate — Two Independent Calculations"),
        p(
            "There are <b>two separate conviction-rate computations</b> in this workflow, "
            "and only one of them reaches the dashboard:"
        ),
        make_table(
            [
                [c("Path"),                    c("Scope"),                  c("Reaches dashboard?")],
                [c("add_conviction_rate"),      c("Per incident_year"),      c("No &mdash; computed but never referenced downstream")],
                [c("conviction_ratio → conviction_rate_pct"), c("All-time single ratio"), c("Yes &mdash; feeds the Conviction Rate widget")],
            ],
            [5*cm, 5*cm, 6*cm],
        ),
        sp(4),
        p(
            "The dashboard's <b>Conviction Rate</b> widget is "
            "<code>total_imprisoned &divide; total_arrested &times; 100</code>, computed "
            "with <code>safe_divide</code> (<code>fill_invalid: 0.0</code>) across the "
            "entire time range — not a per-year figure."
        ),

        sp(4), h2("7.3 Ivory Seizures"),
        p(
            "<code>filter_row_values</code> restricts <code>commodity_type</code> to "
            "<code>Ivory Pieces - Raw</code>, <code>Ivory - Worked</code>, and "
            "<code>Tusk</code>, then <code>aggregate_by</code> sums <code>weight</code> per "
            "<code>incident_year</code>, feeding the <b>Total Seizures of Ivory (kg)</b> "
            "widget (all-time sum)."
        ),

        sp(4), h2("7.4 Most Trafficked Species"),
        p(
            "<code>aggregate_by</code> counts incidents per <code>common_group</code> across "
            "the full time range; <code>get_top_category</code> picks the highest count and "
            "formats it as a label (e.g. &ldquo;Elephant &mdash; 214 incidents&rdquo;) for the "
            "<b>Top Trafficked Species</b> text widget."
        ),
    ]

    # ── 8. Summary Table ──────────────────────────────────────────────────────
    story += [
        sp(4), h1("8. Summary Table &amp; CSV Export"), hr(),
        p(
            "<code>subset_columns</code> narrows the dataset to "
            "<code>date_of_incident</code>, <code>incident_category</code>, "
            "<code>role</code>, and <code>common_group</code>; <code>map_columns</code> "
            "renames these to display labels (Date, Incident Category, Role, Species); "
            "<code>draw_table</code> renders it with sorting and filtering enabled "
            "(download disabled)."
        ),
        p(
            "Separately, <code>persist_df</code> writes the <i>full</i> processed "
            "per-group dataset (all mapped/renamed columns, not the narrowed summary "
            "table) to CSV with an auto-generated filename."
        ),
    ]

    # ── 9. Interactive Dashboard ───────────────────────────────────────────────
    story += [
        sp(4), h1("9. Interactive Dashboard"), hr(),
        p("<code>gather_dashboard</code> assembles the dashboard from twelve widgets:"),
        make_table(
            [
                [c("Widget"),                       c("Type"),          c("Source")],
                [c("Total Number of Incidents"),     c("Single value"),  c("incidents_per_year (sum)")],
                [c("Incidents This Year vs Last Year"), c("Period comparison"), c("incidents_per_year")],
                [c("Top Trafficked Species"),        c("Text"),          c("species_totals → get_top_category")],
                [c("Total Suspects Arrested"),       c("Single value"),  c("total_arrested (sum)")],
                [c("Total Suspects Convicted"),      c("Single value"),  c("total_imprisoned (sum)")],
                [c("Conviction Rate"),               c("Single value"),  c("conviction_rate_pct &mdash; see &sect;7.2")],
                [c("Total Seizures of Ivory (kg)"),  c("Single value"),  c("ivory_weight_per_year (sum)")],
                [c("Incidents Map"),                 c("Map"),           c("draw_incidents_map")],
                [c("Species Map"),                   c("Map"),           c("draw_species_map")],
                [c("Incidents by Species Over Time"), c("Plot"),         c("ts_species_chart")],
                [c("Incidents by Category Over Time"), c("Plot"),        c("ts_category_chart")],
                [c("Summary Table of Incidents"),    c("Table"),         c("filtered_table_html")],
            ],
            [5*cm, 3*cm, 8*cm],
        ),
        sp(4),
        note(
            "Most widgets skip if their input DataFrame is empty "
            "(<code>skipif: any_is_empty_df</code>); the Incidents-YoY widget instead uses "
            "<code>skipif: never</code>, so it always renders even for groups with no data."
        ),
    ]

    # ── 10. Output Files ──────────────────────────────────────────────────────
    story += [
        sp(4), h1("10. Output Files"), hr(),
        p("All files are written to <code>$ECOSCOPE_WORKFLOWS_RESULTS</code>."),
        make_table(
            [
                [c("File / suffix"),                          c("Content")],
                [c("&lt;hash&gt;_incidents_by_species.html"), c("Incidents-by-species bar chart <i>or</i> Species Map (see &sect;5.3)")],
                [c("&lt;hash&gt;_incidents_by_category.html"), c("Incidents-by-category bar chart <i>or</i> Incidents Map (see &sect;5.3)")],
                [c("&lt;hash&gt;_summary_table_of_incidents.html"), c("Filterable/sortable summary table")],
                [c("&lt;group&gt;.csv"),                       c("Full processed incident dataset for that group")],
            ],
            [6*cm, 10*cm],
        ),
    ]

    # ── 11. Workflow Execution Logic ──────────────────────────────────────────
    story += [
        sp(4), h1("11. Workflow Execution Logic"), hr(),

        h2("11.1 Skip Conditions"),
        p(
            "Two default skip conditions apply to every task "
            "(<code>task-instance-defaults</code>): <b>any_is_empty_df</b> and "
            "<b>any_dependency_skipped</b>. Most widget tasks additionally opt into "
            "<code>any_is_empty_df</code> explicitly; the Incidents-YoY widget instead uses "
            "<code>skipif: never</code>."
        ),

        sp(4), h2("11.2 Data Flow Summary"),
        make_table(
            [
                [c("Stage"),              c("Tasks")],
                [c("Setup"),              c("Workflow details, time range, timezone, groupers, base maps, colour palette")],
                [c("Portal download"),    c("Connect to Traffic Portal (credentials or token) → search &amp; export matching incidents (Rwanda/Uganda/Congo DRC by default) for time range")],
                [c("Ingest"),             c("Merge downloaded CSVs (+ optional local CSV) → map columns → dedupe trade routes → numeric conversion → point GDF")],
                [c("GVL context"),        c("Download GVL buffer → reproject → spatial join → country restriction")],
                [c("Labelling"),          c("Species mapping → incident category mapping → temporal index → optional local merge → colormaps")],
                [c("Group split"),        c("split_groups by configured grouper (or single combined group)")],
                [c("Metrics"),            c("Per-year incidents/arrests/imprisonments, conviction rate, ivory totals, top species")],
                [c("Charts"),             c("Species &amp; category time-series bar charts")],
                [c("Maps"),               c("GVL boundary layer + incident/species scatterplot layers → Incidents Map, Species Map")],
                [c("Table &amp; CSV"),    c("Subset/rename → summary table; full dataset → CSV")],
                [c("Dashboard"),          c("gather_dashboard combines all 12 widgets")],
            ],
            [4.5*cm, 12*cm],
        ),
    ]

    # ── 12. Software Versions ─────────────────────────────────────────────────
    story += [
        sp(4), h1("12. Software Versions"), hr(),
        make_table(
            [
                [c("Package"),                              c("Version"),               c("Role")],
                [c("ecoscope-platform"),                    c(">=2.15.0, &lt;2.16.0"),  c("Consolidated core task library and workflow engine")],
                [c("ecoscope-workflows-ext-custom"),        c("0.1.0rc14.*"),           c("Utility tasks (maps, layers, column mapping)")],
                [c("ecoscope-workflows-ext-ste"),           c("0.0.0rc1.*"),            c("Spatial operations tasks (spatial join, view state)")],
                [c("ecoscope-workflows-ext-wwf-virunga"),   c("0.0.0rc7.*"),            c("WWF Virunga domain tasks (colormaps, aggregation, ratios, top-category, portal connect/search/export)")],
                [c("pydeck"),                                c("0.9.2"),                 c("Deck.gl map rendering")],
                [c("opentelemetry-sdk"),                    c(">=1.20.0, &lt;2.0.0"),   c("Observability/tracing")],
            ],
            [6*cm, 4*cm, 6.5*cm],
        ),
        sp(4),
        p(
            "This workflow runs on the consolidated <code>ecoscope-platform</code> package "
            "scheme. Packages are distributed via the <code>repo.prefix.dev</code> conda "
            "channels and pinned to compatible version ranges. The runtime environment is "
            "managed by <b>pixi</b>."
        ),
    ]

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF written → {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
