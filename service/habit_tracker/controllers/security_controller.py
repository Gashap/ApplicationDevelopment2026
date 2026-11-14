# Демонстрационная авторизация: вместо настоящих JWT — заранее известные токены.
DEMO_TOKENS = {
    "alice-token": "alice",
    "bob-token": "bob",
}


def info_from_bearerAuth(token):
    """
    Check and retrieve authentication information from custom bearer token.
    Returned value will be passed in 'token_info' parameter of your operation function, if there is one.
    'sub' or 'uid' will be set in 'user' parameter of your operation function, if there is one.

    :param token Token provided by Authorization header
    :type token: str
    :return: Decoded token information or None if token is invalid
    :rtype: dict | None
    """
    user = DEMO_TOKENS.get(token)
    if user is None:
        return None  # connexion ответит 401 — «не знаю, кто ты»
    return {'sub': user}
