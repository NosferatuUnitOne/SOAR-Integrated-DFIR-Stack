# Phase 1: Shuffle SOAR Setup

## Goal

Set up Shuffle SOAR as the automation and orchestration component of the DFIR lab.

Shuffle will receive Wazuh alerts through webhooks, process the alert data, perform threat-intelligence enrichment, and forward relevant alerts to TheHive.

## Steps Completed

* Created a dedicated Ubuntu VM for the SOAR and automation stack
* Configured the VM network and confirmed that it was reachable from the local lab
* Installed Docker Engine
* Installed Docker Compose
* Cloned the Shuffle repository
* Started the Shuffle stack
* Verified that Docker created a persistent Shuffle database volume
* Routed Wazuh Stack Logs into Shuffle using Python Script
* Added additional configuration to ossec/yml
* Identified the Shuffle health-check container
* Reviewed container logs during troubleshooting

## Issues Faced

The initial Shuffle deployment only showed the health-check container as running.

The main Shuffle containers, including the frontend, backend, OpenSearch, and Orborus, were not immediately visible in the running container list.

This required checking all containers using:

```bash
sudo docker ps -a
```

instead of only:

```bash
sudo docker ps
```

Another minor issue was entering the incorrect command:

```bash
docker psd
```

The correct command was:

```bash
docker ps
```

## Fixes Applied

* Corrected the Docker command typo
* Used `docker ps -a` to display stopped and failed containers
* Used `docker compose ps` to check the entire Shuffle stack
* Used `docker compose logs` to identify startup errors
* Verified that Docker itself was running correctly
* Confirmed that the Shuffle database volume was created
* Avoided deleting Docker volumes until their purpose was confirmed

## Verification

Checked the Docker service status using:

```bash
sudo systemctl status docker
```

Checked running Shuffle containers using:

```bash
sudo docker ps
```

Checked all containers, including stopped containers, using:

```bash
sudo docker ps -a
```

Checked Shuffle Compose services using:

```bash
sudo docker compose ps
```

Checked the created Docker volumes using:

```bash
sudo docker volume ls
```

Confirmed that the following volume was created:

```text
shuffle_shuffle-database
```

Reviewed Shuffle logs using:

```bash
sudo docker compose logs
```

## What I Learned

* How Docker Compose manages several containers as one application stack
* The difference between `docker ps` and `docker ps -a`
* Why a container showing as running does not always mean the complete application is functional
* How Docker volumes preserve application data
* How container logs are used to troubleshoot failed services
* Why Shuffle is deployed separately from the Wazuh Manager
* How Shuffle will act as the connection between Wazuh, threat intelligence, TheHive, and Velociraptor

## Installing Docker and Docker Compose

Installed Docker and verified that the Docker service was running.

## Cloning and Starting Shuffle

Cloned the Shuffle repository and started the deployment using:

```bash
sudo docker compose up -d
```

## Checking Shuffle Containers

Checked running containers using:

```bash
sudo docker ps
```

Checked failed and stopped containers using:

```bash
sudo docker ps -a
```

## Checking Docker Volumes

Verified that Shuffle persistent storage was created using:

```bash
sudo docker volume ls
```

## Reviewing Shuffle Logs

Reviewed container startup and error messages using:

```bash
sudo docker compose logs
```

## Current Status

Shuffle has been deployed using Docker Compose.

The Docker service, Shuffle health-check container, and persistent database volume have been verified.

The remaining work is to confirm that all Shuffle services are healthy, access the web interface, create the administrator account, and configure the Wazuh webhook workflow.

