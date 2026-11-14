"""Все ошибки (в том числе 400/401 от connexion) отдаются в форме DTO ApiError."""
from connexion.exceptions import ProblemException
from flask import jsonify
from werkzeug.exceptions import HTTPException, default_exceptions

DEFAULT_MESSAGES = {
    400: "Некорректный запрос",
    401: "Требуется авторизация",
    403: "Нет доступа",
    404: "Ресурс не найден",
    405: "Метод не поддерживается",
}


def api_error(status: int, message: str):
    response = jsonify({"message": message})
    response.status_code = status
    return response


def _handle_problem(exc: ProblemException):
    message = DEFAULT_MESSAGES.get(exc.status, exc.title or "Ошибка")
    if exc.status == 400 and exc.detail:
        message = f"{message}: {exc.detail.splitlines()[0]}"
    return api_error(exc.status, message)


def _handle_http(exc: HTTPException):
    code = exc.code or 500
    return api_error(code, DEFAULT_MESSAGES.get(code, exc.name))


def register_error_handlers(flask_app) -> None:
    flask_app.register_error_handler(ProblemException, _handle_problem)
    for code in default_exceptions:
        flask_app.register_error_handler(code, _handle_http)
