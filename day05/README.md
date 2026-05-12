# EPR Radical Signal Analysis

This Python project is designed to analyze Electron Paramagnetic Resonance (EPR) data to detect radical formation. It specifically compares chemical setups (FMN vs. Control) under "Dark" and "Light" conditions across multiple replicates.

## Project Overview
The goal of this assignment is to visualize whether a radical signal appears in the FMN samples after light exposure compared to the control (MQ) samples. The program processes raw CSV files, extracts spectral data, performs baseline correction, and generates a comparative matrix plot.

## File Structure
The project is organized into the following components:

* `analysis.py`: The main script containing the data loading logic, preprocessing, and visualization.
* `tests.py`: A simple test suite to verify that the CSV files are being read correctly.
* `requirements.txt`: List of necessary Python libraries.
* `data`:  Ensure that your CSV file is located in the same folder as your script.
    * *Naming Convention:* `[System]_[Condition]_[Capillary](in).csv`
    * *Example:* `LOV_EDTA_0_1M_FMN_200uM_light_01(in).csv`

## Requirements
The following libraries are required:
* **pandas**: For data manipulation and CSV parsing.
* **matplotlib**: For creating the 2x3 matrix plot.
* **numpy**: For numerical operations.

## How to Run
* Install the required libraries using pip:
   pip install -r requirements.txt
* python analysis.py
This will produce a file named epr_analysis_results.png which contains a 2x3 grid of subplots (Dark vs. Light conditions across 3 capillaries).

## AI Assistant
Gemini https://gemini.google.com/u/1/app?pli=1
* I am working on a Python assignment to analyze EPR (Electron Paramagnetic Resonance) data. I need to determine if radicals are formed in my system by comparing two different chemical setups under "Dark" and "Light" conditions.
* I described how the output looks.
* I described the program requirements
* I described the goal and output request
* Please help me write a test file that performs the following tasks:
    1. Check that all the required files are in the folder where the script is run.
    2. Check that we can open the files and read their contents.
    3. Verify that the data we read is not empty and contains information about the field and the intensity.