# Inventory Monitor (invmon) API

This API is a tool that will monitor a site for when something comes in-stock and will alert you about it.

## Getting Started

1. Download Docker Image - TBD
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

## Health Checks

This project has health checks enabled so you can monitor how the API is doing.  The endpoint is `/health`.  


