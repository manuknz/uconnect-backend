from fastapi import status
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

from app.env.env import EmailSettings


mail_settings = EmailSettings()


async def send_email(subject: str, message_html: str, email: str):
    message = MessageSchema(
        subject=subject, recipients=[email], body=message_html, subtype="html"
    )

    fm = FastMail(mail_settings.conf)
    await fm.send_message(message)
    return {"status": status.HTTP_200_OK, "message": "El correo fue enviado."}


async def send_password_recovery_email(full_name, email, password_reset_code):
    subject = "uConnect APP - Recuperar contraseña"
    message = (
        """
    <html>
        <div>Hola """
        + full_name
        + """! </div>
        <div>Hemos recibido una solicitud para recuperar tu contraseña. </div>
        <div>Tu nueva contraseña es: </div>
        <div style="font-weight: bold; margin-top: 1rem; margin-bottom: 1rem"> """
        + password_reset_code
        + """ </div>
        <div>Si no has enviado esta solicitud, puedes ignorar este correo y continuar con tu contraseña actual. </div>
    </html>
    """
    )
    return await send_email(subject, message, email)


async def send_user_job_applied_email(
    company_name, user_name, career_name, job_date, email
):
    subject = "uConnect APP - Nuevo aplicante a tu vacante"
    message = (
        """
    <html>
        <div>Hola """
        + company_name
        + """! </div>
        <div style="font-weight: bold; margin-top: 1rem; margin-bottom: 1rem">El estudiante """
        + user_name
        + """, de la carrera """
        + career_name
        + """, ha aplicado a tu oferta laboral creada el """
        + job_date
        + """. </div>
        <div>Ingresa a la APP para ver mas detalles del aplicante!</div>
    </html>
    """
    )
    return await send_email(subject, message, email)
