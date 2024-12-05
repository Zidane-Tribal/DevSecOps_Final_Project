import requests

# GitLab details
access_token = 'glpat-Y6zraHskbJkzQZy4ZrvH'
project_id = '64378460'

# GitLab API URL
url = f"https://gitlab.com/api/v4/projects/64378460/pipelines"

# Set up headers with the access token
headers = {
    'PRIVATE-TOKEN': glpat-Y6zraHskbJkzQZy4ZrvH
}

# Make the request to the API
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Get the pipeline data (latest pipeline)
    pipelines = response.json()
    latest_pipeline = pipelines[0]
    print(f"Pipeline Status: {latest_pipeline['status']}")
    print(f"Pipeline URL: {latest_pipeline['web_url']}")
else:
    print(f"Failed to fetch pipeline data: {response.status_code}")
