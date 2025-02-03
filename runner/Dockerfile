# syntax=docker/dockerfile:1.4
FROM ubuntu:22.04

# Set default runner version
ARG RUNNER_VERSION=2.321.0

# Install required packages
RUN apt-get update && apt-get install -y \
    curl \
    sudo \
    git \
    jq \
    docker.io \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Create runner user
RUN useradd -m runner && \
    usermod -aG sudo runner && \
    usermod -aG docker runner && \
    echo "runner ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Create cache directory
RUN mkdir -p /actions-cache && \
    chown -R runner:runner /actions-cache

WORKDIR /home/runner

USER runner

# Download and install GitHub runner
RUN curl -o actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz -L https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz && \
    tar xzf ./actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz && \
    rm actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz

COPY --chown=runner:runner start.sh .
RUN sudo chmod +x start.sh

ENTRYPOINT ["./start.sh"] 