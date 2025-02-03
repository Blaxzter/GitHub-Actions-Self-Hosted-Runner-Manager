import os
import time
import docker
import requests
from dotenv import load_dotenv

load_dotenv()

def get_github_token():
    # Get token from environment variable
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")
    return token

def get_runner_prefix():
    return os.getenv('RUNNER_PREFIX', 'github-runner')

def create_runner(client, number, token):
    prefix = get_runner_prefix()
    container_name = f"{prefix}-{number}"
    runner_name = f"{prefix}-{number}"
    
    try:
        client.containers.run(
            "github-runner:latest",
            detach=True,
            name=container_name,
            environment={
                "GITHUB_TOKEN": token,
                "RUNNER_NAME": runner_name,
                "GITHUB_ORG_URL": os.getenv('GITHUB_ORG_URL')
            },
            volumes={
                "/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "rw"}
            },
            restart_policy={"Name": "always"}
        )
        print(f"Created runner {container_name}")
    except docker.errors.APIError as e:
        print(f"Error creating runner {container_name}: {e}")

def main():
    client = docker.from_env()
    prefix = get_runner_prefix()
    
    while True:
        # Get desired number of runners from env or config
        desired_runners = int(os.getenv("DESIRED_RUNNERS", 3))
        
        # Count existing runners
        existing_runners = len(client.containers.list(
            filters={"name": f"{prefix}-"}
        ))
        
        # Create new runners if needed
        if existing_runners < desired_runners:
            for i in range(existing_runners + 1, desired_runners + 1):
                token = get_github_token()
                create_runner(client, i, token)
        
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main() 