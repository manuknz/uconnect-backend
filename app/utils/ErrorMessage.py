from enum import Enum


class ErrorMessage(Enum):
    HTTP_EXCEPTION_401 = "No cuenta con privilegios suficientes."
    HTTP_EXCEPTION_401_USER_DOESNT_EXIST = "El usuario no existe."
    HTTP_EXCEPTION_401_INVALID_CREDENTIAL = "Credenciales incorrectas."
    HTTP_EXCEPTION_403 = "No autenticado."
    HTTP_EXCEPTION_404 = "No se encuentra la entidad solicitada."
    HTTP_EXCEPTION_500 = "Ha ocurrido un error inesperado."

    INFO_GENERAL_EXIST = "El recurso ya se encuentra registrado"
    INFO_GENERAL_UPDATED = "Recurso actualizado satisfactoriamente"
    INFO_GENERAL_DELETED = "Recurso eliminado satisfactoriamente"
    INFO_GENERAL_DESACTIVATED = "Recurso desactivado satisfactoriamente"
    INFO_GENERAL_ACTIVATED = "Recurso activado satisfactoriamente"
    ERROR_UPLOAD_IMAGE = "Error cargando imagen"

    # USER
    USER_EMAIL_REGISTERED = "El correo ya está registrado"
    USER_ASSIGNED = "El usuario fue asignado satisfactoriamente"
    USER_STATE_UPDATED = "El usuario fue editado satisfactoriamente"

    # JOB
    JOB_NOT_FOUND = "La oferta de trabajo no existe"
    JOB_STATE_UPDATED = "La oferta de trabajo fue actualizada satisfactoriamente"
