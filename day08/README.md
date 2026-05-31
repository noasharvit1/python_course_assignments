# Beer-Lambert Law Calculator (v3.0)

## Overview
This project is a versatile Python-based computational tool designed for chemistry students and researchers. It calculates both the Molar Concentration (c) and the Percent Transmittance (%T) of a solution based on the Beer-Lambert Law.

The Physics Behind it:
1. *Concentration:* Calculated using the formula A = εcl
units:
A = unitless
ε = M^-1 * cm^-1
C = M 
l = cm
2. *Transmittance:* Calculated from Absorbance (A) using the logarithmic relationship:%T = 10^(2 - A)

## What's New in This Version?
Compared to the previous versions, this update introduces a modern Web Application:
1. **Web Interface:** A responsive, browser-based user interface built with FastAPI.
2. **Web Testing:** Automated tests for the web application endpoints using FastAPI's `TestClient` and `pytest`.
3. **Environment Management:** Transitioned to using a `requirements.txt` file for easy setup and virtual environment management.

## File Structure
- `beer_lambert_lib.py`: Core "business logic" containing mathematical functions for concentration and transmittance.
- `main_web.py`: **[NEW]** FastAPI web application server and routes.
- `test_web.py`: **[NEW]** Verification tests for the web application endpoints.
- `requirements.txt`: **[NEW]** List of Python package dependencies.
- `main_input.py`: Interactive terminal version.
- `main_cli.py`: Command-line argument version.
- `main_gui.py`: Desktop Graphical User Interface (Tkinter).
- `test_beer_lambert.py`: Verification tests for the core business logic.           

## How to use
1. **install required packages:**
pip install -r requirements.txt

2. **Web Application (FastAPI) - Recommended**
- Start the server by typing: uvicorn main_web:app --reload
- Open your web browser and go to: http://127.0.0.1:8000
- Fill in the form and click "Calculate".

3. **Standard Input Version**
Type python main_input.py in your terminal.

The program will prompt you to enter the absorbance, epsilon, and path length interactively.

4. **Command-Line Version (CLI)**
Type the script name followed by the three values separated by spaces.

Example: python main_cli.py 0.5 15000 1.0

5. **Desktop GUI Version (Tkinter)***
Type python main_gui.py in your terminal.

A desktop window will appear. Enter your values into the text boxes and click the Calculate button.

## Running Tests
To ensure the math logic and web routes are functioning correctly, you can run the test files using pytest. 

To test the web app: pytest test_web.py -v

To test the core logic: pytest test_beer_lambert.py -v
## Requirements
No external libraries are strictly required as it utilizes the built-in math, sys, and tkinter modules.

## AI Interaction
I used Gemini https://gemini.google.com/u/1/app?pli=1

"I'm currently an MSc student in chemistry, and I'm taking a course in Python. I received the following task:

Choose one of your projects so far that includes a "business logic" component that is tested.

Develop a web application for this project. While you can use Flask, it would be preferable to utilize one of the other web frameworks in Python.

Ensure that the web application uses the same "business logic" functions as your original project.

Write test cases for the web application as well.

I uploaded one of the tasks I completed during the semester - a program that uses the Beer-Lambert Law to calculate the concentration of a solution based on the UV absorption of that solution. 

Please help me implement the task using this project."



