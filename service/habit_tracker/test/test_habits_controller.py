import unittest

from flask import json

from habit_tracker.models.api_error import ApiError  # noqa: E501
from habit_tracker.models.habit_page import HabitPage  # noqa: E501
from habit_tracker.models.habit_patch_request import HabitPatchRequest  # noqa: E501
from habit_tracker.models.habit_status import HabitStatus  # noqa: E501
from habit_tracker.models.habit_view import HabitView  # noqa: E501
from habit_tracker.models.new_habit_request import NewHabitRequest  # noqa: E501
from habit_tracker.test import BaseTestCase


class TestHabitsController(BaseTestCase):
    """HabitsController integration test stubs"""

    def test_create_habit(self):
        """Test case for create_habit

        Создать привычку
        """
        new_habit_request = {"targetPerWeek":5,"description":"Перед сном, бумажная книга","title":"Читать 20 минут","frequency":"DAILY"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/habits',
            method='POST',
            headers=headers,
            data=json.dumps(new_habit_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_habit(self):
        """Test case for delete_habit

        Удалить привычку
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/habits/{habit_id}'.format(habit_id=42),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_habit(self):
        """Test case for get_habit

        Получить одну привычку
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/habits/{habit_id}'.format(habit_id=42),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_habits(self):
        """Test case for list_habits

        Список привычек текущего пользователя
        """
        query_string = [('status', habit_tracker.HabitStatus()),
                        ('limit', 20),
                        ('offset', 0)]
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/habits',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_habit(self):
        """Test case for update_habit

        Изменить часть полей привычки
        """
        habit_patch_request = {"targetPerWeek":1,"description":"description","title":"title","frequency":"DAILY","status":"ACTIVE"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/habits/{habit_id}'.format(habit_id=42),
            method='PATCH',
            headers=headers,
            data=json.dumps(habit_patch_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
