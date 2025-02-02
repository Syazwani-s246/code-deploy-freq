import requests
from datetime import datetime, timedelta
import pandas as pd


def fetch_all_releases(repo):
    releases = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{repo}/releases?page={page}&per_page=100"
        headers = {"Authorization": "token ghp_XXXXXXXXXX"}
        response = requests.get(url, headers=headers)
        if response.status_code == 403:  # Check if rate limit is hit
            print("Rate limit exceeded. Please try again later.")
            break
        data = response.json()
        if not data:
            break
        releases.extend(data)
        page += 1
        print(f"Fetched page {page} of releases")
    return releases


# Define the repository
repository = "repo-owner-name/repo-name"


# Fetch all releases for the repository
all_releases = fetch_all_releases(repository)


# Extract release information
# releases_info = [(release['name'], release['published_at']) for release in all_releases]
releases_info = [
    (release['name'], release['published_at'])
    for release in all_releases if not release['prerelease'] and not release['draft']
]


df_releases_info = pd.DataFrame(releases_info, columns=['Release Name', 'Published At'])


# Convert published timestamps to datetime and remove timezone information
df_releases_info['Published At'] = pd.to_datetime(df_releases_info['Published At']).dt.tz_localize(None)


# Calculate number of code releases per time unit
df_releases_info['Day'] = df_releases_info['Published At'].dt.date
df_releases_info['Week'] = df_releases_info['Published At'].dt.to_period('W').astype(str)
df_releases_info['Month'] = df_releases_info['Published At'].dt.to_period('M').astype(str)


daily_releases = df_releases_info.groupby('Day').size().reset_index(name='Release Count')
weekly_releases = df_releases_info.groupby('Week').size().reset_index(name='Release Count')
monthly_releases = df_releases_info.groupby('Month').size().reset_index(name='Release Count')


# Save the results to an Excel file
with pd.ExcelWriter('file-name.xlsx') as writer:
    df_releases_info.to_excel(writer, sheet_name='Release Information', index=False)
    daily_releases.to_excel(writer, sheet_name='Daily Releases', index=False)
    weekly_releases.to_excel(writer, sheet_name='Weekly Releases', index=False)
    monthly_releases.to_excel(writer, sheet_name='Monthly Releases', index=False)


print("Data has been written to 'file-name.xlsx'")
