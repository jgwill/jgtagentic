---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Designing the Process

+++

## Repo links

* [jgwill/jgtatsa](https://github.com/jgwill/jgtatsa/issues)
* [jgwill/jgtd](https://github.com/jgwill/jgtd/issues)
* [issue #25 - fx::Trading Session Assistance](https://github.com/jgwill/jgtd/issues/25)

## Objectives

We aim to create an efficient trading session assistance system that manages entry orders, detects when they become trades, and updates the Jupyter Book configuration accordingly. The system will also provide visual analysis tools and allow for the activation of exit strategies based on predefined criteria.

## Structure

### Data Management

- **Data Files**: Store data files (e.g., JSON, YAML) in a dedicated directory within the Jupyter Book structure.
- **Configuration Files**: Maintain configuration files in the Jupyter Book directory and ensure they are updated when entry orders become trades.

### Entry Orders

- **Detection**: Implement a mechanism to detect when an entry order becomes a trade.
- **Cancellation**: Automatically cancel invalid entry orders.

### Visual Analysis

- **Charts**: Use JGTADS from jgtpy to create charts for visual analysis.
- **Updates**: Ensure the Jupyter Book updates visually to reflect the latest data and analysis.

### Exit Strategies

- **Activation**: Allow for the activation of exit strategies based on analysis.
- **Trailing**: Choose to trail the lips, teeth, or jaw of the Alligator indicator.
- **FDB Signal**: Option to exit on an FDB signal.
- **Configuration Update**: Update the `_config.yml` file to reflect active exit strategies.

## Implementation Steps

1. **Organize Data and Configuration Files**
   - Create a `data` directory within the Jupyter Book structure.
   - Move existing data and configuration files to the appropriate directories.

2. **Detect Entry Orders Becoming Trades**
   - Implement a script to monitor entry orders and detect when they become trades.
   - Update the `_config.yml` file when an entry order becomes a trade.

3. **Visual Analysis Tools**
   - Integrate JGTADS from jgtpy to create charts.
   - Ensure the Jupyter Book updates with the latest visual analysis.

4. **Activate Exit Strategies**
   - Implement functionality to activate exit strategies based on analysis.
   - Update the `_config.yml` file to reflect active exit strategies.

5. **Build and Serve the Jupyter Book**
   - Use Jupyter Book commands to build and serve the book.
   - Ensure the book is visually effective for analysis.

## Further Action

- **Develop Scripts**: Create scripts to automate the detection of trades and update the configuration.
- **Integrate Visual Tools**: Ensure JGTADS charts are integrated and updated in the Jupyter Book.
- **Test and Iterate**: Continuously test the system and iterate based on feedback and analysis.
