import sys
import beer_lambert_lib

def main():
    if len(sys.argv) != 4:
        print("Usage: python main_cli.py <absorbance> <epsilon> <path_length>")
        return

    try:
        a = float(sys.argv[1])
        e = float(sys.argv[2])
        l = float(sys.argv[3])
        
        conc = beer_lambert_lib.calculate_concentration(a, e, l)
        trans = beer_lambert_lib.calculate_transmittance(a)
        
        print(f"Concentration: {conc:.6e} mol/L")
        print(f"Transmittance: {trans:.2f}%")
    except ValueError as err:
        print(f"Error: {err}")

if __name__ == '__main__':
    main()