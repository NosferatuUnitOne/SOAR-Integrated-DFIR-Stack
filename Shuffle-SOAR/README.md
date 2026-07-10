# Shuffle SOAR Setup

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
* Routed Wazuh Stack Logs into Shuffle using Python Script
* Added additional configuration to ossec/yml
* Connected both Wazuh Stack Log pipline to Shuffle Via Webhook
* Opened Shuffle UI to configure New Log Pipline Test
* Ran a simple SSH Failed log in Attempt to Test Shuffle Output

## Issues Faced

* Resourse Restriction and Limitation: was not able to configure both Shuffle and The Hive within a single VM

## Fixes Applied

Moved Shuffle to a new VM Dedicated to its servies alone

## Verification

Had setup the new VM and ensured that it was configured in a Bridged Adaptor in order for it to be accessible to the Local Network

![Pinged VM](./PingedVM.png)

Downloaded Shuffle and configured it all into a Docker container or Docker Compose as a standard setup

![Git Shuffle](./GITSHUFFLE.png)

![Docker Compose](./Dockerup.png)

![Docker Compose](./Dockerps.png)

## Shuffle UI

![Shuffle](./ShuffleUI.png)



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

