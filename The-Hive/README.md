# TheHive Setup

## Goal

Set up TheHive as the alert and case management component of the DFIR/SOC lab.

TheHive will receive alerts from Shuffle, store them under the `OmarSOC` organization, and provide an analyst-facing interface for reviewing alerts and preparing future incident response workflows.

## Steps Completed

* Created a dedicated Ubuntu VM for TheHive
* Configured the VM network and confirmed that it was reachable from the local lab
* Installed Docker Engine
* Installed Docker Compose
* Created a Docker Compose setup for TheHive
* Deployed TheHive with its supporting services
* Opened TheHive UI through the browser
* Created the `OmarSOC` organization
* Created a normal user for analyst access
* Created a service user for Shuffle API access
* Generated an API key for the Shuffle service user
* Connected Shuffle to TheHive using the API key
* Verified TheHive web access from the Shuffle VM
* Tested TheHive API authentication using `curl`
* Tested direct alert creation using TheHive API
* Confirmed Shuffle-created alerts appeared in TheHive
* Used TheHive as the final alert queue for Wazuh alerts routed through Shuffle

## Deployment

TheHive was deployed on a separate Ubuntu VM.

The original plan was to run TheHive on the same VM as Shuffle, but the VM became slow due to heavy disk I/O and multiple containerized services running at the same time.

The final layout became:

```text
VM3 = Shuffle / SOAR
VM4 = TheHive
```

This separation helped reduce load and made the lab easier to troubleshoot.

## Docker Compose Deployment

TheHive was deployed using Docker Compose.

The setup included TheHive and its required supporting services.

Example deployment flow:

```bash
mkdir ~/thehive
cd ~/thehive
nano docker-compose.yml
```

After creating the Docker Compose file, TheHive was started using:

```bash
sudo docker compose up -d
```

Running containers were checked using:

```bash
sudo docker ps
```

TheHive logs were checked using:

```bash
sudo docker logs thehive --tail=100
```

## TheHive Access

TheHive was accessed from the browser using:

```text
http://<THEHIVE_VM_IP>:9000
```

In this lab, the working TheHive instance URL was:

```text
http://172.16.0.237:9000
```

Only the base URL should be used when configuring TheHive inside Shuffle.

Correct:

```text
http://172.16.0.237:9000
```

Incorrect:

```text
http://172.16.0.237:9000/administration/organisations/OmarSOC/users
```

The longer URL is only the browser page inside the TheHive interface. It is not the API base URL.

## Users and Organization

TheHive was configured with a dedicated organization for the lab.

```text
Organization: OmarSOC
```

Two users were created.

Normal user:

```text
Purpose: Used to log in and view alerts
Organization: OmarSOC
Profile: org-admin or analyst
```

Service user:

```text
Purpose: Used by Shuffle for API access
Login: shuffle@omarsoc.local
Organization: OmarSOC
Profile: analyst
```

The Shuffle service user is not meant for normal browsing. It exists so Shuffle can authenticate to TheHive and create alerts through the API.

## Shuffle Authentication

Shuffle was configured to connect to TheHive using the service user API key.

TheHive instance URL:

```text
http://172.16.0.237:9000
```

API key:

```text
API key generated from the Shuffle service user
```

The API key must belong to a user inside the same organization where the alerts should appear.

In this lab:

```text
User: shuffle@omarsoc.local
Organization: OmarSOC
Profile: analyst
Permission: manageAlert/create
```

## API Authentication Test

The API key was tested from the Shuffle VM using:

```bash
curl -i -H "Authorization: Bearer <THEHIVE_API_KEY>" \
  http://172.16.0.237:9000/api/v1/user/current
```

A successful response returned:

```text
HTTP/1.1 200 OK
```

The response confirmed that the API key belonged to the correct service user.

```text
User: shuffle@omarsoc.local
Organization: OmarSOC
Profile: analyst
Permission: manageAlert/create
```

## Direct Alert Creation Test

Before troubleshooting Shuffle, TheHive alert creation was tested directly using the API.

```bash
curl -i -X POST "http://172.16.0.237:9000/api/v1/alert" \
  -H "Authorization: Bearer <THEHIVE_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Direct API Test Alert",
    "description": "Created directly with curl from Shuffle VM.",
    "type": "external",
    "source": "curl-test",
    "sourceRef": "curl-test-001",
    "severity": 2,
    "tlp": 2,
    "pap": 2,
    "tags": ["curl", "shuffle", "thehive", "test"]
  }'
```

A successful response returned:

```text
HTTP/1.1 201 Created
```

This confirmed that TheHive, the API key, the service user, and the `OmarSOC` organization were working correctly.

## Role in the Lab

TheHive acts as the analyst-facing alert management layer.

```text
Wazuh Alert
   ↓
Shuffle SOAR Workflow
   ↓
TheHive Alert
   ↓
Analyst Review / Case Creation
```

In this lab, Wazuh alerts are sent into Shuffle first. Shuffle then creates alerts inside TheHive for analyst review.

## Issues Faced

* TheHive was initially tested on the same VM as Shuffle
* Running TheHive and Shuffle on the same VM caused heavy disk I/O and slow performance
* TheHive had to be moved to a separate VM
* Alerts did not appear at first because the wrong area of TheHive was being viewed
* The default admin area showed platform administration, not the analyst alert queue
* The normal `OmarSOC` user had to be used to view alerts
* Shuffle required the base TheHive instance URL, not the full browser administration URL
* Alert creation initially failed due to an invalid JSON body
* Static `sourceRef` values only worked once because TheHive rejects duplicate alerts with the same source and reference

## Fixes Applied

* Moved TheHive onto a dedicated VM
* Used the base TheHive URL in Shuffle
* Created a dedicated `OmarSOC` organization
* Created a normal user for viewing alerts
* Created a service user for Shuffle API access
* Generated the API key from the Shuffle service user
* Verified API authentication with `/api/v1/user/current`
* Verified direct alert creation with `/api/v1/alert`
* Used dynamic `sourceRef` values when creating alerts
* Logged in as the normal `OmarSOC` user to view alerts in the correct workspace

## Verification

TheHive was verified in stages.

```text
1. Browser access to TheHive UI
2. Login as normal OmarSOC user
3. API authentication test with /api/v1/user/current
4. Direct alert creation test with /api/v1/alert
5. Shuffle-created alert appearing in TheHive
6. Wazuh alert routed through Shuffle into TheHive
```

The successful test confirmed the end-to-end alert flow:

```text
Failed SSH login attempt
   ↓
Wazuh generated alert
   ↓
Wazuh sent alert to Shuffle webhook
   ↓
Shuffle processed alert
   ↓
Shuffle created TheHive alert
   ↓
Alert appeared in OmarSOC alert queue
```

## Lab Status

TheHive is installed, accessible, and integrated with Shuffle.

The SOC lab can now receive Wazuh alerts through Shuffle and display them inside TheHive for analyst review.
