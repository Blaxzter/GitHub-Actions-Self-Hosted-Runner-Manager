# GitHub Actions Self-Hosted Runner Manager

This project provides a Docker-based solution for managing self-hosted GitHub Actions runners. It automatically maintains a pool of runners for your GitHub organization, with features like auto-scaling, persistent build caching, and easy configuration.

## Features

- 🔄 Automatic runner management
- 🏷️ Configurable runner naming with prefixes
- 📦 Persistent Docker build cache for faster Actions
- 🔑 Secure token management
- 🎛️ Configurable number of concurrent runners
- 🐳 Fully Dockerized solution
- 🧹 Automatic runner cleanup on shutdown

## Prerequisites

- Docker and Docker Compose
- GitHub Organization admin access (to generate runner tokens)
- Linux host (recommended) or Windows with WSL2

## Quick Start

1. Clone the repository:

   ```bash
   git clone <your-repo>
   cd runners
   ```

2. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

3. Configure your environment:

   - Get a GitHub runner token from your organization's settings:
     - Go to your GitHub organization
     - Settings → Actions → Runners
     - Click "New runner"
     - Copy the provided token
   - Edit `.env` with your settings:
     ```env
     GITHUB_TOKEN=your_token_here
     GITHUB_ORG_URL=https://github.com/your-org
     DESIRED_RUNNERS=3
     RUNNER_PREFIX=your-prefix
     ```

4. Start the runner manager:
   ```bash
   docker-compose build
   docker-compose up -d agent
   ```

## Configuration

### Environment Variables

| Variable          | Description                      | Default       |
| ----------------- | -------------------------------- | ------------- |
| `GITHUB_TOKEN`    | GitHub runner registration token | Required      |
| `GITHUB_ORG_URL`  | Your GitHub organization URL     | Required      |
| `DESIRED_RUNNERS` | Number of runners to maintain    | 3             |
| `RUNNER_VERSION`  | GitHub runner version            | 2.322.0       |
| `RUNNER_PREFIX`   | Prefix for runner names          | github-runner |

### Build Cache

The system maintains a persistent Docker build cache at `/actions-cache` to speed up your GitHub Actions workflows. This cache is shared across all runners and persists even when runners are recreated.

To optimize your workflows to use this cache, add these parameters to your workflow's Docker build steps:

```yaml
- name: Build
  uses: docker/build-push-action@v4
  with:
    context: .
    push: true
    tags: your-image:tag
    cache-from: type=local,src=/actions-cache
    cache-to: type=local,dest=/actions-cache,mode=max
```

## Architecture

The system consists of two main components:

1. **Agent** (`agent/`):

   - Python service that manages the runner lifecycle
   - Monitors runner count and creates new runners as needed
   - Handles runner registration and cleanup

2. **Runner** (`runner/`):
   - Base Docker image for GitHub Actions runners
   - Includes common tools and Docker support
   - Automatically registers with GitHub on startup
   - Handles graceful deregistration on shutdown

## Runner Management

### Starting Runners

To start or scale up runners:

```bash
# Start with default number of runners
docker-compose up -d agent

# Or scale to a specific number
DESIRED_RUNNERS=5 docker-compose up -d agent
```

### Stopping Runners

The runners are configured to automatically deregister from GitHub when stopped:

```bash
# Stop all runners and the agent
docker-compose down

# Or stop specific runners
docker stop <runner-container-name>
```

### Removing Runners

Runners will automatically remove themselves from GitHub in these cases:

- When the container is stopped gracefully
- When the docker-compose stack is brought down
- When the agent scales down the number of desired runners

If you need to manually remove a runner from GitHub:

1. Stop the runner container:
   ```bash
   docker stop <runner-container-name>
   ```
2. The runner will automatically deregister itself during shutdown

If a runner container was not stopped gracefully and needs cleanup:

1. Go to your GitHub organization
2. Settings → Actions → Runners
3. Find the offline runner
4. Click the ⋮ menu and select "Remove"

## Maintenance

### Updating Runner Version

To update the GitHub Actions runner version:

1. Check the latest version at [actions/runner releases](https://github.com/actions/runner/releases)
2. Update `RUNNER_VERSION` in your `.env` file
3. Rebuild and restart:
   ```bash
   docker-compose build
   docker-compose up -d agent
   ```

### Logs

View runner manager logs:

```bash
docker-compose logs -f agent
```

View individual runner logs:

```bash
docker logs <runner-container-name>
```

## Troubleshooting

1. **Runners not starting:**

   - Check agent logs: `docker-compose logs agent`
   - Verify GitHub token is valid
   - Ensure Docker socket is accessible

2. **Build cache not working:**

   - Verify the `/actions-cache` volume is mounted
   - Check runner has write permissions to cache directory
   - Ensure workflow is configured to use local cache

3. **Runner registration fails:**

   - Verify organization URL is correct
   - Check token permissions and expiration
   - Review runner logs for detailed error messages

4. **Runner not removing itself:**
   - Check if the container was stopped gracefully
   - Verify the token has remove permissions
   - Remove manually from GitHub UI if needed

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
