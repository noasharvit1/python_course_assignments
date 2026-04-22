# Beer-Lambert Law Concentration Calculator

## Description
I wrote a Python program for my laboratory to determine the concentration of a chemical solution using UV-Vis spectroscopy data based on the **Beer-Lambert law**. The program returns the concentration in mol/L in scientific notation using e notation, with a precision of six decimal places.

The formula used is:
**A = εcl**

**c = A / (εl)**

## How to Use
1. Run the script using Python
2. Enter the **Absorbance** measured by your spectrophotometer.
3. Enter the **Molar Extinction Coefficient** (specific to your molecule and wavelength).
4. Enter the **Path Length** of your cuvette (standard is 1 cm).
5. The program will output the concentration in Molar (mol/L) units.


## Example to Use
Suppose you measured an absorbance of 0.5, the molar extinction coefficient is 15 L/(mol·cm), and a standard 1 cm cuvette is being used.
c = A / (εl) = 0.5 / (15*1) = 0.033333 mol/L = 3.333333e-02 mol/L


## AI Use
Gemini
"I am an M.Sc. student in chemistry at the Weizmann Institute of Science, and I am taking a course in Python. 

I have been assigned a task to come up with a well-known scientific calculation from my field. The objective is to write a program that takes input from the user and performs the necessary computations. 

Please help me write a Python script that implements the Beer-Lambert law to calculate the concentration of a solution based on the absorption in UV."
