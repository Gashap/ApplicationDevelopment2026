import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from habit_tracker.errors import api_error
from habit_tracker.models.habit_page import HabitPage  # noqa: E501
from habit_tracker.models.habit_patch_request import HabitPatchRequest  # noqa: E501
from habit_tracker.models.habit_view import HabitView  # noqa: E501
from habit_tracker.models.new_habit_request import NewHabitRequest  # noqa: E501
from habit_tracker.store import HabitEntity, store

DEFAULT_LIMIT = 20
DEFAULT_OFFSET = 0


def _to_view(habit: HabitEntity) -> HabitView:
    """Entity -> DTO: наружу едут только поля из схемы HabitView."""
    return HabitView(
        id=habit.id,
        title=habit.title,
        description=habit.description,
        frequency=habit.frequency,
        target_per_week=habit.target_per_week,
        status=habit.status,
        current_streak=habit.current_streak,
        created_at=habit.created_at,
    )


def _find_own_habit(habit_id, user):
    """404 — привычки нет; 403 — «знаю, кто ты, но привычка чужая»."""
    habit = store.find(habit_id)
    if habit is None:
        return None, api_error(404, f"Привычка {habit_id} не найдена")
    if habit.owner_id != user:
        return None, api_error(403, "Нет доступа к этой привычке")
    return habit, None


def create_habit(new_habit_request, user=None):  # noqa: E501
    """Создать привычку

    Создаёт новую привычку. POST не идемпотентен: два одинаковых запроса создадут две привычки.  # noqa: E501

    :param new_habit_request: 
    :type new_habit_request: dict | bytes

    :rtype: Union[HabitView, Tuple[HabitView, int], Tuple[HabitView, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        new_habit_request = NewHabitRequest.from_dict(connexion.request.get_json())  # noqa: E501
    habit = store.create(
        owner_id=user,
        title=new_habit_request.title,
        frequency=new_habit_request.frequency,
        description=new_habit_request.description,
        target_per_week=new_habit_request.target_per_week,
    )
    return _to_view(habit), 201, {'Location': f'/api/habits/{habit.id}'}


def delete_habit(habit_id, user=None):  # noqa: E501
    """Удалить привычку

    DELETE идемпотентен: повторный вызов вернёт 404, состояние не изменится. # noqa: E501

    :param habit_id: Идентификатор привычки
    :type habit_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    habit, error = _find_own_habit(habit_id, user)
    if error is not None:
        return error
    store.delete(habit.id)
    return '', 204


def get_habit(habit_id, user=None):  # noqa: E501
    """Получить одну привычку

     # noqa: E501

    :param habit_id: Идентификатор привычки
    :type habit_id: int

    :rtype: Union[HabitView, Tuple[HabitView, int], Tuple[HabitView, int, Dict[str, str]]
    """
    habit, error = _find_own_habit(habit_id, user)
    if error is not None:
        return error
    return _to_view(habit)


def list_habits(status=None, limit=None, offset=None, user=None):  # noqa: E501
    """Список привычек текущего пользователя

    Возвращает страницу привычек. Можно отфильтровать по статусу. # noqa: E501

    :param status: Показать только активные или только архивные привычки
    :type status: str
    :param limit: Сколько привычек вернуть на странице
    :type limit: int
    :param offset: Сколько привычек пропустить от начала списка
    :type offset: int

    :rtype: Union[HabitPage, Tuple[HabitPage, int], Tuple[HabitPage, int, Dict[str, str]]
    """
    limit = DEFAULT_LIMIT if limit is None else limit
    offset = DEFAULT_OFFSET if offset is None else offset
    habits = store.list_for_owner(user, status)
    page = habits[offset:offset + limit]
    return HabitPage(
        items=[_to_view(h) for h in page],
        total=len(habits),
        limit=limit,
        offset=offset,
    )


def update_habit(habit_id, habit_patch_request, user=None):  # noqa: E501
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
    habit, error = _find_own_habit(habit_id, user)
    if error is not None:
        return error
    # null в схеме запрещён, поэтому None == «поле не передали».
    for field in ('title', 'description', 'frequency', 'target_per_week', 'status'):
        value = getattr(habit_patch_request, field)
        if value is not None:
            setattr(habit, field, value)
    return _to_view(habit)
