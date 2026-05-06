import beer_lambert_lib  

def test_concentration():
    # Test Case 1: Standard values
    # A=1, e=1, l=1 -> c=1
    assert beer_lambert_lib.calculate_concentration(1.0, 1.0, 1.0) == 1.0
    
    # Test Case 2: Realistic chemical values
    # A=0.5, e=500, l=1 -> c=0.001
    assert beer_lambert_lib.calculate_concentration(0.5, 500, 1.0) == 0.001

    # Test Case 3: Realistic chemical values
    # A=0.05, e=100, l=1 -> c=0.0005
    assert beer_lambert_lib.calculate_concentration(0.05, 100, 1) == 0.0005
    
    print("All tests for calculating concentration have passed!")

def test_transmittance():
    # Test Case 1:
    # A=0 -> T=100%
    assert beer_lambert_lib.calculate_transmittance(0.0) == 100.0

    # Test Case 2:
    # A=2 -> T=1%
    assert beer_lambert_lib.calculate_transmittance(2.0) == 1.0

    print("All tests for calculating transmittance have passed!")


 
    

if __name__ == "__main__":
    test_concentration()
    test_transmittance()
    

