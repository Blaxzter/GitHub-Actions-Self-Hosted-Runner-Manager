import os
import time
import docker
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_github_token():
    # Get token from environment variable
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")
    log_message("✓ GitHub token found")
    return token

def get_runner_prefix():
    prefix = os.getenv('RUNNER_PREFIX', 'github-runner')
    log_message(f"Using runner prefix: {prefix}")
    return prefix

def create_runner(client, number, token):
    prefix = get_runner_prefix()
    container_name = f"{prefix}-{number}"
    runner_name = f"{prefix}-{number}"
    
    try:
        log_message(f"🚀 Creating new runner: {container_name}")
        log_message(f"  ├─ Name: {runner_name}")
        log_message(f"  ├─ Organization: {os.getenv('GITHUB_ORG_URL')}")
        
        container = client.containers.run(
            "github-runner:latest",
            detach=True,
            name=container_name,
            environment={
                "GITHUB_TOKEN": token,
                "RUNNER_NAME": runner_name,
                "GITHUB_ORG_URL": os.getenv('GITHUB_ORG_URL')
            },
            volumes={
                "/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "rw"},
                "/actions-cache": {"bind": "/actions-cache", "mode": "rw"}
            },
            restart_policy={"Name": "always"}
        )
        log_message(f"  └─ ✓ Runner container created successfully: {container.short_id}")
    except docker.errors.APIError as e:
        log_message(f"❌ Error creating runner {container_name}: {e}")
        raise

def list_runners(client, prefix):
    runners = client.containers.list(filters={"name": f"{prefix}-"})
    if runners:
        log_message(f"📋 Current runners ({len(runners)}):")
        for runner in runners:
            status = "🟢" if runner.status == "running" else "🔴"
            log_message(f"  {status} {runner.name} ({runner.short_id}) - {runner.status}")
    else:
        log_message("📋 No runners currently running")
    return runners

def main():
    log_message("🎬 Starting GitHub Actions Runner Manager")
    log_message(f"  ├─ Organization: {os.getenv('GITHUB_ORG_URL')}")
    log_message(f"  └─ Desired runners: {os.getenv('DESIRED_RUNNERS', '3')}")
    
    client = docker.from_env()
    prefix = get_runner_prefix()
    
    while True:
        try:
            log_message("\n🔄 Checking runner status...")
            
            # Get desired number of runners from env or config
            desired_runners = int(os.getenv("DESIRED_RUNNERS", 3))
            
            # List and count existing runners
            existing_runners = list_runners(client, prefix)
            existing_count = len(existing_runners)
            
            # Create new runners if needed
            if existing_count < desired_runners:
                runners_to_create = desired_runners - existing_count
                log_message(f"📈 Need to create {runners_to_create} new runner(s)")
                
                for i in range(existing_count + 1, desired_runners + 1):
                    token = get_github_token()
                    create_runner(client, i, token)
            else:
                log_message("✓ Runner count is at desired level")
            
            log_message("💤 Waiting 60 seconds before next check...")
        except Exception as e:
            log_message(f"❌ Error in main loop: {str(e)}")
            log_message("⚠️ Will retry in 60 seconds...")
        
        time.sleep(60)

if __name__ == "__main__":
    main() 