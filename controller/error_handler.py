import logging

from flask import jsonify
from flask_principal import PermissionDenied

from controller.exceptions import NotFound, Unauthorized, AlreadyExists
from core.application import app


def wrapp_error(status_code, payload):
    """
    Wrap all of our exception responses in a JSON object
    """
    response = jsonify(payload)
    response.status_code = status_code
    return response


@app.errorhandler(Exception)
def handle_unknown(error):
    """
    Catch any unknown exceptions.
    Try to transform errors with a name and code.
    If those attributes do not exist default to 500/unknown error
    """
    logging.error(error)
    return wrapp_error(500 if not hasattr(error, 'code') else error.code,
                       {"message": "unknown error" if not hasattr(error, 'name') else error.name})


@app.errorhandler(PermissionDenied)
def handle_permission_denied(error):
    return wrapp_error(401, {"message": "Permission Denied"})


@app.errorhandler(NotFound)
def handl_not_found(error):
    """
    Catch and transform any NotFound errors into JSON format.
    """
    return wrapp_error(error.status_code, error.to_dict())


@app.errorhandler(Unauthorized)
def handle_unauthorized(error):
    """
    Catch and transform any Unauthorized errors into JSON format.
    """
    return wrapp_error(error.status_code, error.to_dict())


@app.errorhandler(AlreadyExists)
def handle_already_exists(error):
    """
    Catch and transform any AlreadyExists errors into JSON format.
    """
    return wrapp_error(error.status_code, error.to_dict())
