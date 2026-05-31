import beer_lambert_lib

def main():
    try:
        a = float(input("Enter absorbance (A): "))
        e = float(input("Enter molar extinction coefficient (ε): "))
        l = float(input("Enter path length (l): "))
        
        conc = beer_lambert_lib.calculate_concentration(a, e, l)
        trans = beer_lambert_lib.calculate_transmittance(a) # New calculation
        
        print(f"Concentration: {conc:.6e} mol/L")
        print(f"Transmittance: {trans:.2f}%") # New output
    except ValueError as err:
        print(f"Input Error: {err}")

if __name__ == '__main__':
    main()