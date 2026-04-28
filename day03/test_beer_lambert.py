from beer_lambert_lib import calculate_concentration

def test_logic():
    # Test Case 1: Standard values
    # A=1, e=1, l=1 -> c=1
    assert calculate_concentration(1.0, 1.0, 1.0) == 1.0
    
    # Test Case 2: Realistic chemical values
    # A=0.5, e=500, l=1 -> c=0.001
    assert calculate_concentration(0.5, 500, 1.0) == 0.001

    # Test Case 3: Realistic chemical values
    # A=0.05, e=100, l=1 -> c=0.0005
    assert calculate_concentration(0.05, 100, 1) == 0.0005
    
    print("All tests passed!")

if __name__ == "__main__":
    test_logic()