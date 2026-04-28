# Beer-Lambert Concentration Calculator

## Overview
This project is a computational tool designed to calculate the molar concentration of a solution based on the Beer-Lambert Law. The calculation is performed using the following formula: 
**A = εcl**

## Structure
- `beer_lambert_lib.py`: This file contains the logic for the calculation (Shared Library).
- `main_input.py`: Interactive terminal version.
- `main_cli.py`: Command-line argument version.
- `main_gui.py`: Graphical User Interface (Tkinter).
- `test_beer_lambert.py`: Verification tests.
- `Beer_Lambert_law.py`: The initial version of the code.

## How to use
- `main_input.py`-Type python main_input.py in your terminal.
The program will display "Enter absorbance:". You type the value, press Enter, and repeat for the other parameters.
- `main_cli.py`-Type the script name followed by the three values (Absorbance, Epsilon, Path Length) separated by spaces.
Example: main_cli.py 0.5 15000 1.0.
- `main_gui.py`-Type python main_gui.py in your terminal.
A window will appear. Enter your values into the text boxes and click the Calculate button to see the result.


## AI Interaction
I used Gemini https://gemini.google.com/u/1/app?pli=1

I am an MSc student in chemistry, and I am currently taking a course in Python. I wrote a function that calculates the concentration of a solution using Beer-Lambert's Law. I have included the script I wrote in Python.

I would like help implementing the following tasks:

1. Create a Python script that only performs the concentration calculation and call it "beer_lambert_lib." This will serve as the shared library.

2. I need to run the calculation in three different ways using the shared library. Each version should allow for different user interactions:
   - One version that uses standard input (the `input` function).
   - One version that uses the command line (the `sys.argv` list).
   - One version that uses a GUI (you can use Tkinter or another library).
