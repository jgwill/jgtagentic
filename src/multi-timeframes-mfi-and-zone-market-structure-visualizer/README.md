
# Multi-Timeframes MFI and Zone Market Structure Visualizer

This application visualizes financial trend data, specifically focusing on Market Facilitation Index (MFI) and Zone Color indicators across multiple timeframes (M1, W1, D1, H4). It processes a user-uploaded CSV file to generate these visualizations, providing a quick overview of market conditions based on the MFI + Zone trading pattern.

![](https://i.imgur.com/Y0Yujq3.jpeg)


## Features

*   **Multi-Timeframe Visualization:** Displays data for M1, W1, D1, and H4 timeframes.
*   **MFI Signal Display:** Shows MFI signals (`++`, `--`, `-+`, `+-`) with descriptive names (Green, Fade, Fake, Squat) and intuitive glyphs (🌿, 🍂, 🎭, 🌫).
*   **Zone Color Indication:** Visualizes Zone colors (green, red, gray) for each timeframe.
*   **Trend Derivation:** Determines an overall trend (Bullish, Bearish, Neutral) based on the MFI signal.
*   **Dynamic Instrument Naming:** Derives the instrument name from the uploaded CSV filename (e.g., `SPX500.csv` becomes `SPX500`).
*   **Last Close Price:** Displays the last closing price from the most recent data row.
*   **Metadata Sidebar:** Provides context including:
    *   Instrument name and last close price.
    *   Source CSV columns used for MFI and Zone data.
    *   Summaries of MFI alignment (trend per timeframe) and Zone colors per timeframe.
*   **Responsive Design:** Adapts to different screen sizes for better usability.

## How it Works

1.  **CSV Upload:** The user uploads a CSV file containing financial data.
2.  **Data Processing:**
    *   The application requires at least two data rows (plus a header).
    *   **Trend, MFI, and Zone Data:** Information for these indicators is extracted from the **second-to-last data row** in the CSV. This represents the last *completed* bar's analysis.
    *   **Last Close Price:** The `Close` price is taken from the **last data row** (assumed to be the current, potentially incomplete, bar). If not available, it falls back to the `Close` price from the second-to-last row.
    *   **Instrument Name:** The instrument name is derived from the filename of the uploaded CSV (e.g., "EURUSD_Data.csv" would likely result in an instrument name of "EURUSD_DATA").
3.  **Visualization:** The processed data is then displayed in a structured visual format.

## Required CSV Format

The CSV file must adhere to the following:

*   **Valid CSV Structure:** Comma-separated values.
*   **Header Row:** The first row must contain column headers.
*   **Data Rows:** At least two data rows are required below the header.
*   **Essential Columns:** The application specifically looks for the following column names in the header:
    *   `Close`: The closing price of the instrument for each period.
    *   **MFI Signal Columns:**
        *   For M1 timeframe: `mfi_str_M1` (e.g., "++", "--")
        *   For W1 timeframe: `mfi_str_W1`
        *   For D1 timeframe: `mfi_str_D1`
        *   For H4 timeframe: `mfi_str`
    *   **Zone Color Columns:**
        *   For M1 timeframe: `zcol_M1` (e.g., "green", "red", "gray")
        *   For W1 timeframe: `zcol_W1`
        *   For D1 timeframe: `zcol_D1`
        *   For H4 timeframe: `zcol`

    *Note: If a column is missing or a value is not present for a specific timeframe in the relevant data row, it will be displayed as "N/A" in the visualization.*

## Interpreting the Visualization

### Metadata Sidebar

Located on the left, this section provides:

*   **Instrument & Price:** The name of the financial instrument and its last recorded closing price.
*   **Source Columns:** Lists the exact column names from your CSV (e.g., `mfi_str_M1`, `zcol`) that are being used for MFI and Zone data. This helps verify data mapping.
*   **MFI Alignment:** A summary of the derived trend (Bullish, Bearish, Neutral) for each timeframe.
*   **Zone Summary:** A summary of the Zone color for each timeframe.

### Main Visualizer Columns (from left to right)

1.  **MFI Zone Trend:**
    *   Displays the overall market trend interpreted from the MFI signal for each timeframe.
    *   **Bullish:** Indicates a positive or upward market sentiment.
    *   **Bearish:** Indicates a negative or downward market sentiment.
    *   **Neutral:** Indicates a sideways or consolidating market.
    *   **N/A:** Data not available to determine a trend.

2.  **MFI Signal:**
    *   Shows the raw MFI signal value from the CSV, its interpreted name, and a corresponding glyph.
    *   **`++` (Green 🌿):** Strong positive volume and MFI. Trend: **Bullish**.
    *   **`--` (Fade 🍂):** Weakening volume and MFI. Trend: **Bearish**.
    *   **`-+` (Fake 🎭):** Low volume with positive MFI. Often suggests a false move. Trend: **Bearish** (as per current app logic for trend derivation).
    *   **`+-` (Squat 🌫):** High volume with low MFI. Indicates consolidation or a potential turning point. Trend: **Neutral**.
    *   **`N/A` (N/A ❔):** MFI data not available. Trend: **N/A**.

3.  **Zone Color:**
    *   Displays the Zone color from the CSV, indicating market sentiment based on a combination of Awesome Oscillator (AO) and Acceleration/Deceleration Oscillator (AC) (though the raw calculation is external to this visualizer).
    *   **Green:** Typically indicates a "Buy Zone" or bullish conditions.
    *   **Red:** Typically indicates a "Sell Zone" or bearish conditions.
    *   **Gray:** Typically indicates a neutral or "Do Nothing" zone.
    *   **N/A:** Zone color data not available.

## Technology Stack

*   **React:** For building the user interface.
*   **TypeScript:** For static typing and improved code quality.
*   **Tailwind CSS:** For utility-first CSS styling.

## How to Use

1.  Open the `index.html` file in a modern web browser.
2.  Click the file input button (often styled and may not explicitly say "Choose File" depending on the browser, but will be part of the header).
3.  Select your prepared CSV file that matches the [Required CSV Format](#required-csv-format).
4.  The visualization will automatically update to reflect the data from your file.
5.  If there are errors in parsing or if the data doesn't meet requirements, an error message will be displayed.
