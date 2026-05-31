from fastapi.testclient import TestClient
from main_web import app

# Create a test client using your FastAPI app
client = TestClient(app)

def test_get_home_page():
    """Test that the homepage loads correctly."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Beer-Lambert Calculator" in response.text
    assert "<form" in response.text

def test_calculate_success():
    """Test the POST route with valid data."""
    # Sending form data to the /calculate endpoint
    response = client.post(
        "/calculate", 
        data={"a": "0.5", "e": "500", "l": "1.0"}
    )
    
    assert response.status_code == 200
    # Checking if the expected mathematical answers appear in the HTML
    assert "1.000000e-03" in response.text  # Concentration result
    assert "31.62%" in response.text        # Transmittance result

def test_calculate_value_error():
    """Test the POST route with a zero value for epsilon to trigger your business logic error."""
    response = client.post(
        "/calculate", 
        data={"a": "0.5", "e": "0", "l": "1.0"}
    )
    
    assert response.status_code == 200
    # Ensure the business logic's ValueError message bubbles up to the frontend
    assert "Epsilon and path length must be non-zero." in response.text