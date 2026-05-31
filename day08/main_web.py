from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import beer_lambert_lib

# Initialize the FastAPI app
app = FastAPI(title="Beer-Lambert Web App")

@app.get("/", response_class=HTMLResponse)
def get_home():
    """
    Serves the beautiful, modern HTML form for user input.
    """
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Beer-Lambert Calculator</title>
            <style>
                /* Background and font setup */
                body {
                    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                    background-color: #f0f2f5;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                /* The main white card */
                .container {
                    background-color: #ffffff;
                    padding: 40px;
                    border-radius: 12px;
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
                    width: 100%;
                    max-width: 350px;
                }
                h2 {
                    color: #1a1a1a;
                    text-align: center;
                    margin-top: 0;
                    margin-bottom: 25px;
                    font-weight: 600;
                }
                label {
                    font-weight: 500;
                    color: #444;
                    display: inline-block;
                    margin-bottom: 8px;
                }
                .unit {
                    font-size: 0.85em;
                    color: #888;
                    font-weight: normal;
                }
                /* Styling the input boxes */
                input[type="text"] {
                    width: 100%;
                    padding: 12px;
                    margin-bottom: 20px;
                    border: 1px solid #ccd0d5;
                    border-radius: 6px;
                    box-sizing: border-box;
                    font-size: 16px;
                    transition: border-color 0.3s, box-shadow 0.3s;
                }
                /* The blue glow when you click inside a box */
                input[type="text"]:focus {
                    border-color: #007bff;
                    outline: none;
                    box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.2);
                }
                /* The beautiful submit button */
                button {
                    width: 100%;
                    padding: 14px;
                    background-color: #007bff;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: background-color 0.3s, transform 0.1s;
                }
                button:hover {
                    background-color: #0056b3;
                }
                button:active {
                    transform: scale(0.98);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Beer-Lambert Calculator</h2>
                <form action="/calculate" method="post">
                    
                    <label>Absorbance (A) <span class="unit">[Unitless]</span></label>
                    <input type="text" name="a" required placeholder="e.g., 0.5">
                    
                    <label>Epsilon (ε) <span class="unit">[M<sup>-1</sup> cm<sup>-1</sup>]</span></label>
                    <input type="text" name="e" required placeholder="e.g., 500">
                    
                    <label>Path Length (l) <span class="unit">[cm]</span></label>
                    <input type="text" name="l" required placeholder="e.g., 1.0">
                    
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
    Receives form data, calculates, and returns a beautiful HTML page with the results.
    """
    try:
        conc = beer_lambert_lib.calculate_concentration(a, e, l)
        trans = beer_lambert_lib.calculate_transmittance(a)
        
        # A matching beautiful results page
        return f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Results</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                        background-color: #f0f2f5;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }}
                    .container {{
                        background-color: #ffffff;
                        padding: 40px;
                        border-radius: 12px;
                        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
                        width: 100%;
                        max-width: 350px;
                    }}
                    h2 {{ color: #1a1a1a; text-align: center; margin-top: 0; border-bottom: 1px solid #eee; padding-bottom: 15px; }}
                    .result-box {{
                        background-color: #e9f7ef;
                        border-left: 4px solid #28a745;
                        padding: 15px;
                        margin-bottom: 15px;
                        border-radius: 4px;
                    }}
                    .label {{ color: #555; font-size: 0.9em; }}
                    .value {{ font-size: 1.2em; font-weight: bold; color: #2c3e50; margin-top: 5px; }}
                    a.button {{
                        display: block;
                        text-align: center;
                        width: calc(100% - 28px);
                        padding: 14px;
                        margin-top: 25px;
                        background-color: #6c757d;
                        color: white;
                        text-decoration: none;
                        border-radius: 6px;
                        font-weight: 600;
                        transition: background-color 0.3s;
                    }}
                    a.button:hover {{ background-color: #5a6268; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Calculation Results</h2>
                    
                    <div class="result-box">
                        <div class="label">Concentration (c):</div>
                        <div class="value">{conc:.6e} <span style="font-size: 0.8em; font-weight: normal; color: #666;">mol/L</span></div>
                    </div>
                    
                    <div class="result-box" style="background-color: #e3f2fd; border-left-color: #007bff;">
                        <div class="label">Transmittance (%T):</div>
                        <div class="value">{trans:.2f}%</div>
                    </div>
                    
                    <a href="/" class="button">← Calculate Again</a>
                </div>
            </body>
        </html>
        """
    except ValueError as err:
        # Error page styling
        return f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Error</title>
                <style>
                    body {{ font-family: 'Segoe UI', sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; }}
                    .container {{ background-color: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center; }}
                    h2 {{ color: #dc3545; }}
                    a {{ display: inline-block; margin-top: 20px; color: #007bff; text-decoration: none; font-weight: bold; }}
                    a:hover {{ text-decoration: underline; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Input Error</h2>
                    <p style="color: #666;">{err}</p>
                    <a href="/">← Try Again</a>
                </div>
            </body>
        </html>
        """