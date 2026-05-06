def calculate_concentration(absorbance, epsilon, path_length):
    """
    Calculates the concentration (c) using Beer-Lambert's Law: A = ε * l * c
    Rearranged: c = A / (ε * l)
    """
    if epsilon == 0 or path_length == 0:
        raise ValueError("Epsilon and path length must be non-zero.")
    
    return absorbance / (epsilon * path_length)

def calculate_transmittance(absorbance):
    """
    Calculates Percent Transmittance (%T) from Absorbance (A).
    Formula: %T = 10^(2 - A)
    """
    return 10 ** (2 - absorbance)