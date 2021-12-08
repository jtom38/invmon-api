# Inventory Monitor (invmon) API

- [Inventory Monitor (invmon) API](#inventory-monitor-invmon-api)
  - [About](#about)
  - [Getting Started](#getting-started)
  - [Database](#database)
  - [Database Migrations](#database-migrations)
    - [Running migrations from docker compose](#running-migrations-from-docker-compose)
  - [Health Checks](#health-checks)
    - [Docker Health Check](#docker-health-check)
    - [Kubernetes Health Check](#kubernetes-health-check)
  - [Changelog](#changelog)
    - [0.1.0](#010)

## About

This API is a tool that will monitor a site for when something comes in-stock and will alert you about it.  Right now, its still very early in its life and will get updates as I have free time to work on them.

## Getting Started

1. Download Docker Image
1. Configure Docker Container
    1. Setup ENV flags
1. Run Migrations
1. Start API
    1. Add SmtpContact
        1. This defines who will get alerts.
    1. Add Inventory
        1. This defines what the API will monitor item wise.
    1. Add Alerts
        1. This defines when an item (inventory) is found, who will get the alert.

## Database

This application is built to support SQLite or Postgresql.  Postgresql is recommended.  

Once you have postgresql installed, you will need to edit alembic.ini and update the line for `sqlalchemy.url` with your connection information.

## Database Migrations

Each release it is recommended to run the database migrations.  If anything comes up, the database schema can be rolled back!  But, always practice safe database habits and backup the database prior to running migrations.

To upgrade the database, `alembic upgrade head`

To rollback `alembic downgrade -1`

### Running migrations from docker compose

Because you will need to have your secrets to connect to your Postgres Server, you can run the migrations directly from your docker-compose.yaml file.  I will use the `docker-compose.yaml` in the project as an example.  The `api` call references the service named `api` in the compose file.  All of the `environment` values will be used as it talks to the database server.

`docker compose run api alembic upgrade head`
`docker compose run api alembic downgrade -1`

## Health Checks

This project has health checks enabled so you can monitor how the API is doing.  The endpoint is `/health`.  

### Docker Health Check

See the `docker-compose.yaml` file for an example on how to configure the health check for Docker

### Kubernetes Health Check

TBD

## Changelog

### 0.1.0

- The API will use Postgres as its primary DB.
- Health checks have been added to monitor the DB and check on the `shopdisney.com` site.
- The `shopdisney.com` site was added as a monitored inventory service.
- The following tables where added to the database.
  - SmtpContacts
  - EmailAlerts
  - ActiveAlerts
- SMTP Information can be added via the environment variables.
- SMTP was tested against gmail.
