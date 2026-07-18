from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.hr.models import Employee

class EmployeeLoginViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employee = Employee.objects.create_user(
            emp_id='EMP001',
            password='password123',
            name='Test Employee',
            email='test@acme.com'
        )

    def test_login_success(self):
        response = self.client.post(
            reverse('employee-login'),
            {'emp_id': 'EMP001', 'password': 'password123'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['employee']['emp_id'], 'EMP001')

    def test_login_invalid_password(self):
        response = self.client.post(
            reverse('employee-login'),
            {'emp_id': 'EMP001', 'password': 'wrongpassword'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Invalid emp_id or password')

    def test_login_invalid_emp_id(self):
        response = self.client.post(
            reverse('employee-login'),
            {'emp_id': 'EMP999', 'password': 'password123'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Invalid emp_id or password')

    def test_login_missing_fields(self):
        response = self.client.post(
            reverse('employee-login'),
            {'emp_id': 'EMP001'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'emp_id and password are required')

    def test_login_success_case_insensitive(self):
        response = self.client.post(
            reverse('employee-login'),
            {'emp_id': 'emp001', 'password': 'password123'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employee']['emp_id'], 'EMP001')

    def test_login_success_with_dashes(self):
        response = self.client.post(
            reverse('employee-login'),
            {'emp_id': 'EMP-001', 'password': 'password123'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employee']['emp_id'], 'EMP001')

    def test_login_success_lowercase_with_dashes(self):
        response = self.client.post(
            reverse('employee-login'),
            {'emp_id': 'emp-001', 'password': 'password123'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employee']['emp_id'], 'EMP001')
