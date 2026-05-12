import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_epr_data(filename):
    """
    Loads EPR data from a semicolon-separated CSV file.
    Automatically identifies the start of the data section by searching for the header.
    """
    if not os.path.exists(filename):
        return None
    
    # Using latin1 encoding as lab CSVs often come from Windows systems
    with open(filename, 'r', encoding='latin1') as f:
        lines = f.readlines()
    
    header_idx = -1
    for i, line in enumerate(lines):
        if 'BField' in line:
            header_idx = i
            break
            
    if header_idx == -1:
        print(f"Warning: Could not find data header in {filename}")
        return None
    
    # Load data, selecting only the first two columns (Magnetic Field and Intensity)
    df = pd.read_csv(filename, sep=';', skiprows=header_idx)
    df = df.iloc[:, :2] 
    df.columns = ['Field', 'Intensity']
    
    # Convert to numeric and drop potential empty rows
    df['Field'] = pd.to_numeric(df['Field'], errors='coerce')
    df['Intensity'] = pd.to_numeric(df['Intensity'], errors='coerce')
    df.dropna(inplace=True)
    
    return df

def generate_matrix_plot(output_name='epr_analysis_results.png'):
    """
    Creates a 2x3 grid of EPR spectra overlaying MQ and FMN samples.
    """
    systems = {
        'Control (MQ)': 'LOV_EDTA_0_1M',
        'FMN Experimental': 'LOV_EDTA_0_1M_FMN_200uM'
    }
    conditions = ['dark', 'light']
    capillaries = ['01', '02', '03']
    colors = {'Control (MQ)': 'gray', 'FMN Experimental': 'blue'}

    fig, axes = plt.subplots(2, 3, figsize=(15, 10), sharex=True)

    for row_idx, cond in enumerate(conditions):
        for col_idx, cap in enumerate(capillaries):
            ax = axes[row_idx, col_idx]
            
            found_any = False
            for label, prefix in systems.items():
                # Filename pattern: System_Condition_Capillary(in).csv
                filename = f"{prefix}_{cond}_{cap}(in).csv"
                data = load_epr_data(filename)
                
                if data is not None:
                    # Baseline correction: subtract the mean of the first 50 points
                    baseline = data['Intensity'].iloc[:50].mean()
                    ax.plot(data['Field'], data['Intensity'] - baseline, 
                            label=label, color=colors[label], lw=1.5, alpha=0.8)
                    found_any = True
            
            # Formatting
            ax.set_title(f"Capillary {cap} - {cond.capitalize()}", fontsize=12, fontweight='bold')
            if row_idx == 1:
                ax.set_xlabel('Magnetic Field [mT]')
            if col_idx == 0:
                ax.set_ylabel('Intensity (Baseline Corrected)')
            
            if found_any:
                ax.legend(loc='upper right', fontsize='small')
                ax.grid(True, linestyle=':', alpha=0.6)
            else:
                ax.text(0.5, 0.5, 'Data File Missing', ha='center', va='center', transform=ax.transAxes, color='red')

    plt.suptitle('EPR Radical Signal Analysis: LOV EDTA System', fontsize=16, y=0.98)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(output_name, dpi=300)
    print(f"Analysis complete. Plot saved as {output_name}")

if __name__ == "__main__":
    generate_matrix_plot()