import unittest

from habit_tracker.test import BaseTestCase

ALICE = {'Authorization': 'Bearer alice-token'}
BOB = {'Authorization': 'Bearer bob-token'}


class TestHabitsController(BaseTestCase):
    """HabitsController integration test stubs"""

    def _create(self, headers=ALICE, **body):
        payload = {'title': 'Читать 20 минут', 'frequency': 'WEEKLY', 'targetPerWeek': 5}
        payload.update(body)
        return self.client.post('/api/habits', json=payload, headers=headers)

    def test_create_habit(self):
        response = self._create(description='Перед сном')
        self.assertStatus(response, 201)
        self.assertEqual(response.headers['Location'], '/api/habits/1')
        body = response.json
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['status'], 'ACTIVE')
        self.assertEqual(body['currentStreak'], 0)
        self.assertTrue(body['createdAt'].endswith('+00:00'))
        self.assertNotIn('ownerId', body)
        self.assertNotIn('owner_id', body)
        self.assertNotIn('reminderJobId', body)

    def test_create_habit_validation(self):
        self.assert400(self._create(title=''))
        self.assert400(self._create(frequency='HOURLY'))
        self.assert400(self._create(targetPerWeek=8))
        self.assert400(self._create(ownerId='bob'))
        response = self.client.post('/api/habits', json={'title': 'x'}, headers=ALICE)
        self.assert400(response)
        self.assertIn('message', response.json)

    def test_unauthorized(self):
        for headers in ({}, {'Authorization': 'Bearer wrong'}):
            response = self.client.get('/api/habits', headers=headers)
            self.assert401(response)
            self.assertEqual(response.json, {'message': 'Требуется авторизация'})
        self.assert401(self._create(headers={}))

    def test_list_habits(self):
        self._create()
        self._create(title='Бегать', frequency='DAILY')
        self._create(headers=BOB)
        self.client.patch('/api/habits/2', json={'status': 'ARCHIVED'}, headers=ALICE)

        response = self.client.get('/api/habits', headers=ALICE)
        self.assert200(response)
        self.assertEqual(response.json['total'], 2)
        self.assertEqual(response.json['limit'], 20)
        self.assertEqual(response.json['offset'], 0)

        response = self.client.get('/api/habits?status=ARCHIVED', headers=ALICE)
        self.assertEqual([h['id'] for h in response.json['items']], [2])

        response = self.client.get('/api/habits?limit=1&offset=1', headers=ALICE)
        self.assertEqual([h['id'] for h in response.json['items']], [2])
        self.assertEqual(response.json['total'], 2)

        self.assert400(self.client.get('/api/habits?limit=0', headers=ALICE))
        self.assert400(self.client.get('/api/habits?limit=abc', headers=ALICE))
        self.assert400(self.client.get('/api/habits?status=DONE', headers=ALICE))

    def test_get_habit(self):
        self._create()
        response = self.client.get('/api/habits/1', headers=ALICE)
        self.assert200(response)
        self.assertEqual(response.json['title'], 'Читать 20 минут')

        self.assert403(self.client.get('/api/habits/1', headers=BOB))
        self.assert404(self.client.get('/api/habits/99', headers=ALICE))
        self.assert401(self.client.get('/api/habits/1'))

    def test_update_habit(self):
        self._create()
        response = self.client.patch('/api/habits/1', json={'status': 'ARCHIVED'}, headers=ALICE)
        self.assert200(response)
        self.assertEqual(response.json['status'], 'ARCHIVED')
        self.assertEqual(response.json['title'], 'Читать 20 минут')

        self.assert400(self.client.patch('/api/habits/1', json={}, headers=ALICE))
        self.assert400(self.client.patch('/api/habits/1', json={'title': None}, headers=ALICE))
        self.assert403(self.client.patch('/api/habits/1', json={'title': 'x'}, headers=BOB))
        self.assert404(self.client.patch('/api/habits/99', json={'title': 'x'}, headers=ALICE))

    def test_delete_habit(self):
        self._create()
        self.assert403(self.client.delete('/api/habits/1', headers=BOB))
        response = self.client.delete('/api/habits/1', headers=ALICE)
        self.assertStatus(response, 204)
        self.assertEqual(response.data, b'')
        self.assert404(self.client.delete('/api/habits/1', headers=ALICE))
        self.assert404(self.client.get('/api/habits/1', headers=ALICE))


if __name__ == '__main__':
    unittest.main()
