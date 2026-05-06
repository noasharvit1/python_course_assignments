# Beer-Lambert Law Calculator (v2.0)

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
Compared to the initial script, this version introduces several major improvements:
1. New Feature: Added automatic calculation of Percent Transmittance (%T).
2. Multi-Interface Support: You can run the tool via standard input, command-line arguments, or a modern Graphical User Interface (GUI).

## File Structure
- `beer_lambert_lib.py`: Contains the mathematical functions for concentration and transmittance.
- `main_input.py`: Interactive terminal version.
- `main_cli.py`: Command-line argument version.
- `main_gui.py`: Graphical User Interface (Tkinter).
- `test_beer_lambert.py`: Verification tests.

## How to use
- `main_input.py`-Type python main_input.py in your terminal.
The program will display "Enter absorbance:". You type the value, press Enter, and repeat for the other parameters.
- `main_cli.py`-Type the script name followed by the three values (Absorbance, Epsilon, Path Length) separated by spaces.
Example: main_cli.py 0.5 15000 1.0.
- `main_gui.py`-Type python main_gui.py in your terminal.
A window will appear. Enter your values into the text boxes and click the Calculate button to see the result.

## Requirements
No external libraries are strictly required as it utilizes the built-in math, sys, and tkinter modules.

## AI Interaction
I used Gemini https://gemini.google.com/u/1/app?pli=1

I am currently an MSc student in chemistry, and I am taking a course in Python. I have developed a function that calculates the concentration of a solution using Beer-Lambert's Law. The code performs the calculation in three different ways:

- One version uses standard input (the input function).
- Another version utilizes the command line (the sys.argv list).
- The third version features a graphical user interface (GUI).

Now, I want to add an interesting new feature to my project. I would like to implement part in the code that also calculate the Transmittance (T%) .
accordind to the relation A = 2 - log_{10}(%T) 

Please help me implement this feature. 

## Interaction with other students
I reviewed other students' repositories and opened issues with improvements or suggestions from my perspective.
I received feedback and improved my project.