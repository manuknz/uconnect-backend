from enum import Enum


class ErrorMessage(Enum):
    HTTP_EXCEPTION_401 = "No se pudo validar las credenciales"
    HTTP_EXCEPTION_401_USER_DOESNT_EXIST = "El usuario no existe"
    HTTP_EXCEPTION_401_COMPANY_DOESNT_EXIST = "El usuario no existe"
    HTTP_EXCEPTION_401_INVALID_CREDENTIAL = "Credenciales incorrectas"
    HTTP_EXCEPTION_403 = "No autenticado"
    HTTP_EXCEPTION_404 = "No se encuentra la entidad solicitada"
    HTTP_EXCEPTION_500 = "Ha ocurrido un error inesperado"

    INFO_GENERAL_EXIST = "El recurso ya se encuentra registrado"
    INFO_GENERAL_UPDATED = "Recurso actualizado satisfactoriamente"
    INFO_GENERAL_DELETED = "Recurso eliminado satisfactoriamente"
    INFO_GENERAL_DESACTIVATED = "Recurso desactivado satisfactoriamente"
    INFO_GENERAL_ACTIVATED = "Recurso activado satisfactoriamente"

    # USER
    USER_EMAIL_REGISTERED = "El correo ya está registrado"
    USER_EMAIL_NOT_FOUND = "El correo no se encuentra registrado"
    USER_ASSIGNED = "El usuario fue asignado satisfactoriamente"
    USER_STATE_UPDATED = "El usuario fue editado satisfactoriamente"

    # JOB
    JOB_NOT_FOUND = "La oferta de trabajo no existe"
    JOB_STATE_UPDATED = "La oferta de trabajo fue actualizada satisfactoriamente"

    # CAREER
    CAREER_NOT_FOUND = "La carrera no existe"

    # CITY
    CITY_NOT_FOUND = "La ciudad no existe"

    # FILE
    FILE_NOT_FOUND = "El archivo no existe"
    FILE_EXTENSION_NOT_ALLOWED = (
        "Formato de archivo no permitido. Formatos permitidos: PNG/JPEG/WEBP/PDF"
    )
    FILE_DELETED = "Archivo eliminado satisfactoriamente"
    FILE_UPLOAD_ERROR = "Ha ocurrido un error al cargar el archivo"
    IMAGE_EXTENSION_NOT_ALLOWED = (
        "Formato de archivo no permitido. Formatos permitidos: PNG/JPEG/WEBP"
    )
