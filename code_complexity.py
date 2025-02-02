import subprocess
import pandas as pd
import os

# Path to the repository
repo_path = r"C:\Path\To\Your\Repo"
output_path = r"C:\Path\To\Your\Output\lizard_output.xlsx"


# List of releases to analyze
releases = ["v1.0.0", "v1.1.0", "v1.2.0", "v1.3.0", "v2.0.0", "v2.1.0", "v2.2.0", "v2.3.0", "v3.0.0"]

# Function to run lizard and extract the summary
def run_lizard(repo_path, release_name):
    result = subprocess.run(['lizard', repo_path], capture_output=True, text=True)
    output = result.stdout.splitlines()

    # Parse summary section
    summary_start = False
    summary_data = []
    for line in output:
        if "Total nloc" in line:  # Start of the summary section
            summary_start = True
        elif summary_start and line.strip():  # Summary lines
            parts = line.split()
            if len(parts) == 8:  # Ensure it's a valid summary line
                summary_data.append(parts)

    if summary_data:
        # Extract the last valid summary
        last_summary = summary_data[-1]
        return {
            "Release Name": release_name,
            "Total NLOC": int(last_summary[0]),
            "Avg. NLOC": float(last_summary[1]),
            "Avg. CCN": float(last_summary[2]),
            "Avg. Token": float(last_summary[3]),
            "Fun Cnt": int(last_summary[4]),
            "Warning Cnt": int(last_summary[5]),
            "Fun Rt": float(last_summary[6]),
            "NLOC Rt": float(last_summary[7])
        }
    return None

# Initialize a list to store all summary data
all_data = []

# Checkout each release, run lizard, and collect results
for release in releases:
    try:
        print(f"Checking out release: {release}")
        subprocess.run(['git', 'checkout', release], cwd=repo_path, check=True)

        print(f"Running Lizard on release: {release}")
        summary = run_lizard(repo_path, release)

        if summary:
            all_data.append(summary)
        else:
            print(f"No summary data found for release: {release}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing release {release}: {e}")
        continue

# Convert all data to a DataFrame
if all_data:
    df_all = pd.DataFrame(all_data)
    df_all.to_excel(output_path, index=False)
    print(f"Lizard output saved to {output_path}")
else:
    print("No data was collected. Please check the lizard output and script logic.")
