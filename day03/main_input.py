import beer_lambert_lib

def main():
    try:
        a = float(input("Enter absorbance (A): "))
        e = float(input("Enter molar extinction coefficient (ε): "))
        l = float(input("Enter path length (l): "))
        
        # Calling the library function
        conc = beer_lambert_lib.calculate_concentration(a, e, l)
        print(f"Concentration: {conc:.6e} mol/L")
    except ValueError as err:
        print(f"Input Error: {err}")

if __name__ == '__main__':
    main()