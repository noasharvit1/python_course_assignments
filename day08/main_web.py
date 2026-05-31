from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import beer_lambert_lib

# Initialize the FastAPI app
app = FastAPI(title="Beer-Lambert Web App")

@app.get("/", response_class=HTMLResponse)
def get_home():
    """
    Serves the main HTML form for user input.
    """
    return """
    <html>
        <head>
            <title>Beer-Lambert Calculator</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 400px; padding: 20px; border: 1px solid #ccc; border-radius: 8px; }
                input { margin-bottom: 10px; width: 100%; padding: 5px; }
                button { padding: 10px; width: 100%; background-color: #007bff; color: white; border: none; cursor: pointer; }
                button:hover { background-color: #0056b3; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Beer-Lambert Calculator</h2>
                <form action="/calculate" method="post">
                    <label>Absorbance (A):</label><br>
                    <input type="text" name="a" required><br>
                    
                    <label>Epsilon (ε):</label><br>
                    <input type="text" name="e" required><br>
                    
                    <label>Path Length (l):</label><br>
                    <input type="text" name="l" required><br>
                    
                    <button type="submit">Calculate</button>
                </form>
            </div>
        </body>
    </html>
    """

@app.post("/calculate", response_class=HTMLResponse)
def calculate_results(
    a: float = Form(...), 
    e: float = Form(...), 
    l: float = Form(...)
):
    """
    Receives form data, uses the business logic to calculate, 
    and returns an HTML page with the results.
    """
    try:
        # Utilizing the exact same business logic from your library
        conc = beer_lambert_lib.calculate_concentration(a, e, l)
        trans = beer_lambert_lib.calculate_transmittance(a)
        
        return f"""
        <html>
            <head><title>Results</title></head>
            <body style="font-family: Arial, sans-serif; margin: 40px;">
                <h2>Calculation Results</h2>
                <p><strong>Concentration (c):</strong> {conc:.6e} mol/L</p>
                <p><strong>Transmittance (%T):</strong> {trans:.2f}%</p>
                <br>
                <a href="/">← Go Back</a>
            </body>
        </html>
        """
    except ValueError as err:
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; margin: 40px; color: red;">
                <h2>Input Error</h2>
                <p>{err}</p>
                <a href="/">← Try Again</a>
            </body>
        </html>
        """