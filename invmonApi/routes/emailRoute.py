from fastapi import APIRouter
from invmonInfra.domain.emailInterface import EmailInterface
from invmonService import EmailService


EmailRouter = APIRouter(prefix='/email', tags=['email', 'test'])


@EmailRouter.get('/test/email')
def testEmail(emailAddress: str) -> None:
    es: EmailInterface = EmailService()
    es.setTo(emailAddress)
    es.setSubject("API Route Test")
    es.setBody("Nothing to see here, but did it work?")
    es.send()
    print('l')
