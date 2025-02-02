import requests  # Import the requests library to make HTTP requests

# Personal access token (replace with your actual token)
# Note: Keep your token secure and avoid sharing it publicly.
token = 'token ghp_XXXXXXXXXX'

# Specify the repository owner and name
owner = 'owner-name'  # Replace 'twbs' with the owner of the Bootstrap repository
repo = 'repo-name'  # Replace 'bootstrap' with the repository name

# Define the GitHub API endpoint for fetching pull requests
url = f'https://api.github.com/repos/{owner}/{repo}/pulls'

# Define the request headers, including the authorization token for API access
headers = {'Authorization': f'token {token}'}

# Make a GET request to the GitHub API to fetch pull request data
response = requests.get(url, headers=headers)

# Check if the API request was successful
if response.status_code == 200:
    # Parse the JSON response to extract pull request data
    pull_requests = response.json()

    # Process the pull request data as needed
    # For example, print the title of each pull request
    for pr in pull_requests:
        print(f"PR Title: {pr['title']}, Created at: {pr['created_at']}")
    print("Success: Pull request data retrieved successfully.")
else:
    # Print an error message if the API request failed
    print(f'Error: {response.status_code} - {response.reason}')
