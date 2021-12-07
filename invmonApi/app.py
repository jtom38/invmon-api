from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_healthcheck import HealthCheckFactory, healthCheckRoute
from fastapi_healthcheck_sqlalchemy import HealthCheckSQLAlchemy
from fastapi_healthcheck_uri import HealthCheckUri
from invmonApi.databaseConnection import ConnectionString
from invmonApi.routes import *
from invmonApi.events import ApiEventsService
from invmonService import EnvReaderService
from invmonInfra.enum import EnvReaderEnum
from invmonService.envReaderService import EnvReaderService
from invmonInfra.models import SmtpContactsSqlModel

_env = EnvReaderService()

# Enable pyroscope for profiling
if _env.getValue(EnvReaderEnum.PYROSCOPEENABLED) == True:
    import pyroscope
    pyroscope_address = _env.getValue(EnvReaderEnum.PYROSCOPESERVERADDRESS)
    pyroscope.configure(
        app_name='invmon.api'
        ,server_address=pyroscope_address
    )
    print(f"Pyroscope metrics are being sent to {pyroscope_address}")

tags = []
tags.append(ActiveAlertsTags)
tags.append(SmtpContactsTags)
tags.append(EmailAlertTags)
tags.append(InventoryTag)

app = FastAPI(
    title="Inventory Monitor"
    ,description="The backend agent to collect articles and send notifications."
    ,version="0.0.1"
    ,openapi_tags=tags
)

# Enable SQL Connection to the API
cs = ConnectionString()
app.add_middleware(DBSessionMiddleware, db_url=cs.value)

# Add Health Checks
_healthChecks = HealthCheckFactory()
_healthChecks.add(HealthCheckSQLAlchemy(alias='postgres db', table=SmtpContactsSqlModel, tags=('postgres', 'db', 'sql01.home.local')))
_healthChecks.add(HealthCheckUri(alias='shopdisney', connectionUri="https://www.shopdisney.com/", tags=('external', 'shopdisney', 'uri')))

app.add_api_route('/health', endpoint=healthCheckRoute(factory=_healthChecks), include_in_schema=False)

# Add routes
app.include_router(SchedulerRouter)
app.include_router(SmtpContactsRouter)
app.include_router(ActiveAlertsRouter)
app.include_router(EmailAlertsRouter)
app.include_router(InventoryRouter)

# Enable debug routes
if _env.getValue(EnvReaderEnum.LOCALDEV) == True:
    from invmonApi.routes import EmailRouter
    app.include_router(EmailRouter)

@app.on_event('startup')
def startupEvent() -> None:
    ApiEventsService().startup()
    pass

@app.on_event('shutdown')
def shutdownEvent() -> None:
    ApiEventsService().shutdown()
