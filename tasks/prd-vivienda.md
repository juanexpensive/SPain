# PRD: S-Pain

## Introduction

`S-Pain` is a small data product focused on showing how housing prices have evolved over time across Spanish provinces using public INE data. The goal is to build a visually strong, easy-to-understand portfolio project that lets a user explore historical trends, identify which provinces have risen the most, and understand territorial differences through charts, rankings, and a map.

This first version is designed to be realistic for a short delivery window while still feeling like a polished product instead of a class exercise.

## Goals

- Visualize the historical evolution of housing prices by province in a clear and interactive way.
- Highlight which provinces have experienced the highest cumulative growth over time.
- Provide a simple geographic overview through a map colored by latest value or variation.
- Deliver a portfolio-ready web app with a clean interface and a clear data story.
- Keep the first version intentionally scoped so it can be completed in a few days.

## User Stories

### US-001: Load and normalize INE housing data
**Description:** As a developer, I want to fetch and normalize the INE dataset so that the app can work from a consistent internal data model.

**Acceptance Criteria:**
- [ ] The app can retrieve the selected INE public dataset or read a cached export derived from it.
- [ ] Data is normalized into a tabular structure with at least province, date/period, value, and metric labels.
- [ ] Missing or malformed rows are handled without crashing the app.
- [ ] Typecheck/lint passes

### US-002: Select a province
**Description:** As a user, I want to select a province so that I can focus the analysis on a specific territory.

**Acceptance Criteria:**
- [ ] The interface shows a province selector with all available provinces from the dataset.
- [ ] A default province is preselected on first load.
- [ ] Changing the selected province updates all dependent visualizations on the page.
- [ ] Typecheck/lint passes
- [ ] Verify in browser using dev-browser skill

### US-003: View historical evolution chart
**Description:** As a user, I want to see the historical price evolution for a province so that I can understand how it has changed over time.

**Acceptance Criteria:**
- [ ] The main chart displays the time series for the selected province.
- [ ] The x-axis represents time and the y-axis represents the housing price metric from the dataset.
- [ ] The chart remains readable on desktop and mobile widths.
- [ ] Typecheck/lint passes
- [ ] Verify in browser using dev-browser skill

### US-004: Filter by time range
**Description:** As a user, I want to adjust the time range so that I can focus on a recent or long-term period.

**Acceptance Criteria:**
- [ ] The interface provides a start period and end period control, or an equivalent range selector.
- [ ] The time-series chart updates to reflect the selected range.
- [ ] KPI calculations and ranking calculations respect the selected range.
- [ ] Invalid ranges are prevented or corrected gracefully.
- [ ] Typecheck/lint passes
- [ ] Verify in browser using dev-browser skill

### US-005: View summary KPIs
**Description:** As a user, I want to see key indicators for the selected province so that I can quickly interpret its trend.

**Acceptance Criteria:**
- [ ] The page shows at least latest available value, total variation in the selected period, and percentage variation in the selected period.
- [ ] KPI values update when the province or period changes.
- [ ] KPI labels are understandable without reading technical documentation.
- [ ] Typecheck/lint passes
- [ ] Verify in browser using dev-browser skill

### US-006: Explore provincial ranking
**Description:** As a user, I want to see which provinces have grown the most or least so that I can compare territorial trends at a glance.

**Acceptance Criteria:**
- [ ] The app displays a ranking of provinces ordered by variation over the selected period.
- [ ] The ranking can show both top increases and bottom increases, or a full sorted list that makes both visible.
- [ ] The ranking updates when the date range changes.
- [ ] Typecheck/lint passes
- [ ] Verify in browser using dev-browser skill

### US-007: View a colored map of Spain
**Description:** As a user, I want to see a map colored by value or variation so that I can understand geographic patterns quickly.

**Acceptance Criteria:**
- [ ] The app displays a map covering Spanish provinces.
- [ ] The map can color provinces by latest value or cumulative variation over the selected period.
- [ ] A legend explains the meaning of the color scale.
- [ ] If provincial geometries are unavailable, the app shows a clear fallback message instead of failing silently.
- [ ] Typecheck/lint passes
- [ ] Verify in browser using dev-browser skill

### US-008: Read generated insights
**Description:** As a user, I want to read short textual insights so that I can understand the main takeaway without interpreting every chart myself.

**Acceptance Criteria:**
- [ ] The page displays a short generated summary based on the selected province and current data range.
- [ ] The summary mentions at least one factual trend based on the dataset, such as long-term increase or ranking position.
- [ ] The summary does not invent unsupported claims.
- [ ] Typecheck/lint passes
- [ ] Verify in browser using dev-browser skill

### US-009: Handle loading and data errors clearly
**Description:** As a user, I want clear loading and error states so that the app feels reliable.

**Acceptance Criteria:**
- [ ] The app shows a loading state while retrieving or preparing data.
- [ ] The app shows a readable error message if the dataset cannot be loaded.
- [ ] Partial failures in one visual block do not blank the entire page when a graceful fallback is possible.
- [ ] Typecheck/lint passes
- [ ] Verify in browser using dev-browser skill

### US-010: Present a portfolio-ready landing layout
**Description:** As a recruiter or reviewer, I want the app to feel polished so that it communicates product sense as well as technical execution.

**Acceptance Criteria:**
- [ ] The page has a title, subtitle, and section structure that explain the purpose of the app.
- [ ] Colors, spacing, and typography feel intentional rather than default or raw.
- [ ] The layout remains usable on common laptop and mobile widths.
- [ ] Typecheck/lint passes
- [ ] Verify in browser using dev-browser skill

## Functional Requirements

- FR-1: The system must ingest a public INE housing-price dataset suitable for historical territorial analysis.
- FR-2: The system must normalize the data into a structure that supports filtering by province and period.
- FR-3: The system must let the user select a province as the main analysis target.
- FR-4: The system must display a historical line chart for the selected province.
- FR-5: The system must let the user limit the visible analysis to a selected time range.
- FR-6: The system must calculate and display summary metrics for the selected province and range.
- FR-7: The system must rank provinces by variation across the selected period.
- FR-8: The system must display a Spain map with provincial coloring based on a selected metric when geometry data is available.
- FR-9: The system must show a legend and clear labeling for all visual encodings.
- FR-10: The system must generate concise text insights based only on the loaded data.
- FR-11: The system must provide explicit loading, empty, and error states.
- FR-12: The system must render a responsive interface appropriate for desktop and mobile use.
- FR-13: The system must make the recommended stack explicit in project documentation, even if the implementation decision is finalized later.

## Non-Goals

- No price prediction, forecasting, or machine learning models.
- No authentication, accounts, or user-specific saved dashboards.
- No advanced custom frontend architecture that slows delivery of the first version.
- No real estate listing search or integration with private portals.
- No municipal or neighborhood-level analysis unless the selected dataset directly supports it and the scope is reconsidered.
- No download center, reporting engine, or PDF export in the first version.

## Design Considerations

- The interface should feel like a compact analytical product, not a notebook with widgets.
- The top of the page should communicate the app value immediately with a strong title and one-sentence explanation.
- KPI cards should sit near the top so the user gets an instant summary before reading the chart.
- The main line chart should be the visual centerpiece.
- Ranking and map should complement the chart rather than compete with it.
- The language should stay simple and explanatory because the likely audience includes recruiters and non-specialists.

## Technical Considerations

- Python with Streamlit is the recommended implementation path because it enables fast delivery and a polished UI with low frontend overhead.
- The PRD does not fully lock the stack, but any alternative should preserve the fast-delivery goal.
- The INE API or dataset access pattern should be validated early, including field naming, territorial granularity, and update cadence.
- A local cached data file may be useful to avoid repeated API calls during development or demo sessions.
- Provincial map rendering may require an external GeoJSON or shapefile source compatible with the chosen province identifiers.
- Data transformation logic should be separated from UI rendering so the app can be maintained and extended later.
- Recommended implementation sequencing:
  - first complete the UI and analytics slices against a stable sample or cached dataset
  - then connect the real INE source inside `US-001` once the internal data contract is stable
  - this reduces the risk of mixing ingestion/debugging problems with unfinished product slices

## Success Metrics

- A user can choose a province and understand its historical trend within the first 30 seconds of use.
- The app can answer both of these questions clearly: "How has this province evolved?" and "Which provinces have risen the most?"
- The interface works reliably in a live demo without broken states caused by common data issues.
- The finished project is strong enough to include in a CV or portfolio with a public demo and screenshots.
- The first version is implementable within a short timebox of a few days.

## Open Questions

- Which exact INE dataset should be used as the canonical source for the first release?
- Should the default map metric be latest value, accumulated variation, or percentage variation?
- Should the ranking show absolute change, percentage change, or allow switching between both?
- Is province-level coverage complete enough in the selected dataset, or will the first version need fallback support for autonomous communities?
- The app name is now `S-Pain`; future naming work should focus on branding polish rather than a full rename.
