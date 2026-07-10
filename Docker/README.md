# Docker Setup

## Goal

Set up Docker as the container runtime for the SOAR and automation components of the DFIR/SOC lab.

Docker will be used to run containerized applications such as Shuffle and its supporting services. This allows the lab to deploy automation tools without manually installing every dependency directly on the Ubuntu VM.

## Steps Completed

* Created a dedicated Ubuntu VM for the SOAR and automation stack
* Updated the Ubuntu package repository
* Installed required packages for Docker setup
* Installed Docker Engine
* Installed Docker Compose
* Started the Docker service
* Enabled Docker to start automatically on boot
* Verified Docker installation using version commands
* Confirmed Docker was running successfully with `systemctl`
* Used Docker Compose to deploy the Shuffle stack
* Verified running containers using `docker ps`
* Checked Docker volumes created by Shuffle
* Identified which containers belonged to Shuffle core services
* Confirmed that extra Shuffle app containers were normal and not separate full applications

## Installation

Updated the Ubuntu VM:

```bash
sudo apt update && sudo apt upgrade -y
```

Installed Docker and Docker Compose:

```bash
sudo apt install -y docker.io docker-compose-v2
```

Started Docker:

```bash
sudo systemctl start docker
```

Enabled Docker on boot:

```bash
sudo systemctl enable docker
```

Verified Docker version:

```bash
docker --version
```

Verified Docker Compose version:

```bash
docker compose version
```

## Docker Role in the Lab

Docker acts as the base container layer for the SOAR side of the lab.

```text
Ubuntu VM
   ↓
Docker Engine
   ↓
Docker Compose
   ↓
Shuffle Containers
   ↓
SOAR Workflow
```

Instead of installing Shuffle manually as a normal application, Docker allows Shuffle to run as a group of containers. This makes the setup easier to manage, restart, and troubleshoot.

## Useful Docker Commands

Check running containers:

```bash
sudo docker ps
```

Check all containers, including stopped containers:

```bash
sudo docker ps -a
```

Check Docker volumes:

```bash
sudo docker volume ls
```

Check logs for a container:

```bash
sudo docker logs <container_name> --tail=100
```

Start containers using Docker Compose:

```bash
sudo docker compose up -d
```

Stop containers using Docker Compose:

```bash
sudo docker compose down
```

## Issues Faced

* Docker Compose package name differed from the expected package name
* Multiple containers appeared after starting Shuffle
* Some Shuffle app containers looked like separate security tools at first
* TheHive was originally tested on the same VM as Shuffle, but the VM became slow
* Docker containers created additional volumes that needed to be identified
* Extra containers from Shuffle made it harder to tell which services were actually part of the core stack

## Fixes Applied

* Installed Docker Compose v2 using the available Ubuntu package
* Used `docker ps` to identify active containers
* Used `docker volume ls` to inspect Docker volumes
* Separated core Shuffle containers from temporary Shuffle app/action containers
* Moved TheHive onto a separate VM to reduce Docker workload and disk I/O pressure
* Used Docker logs to troubleshoot container behavior

## Verification

Docker was verified by checking the Docker service:

```bash
sudo systemctl status docker
```

Docker containers were verified using:

```bash
sudo docker ps
```

Docker volumes were checked using:

```bash
sudo docker volume ls
```

The successful output confirmed that Docker was installed, running, and able to support the Shuffle SOAR stack.

## Lab Status

Docker is installed and functional.

It is currently being used as the container runtime for the SOAR and automation side of the lab, mainly for running Shuffle and its supporting containers.
