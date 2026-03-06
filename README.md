# Cafe Finder Agent

An AI-powered agent that scans a map to find the newest cafes in a given area.

## Overview

This project provides a map-scanning agent that identifies recently opened cafes within a specified geographic area. It leverages mapping APIs and location data to discover, rank, and present the newest cafe openings near you.

## Features

- Search for cafes within a defined radius of any location
- Sort results by opening date to surface the newest spots
- Display cafe details including name, address, rating, and opening date
- Support for multiple map data providers (Google Maps, OpenStreetMap)

## Getting Started

### Prerequisites

- Python 3.10+
- A Google Maps API key (or other supported map provider key)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/McJohnte/Repo-what-a-gwan.git
   cd Repo-what-a-gwan
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set your API key as an environment variable:

   ```bash
   export MAPS_API_KEY="your-api-key-here"
   ```

### Usage

Run the agent with a location and search radius:

```bash
python agent.py --location "New York, NY" --radius 5
```

#### Options

| Flag         | Description                          | Default |
|--------------|--------------------------------------|---------|
| `--location` | City, address, or coordinates        | —       |
| `--radius`   | Search radius in kilometers          | 2       |
| `--limit`    | Maximum number of results to return  | 10      |
| `--provider` | Map data provider (`google`, `osm`)  | google  |

### Example Output

```
Searching for newest cafes within 5 km of New York, NY...

1. The Morning Grind — 123 Main St (Opened: Jan 2026) ★ 4.7
2. Bean & Bloom — 456 Oak Ave (Opened: Dec 2025) ★ 4.5
3. Roast Republic — 789 Elm Blvd (Opened: Nov 2025) ★ 4.3
```

## How It Works

1. **Geocoding** — The agent converts the provided location into geographic coordinates.
2. **Area Scan** — It queries the map provider API for cafes within the specified radius.
3. **Data Enrichment** — Each result is enriched with metadata such as opening date, ratings, and reviews.
4. **Ranking** — Results are sorted by opening date (newest first) and returned to the user.

## Project Structure

```
├── agent.py           # Main entry point for the cafe finder agent
├── geocoder.py        # Converts addresses to coordinates
├── scanner.py         # Queries map APIs for cafe data
├── enricher.py        # Enriches results with additional metadata
├── models.py          # Data models for cafe entries
├── config.py          # Configuration and API key management
├── requirements.txt   # Python dependencies
└── README.md
```

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
