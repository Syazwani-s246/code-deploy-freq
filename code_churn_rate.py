import subprocess
import pandas as pd
import os
from scipy.stats import pearsonr

# Paths
repo_path = r"C:\Path\To\Your\Repo"
output_path = r"C:\Path\To\Your\Output\release_analysis_with_correlations_v1.xlsx"

# Use to check tag actual name
# cd "C:\Users\Lenovo\Desktop\RA-DevOps Material\GitHub Repo\junit5"
# git tag

# List of releases to analyze
releases = ["v1.0.0", "v1.1.0", "v1.2.0", "v1.3.0", "v2.0.0", "v2.1.0", "v2.2.0", "v2.3.0", "v3.0.0"]


# Function to get git statistics
def get_git_stats(repo_path, release_name):
    try:
        result = subprocess.run(
            ['git', 'log', '--shortstat', '--oneline', release_name],
            cwd=repo_path,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode != 0 or not result.stdout:
            print(f"No git stats found for release {release_name}.")
            return None

        output = result.stdout.splitlines()
        commit_count, total_files_changed, total_lines_added, total_lines_deleted = 0, 0, 0, 0

        for line in output:
            if "files changed" in line or "file changed" in line:
                commit_count += 1
                parts = line.split(',')
                files_changed = int(parts[0].split()[0])
                lines_added = int(parts[1].split()[0]) if "insertions(+)" in parts[1] else 0
                lines_deleted = int(parts[2].split()[0]) if len(parts) > 2 and "deletions(-)" in parts[2] else 0

                total_files_changed += files_changed
                total_lines_added += lines_added
                total_lines_deleted += lines_deleted

        return {
            "Release Name": release_name,
            "Commits": commit_count,
            "File Changes": total_files_changed,
            "Code Added": total_lines_added,
            "Code Deleted": total_lines_deleted,
        }
    except Exception as e:
        print(f"Error while getting git stats for release {release_name}: {e}")
        return None

# Function to run Lizard and extract function count
def run_lizard(repo_path, release_name):
    try:
        result = subprocess.run(
            ['lizard', repo_path],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode != 0 or not result.stdout:
            print(f"No Lizard output for release {release_name}.")
            return 0

        # Parse function count from summary
        for line in result.stdout.splitlines():
            if line.startswith("Total nloc"):
                parts = line.split()
                return int(parts[4])  # Fun Cnt is the 5th field in the summary
        return 0
    except Exception as e:
        print(f"Error while running Lizard for release {release_name}: {e}")
        return 0

# Collect data for all releases
data = []
for release in releases:
    print(f"Processing release: {release}")
    try:
        subprocess.run(['git', 'checkout', release], cwd=repo_path, check=True, encoding='utf-8')
        git_stats = get_git_stats(repo_path, release)
        if git_stats:
            function_count = run_lizard(repo_path, release)
            git_stats["Function Count"] = function_count
            data.append(git_stats)
    except subprocess.CalledProcessError as e:
        print(f"Error processing release {release}: {e}")

# Create a DataFrame
df = pd.DataFrame(data)

# Calculate Pearson Correlation for all releases (global conclusion)
if not df.empty:
    correlation, p_value = pearsonr(df["Function Count"], df["Commits"])
    conclusion = f"The Pearson correlation coefficient is {correlation:.4f}, indicating a {'strong' if abs(correlation) > 0.7 else 'moderate'} positive correlation."

    print(conclusion)  # Print in the console

    # Save conclusion and data to Excel
    with pd.ExcelWriter(output_path) as writer:
        df.to_excel(writer, index=False, sheet_name="Release Data")
        conclusion_df = pd.DataFrame({"Conclusion": [conclusion]})
        conclusion_df.to_excel(writer, index=False, sheet_name="Conclusion")

    print(f"Analysis and conclusion saved to {output_path}")
else:
    print("No data to analyze. Please check the script and data.")
