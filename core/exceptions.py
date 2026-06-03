"""Исключения приложения."""


class UserAlreadyExistsError(Exception):
    """Пользователь уже существует."""


class UserNotFoundError(Exception):
    """Пользователь не найден."""


class CredentialsError(Exception):
    """Неверные данные авторизации."""


class TokenError(Exception):
    """Ошибка токена."""


class CurrencyNotFoundError(Exception):
    """Валюта не найдена."""
