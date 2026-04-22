def calculate_concentration():
    print("--- Beer-Lambert Concentration Calculator ---")
    
    try:
        # Collecting inputs from the user
        # We use float() to ensure the inputs can handle decimals
        absorbance = float(input("Enter the measured absorbance (A): "))
        epsilon = float(input("Enter the molar extinction coefficient (ε) in L/(mol·cm): "))
        path_length = float(input("Enter the path length (l) in cm [usually 1.0]: "))

        # Rearranging the formula: c = A / (ε * l)
        if epsilon == 0 or path_length == 0:
            print("\nError: Epsilon and path length must be non-zero values.")
        else:
            concentration = absorbance / (epsilon * path_length)
            
            # Formatting the output to scientific notation for readability
            print(f"\n--- Results ---")
            print(f"The concentration (c) is: {concentration:.6e} mol/L")

    except ValueError:
        print("\nInput Error: Please enter numerical values only.")

if __name__ == "__main__":
    calculate_concentration()