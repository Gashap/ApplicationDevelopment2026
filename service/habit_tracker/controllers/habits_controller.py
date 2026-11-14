import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from habit_tracker.models.api_error import ApiError  # noqa: E501
from habit_tracker.models.habit_page import HabitPage  # noqa: E501
from habit_tracker.models.habit_patch_request import HabitPatchRequest  # noqa: E501
from habit_tracker.models.habit_status import HabitStatus  # noqa: E501
from habit_tracker.models.habit_view import HabitView  # noqa: E501
from habit_tracker.models.new_habit_request import NewHabitRequest  # noqa: E501
from habit_tracker import util


def create_habit(new_habit_request):  # noqa: E501
    """Создать привычку

    Создаёт новую привычку. POST не идемпотентен: два одинаковых запроса создадут две привычки.  # noqa: E501

    :param new_habit_request: 
    :type new_habit_request: dict | bytes

    :rtype: Union[HabitView, Tuple[HabitView, int], Tuple[HabitView, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        new_habit_request = NewHabitRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_habit(habit_id):  # noqa: E501
    """Удалить привычку

    DELETE идемпотентен: повторный вызов вернёт 404, состояние не изменится. # noqa: E501

    :param habit_id: Идентификатор привычки
    :type habit_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_habit(habit_id):  # noqa: E501
    """Получить одну привычку

     # noqa: E501

    :param habit_id: Идентификатор привычки
    :type habit_id: int

    :rtype: Union[HabitView, Tuple[HabitView, int], Tuple[HabitView, int, Dict[str, str]]
    """
    return 'do some magic!'


def list_habits(status=None, limit=None, offset=None):  # noqa: E501
    """Список привычек текущего пользователя

    Возвращает страницу привычек. Можно отфильтровать по статусу. # noqa: E501

    :param status: Показать только активные или только архивные привычки
    :type status: dict | bytes
    :param limit: Сколько привычек вернуть на странице
    :type limit: int
    :param offset: Сколько привычек пропустить от начала списка
    :type offset: int

    :rtype: Union[HabitPage, Tuple[HabitPage, int], Tuple[HabitPage, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        status =  HabitStatus.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_habit(habit_id, habit_patch_request):  # noqa: E501
    """Изменить часть полей привычки

    Частичное обновление: меняются только переданные поля. Например, тело только с полем status &#x3D; ARCHIVED отправит привычку в архив.  # noqa: E501

    :param habit_id: Идентификатор привычки
    :type habit_id: int
    :param habit_patch_request: 
    :type habit_patch_request: dict | bytes

    :rtype: Union[HabitView, Tuple[HabitView, int], Tuple[HabitView, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        habit_patch_request = HabitPatchRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
