from enum import Enum


class ErrorMessage(Enum):
    HTTP_EXCEPTION_401 = "No cuenta con privilegios suficientes."
    HTTP_EXCEPTION_401_USER_DOESNT_EXIST = "El usuario no existe."
    HTTP_EXCEPTION_401_INVALID_CREDENTIAL = "Credenciales incorrectas."
    HTTP_EXCEPTION_403 = "No autenticado."
    HTTP_EXCEPTION_404 = "No se encuentra la entidad solicitada."
    HTTP_EXCEPTION_500 = "Ha ocurrido un error inesperado."

    BUSINESS_INFO_GENERAL_EXIST = "El recurso ya se encuentra registrado"
    BUSINESS_INFO_GENERAL_UPDATED = "Recurso actualizado satisfactoriamente"
    BUSINESS_INFO_GENERAL_DELETED = "Recurso eliminado satisfactoriamente"
    BUSINESS_INFO_GENERAL_DESACTIVATED = "Recurso desactivado satisfactoriamente"
    BUSINESS_INFO_GENERAL_ACTIVATED = "Recurso Activado satisfactoriamente"
    BUSINESS_ERROR_UPLOAD_IMAGE = "Error cargando imagen"

    # USER
    BUSINESS_INFO_USER_EMAIL_REGISTERED = "El correo ya está registrado"
    BUSINESS_INFO_USER_ASSIGNED = "El usuario fue asignado satisfactoriamente"
    BUSINESS_INFO_USER_STATE_UPDATED = (
        "El estado del usuario fue actualizado satisfactoriamente"
    )

    # CART USER
    BUSINESS_INFO_USER_REMOVED_FROM_CART = "El usuario fue eliminado del carrito"
    BUSINESS_INFO_USER_ALREADY_ACTIVE = (
        "El usuario ya se encuentra activo en el carrito"
    )

    # PRODUCT
    BUSINESS_INFO_PRODUCT_ID_NULL = "El identificador del producto no puede ser nulo"
    NO_PRODUCT_BY_VIDEO = "No hay un producto relacionado con este video"
    NO_LIST_RELATED_ITEM = "La lista de productos a relacionar no debe estar vacía"
    PRODUCT_RELATED = "Productos relacionados satisfactoriamente"
    LIST_PRODUCT_RELATED = "La lista de productos está vacía"

    # ROL
    BUSINESS_ERROR_ROL_NOT_VALID = "Rol no válido"

    # SUBROL
    BUSINESS_ERROR_SUBROL_NOT_VALID = "SubRol no válido"

    # TAG
    BUSINESS_INFO_TAG_ASSIGNED = "Tag asignado satisfactoriamente"

    # ORDER
    BUSINESS_ERROR_ORDER_CART_EXISTS = (
        "Ya existe una orden creada para el carrito indicado"
    )

    # CART
    BUSINESS_ERROR_CART_NAME_EXISTS = (
        "Ya existe un carrito con este nombre para el usuario"
    )

    # SHOPPING LIST
    BUSINESS_ERROR_ITEM_EXISTS_IN_LIST = (
        "El producto con id {} ya existe en la lista {}"
    )
    BUSINESS_INFO_ITEM_ADDED_SHOPPING_LIST = "Item(s) agregado(s) exitosamente"

    # SCHEDULE DELIVERY
    BUSINESS_ERROR_DATE = "La fecha de inicio no puede ser mayor a la fecha de fin"
