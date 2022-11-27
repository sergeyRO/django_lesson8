import random

import pytest
from rest_framework.test import APIClient
from students.models import Course, Student
from model_bakery import baker


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student():
    return Student.objects.create(name='Василий Пупкин')


@pytest.fixture
def course():
    return baker.make(Course)


@pytest.fixture
def courses():
    return baker.make(Course, 10)


@pytest.mark.django_db
def test_get_course(client, course):
    response = client.get(f'/api/v1/courses/{course.id}/')
    assert response.status_code == 200
    assert response.data['id'] == course.id


@pytest.mark.django_db
def test_get_courses(client, courses):
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    assert len(courses) == len(response.data)


@pytest.mark.django_db
def test_get_filter_course_id(client, courses):
    id_course = [item.id for item in courses][random.randint(0, 9)]
    response = client.get(f'/api/v1/courses/?id={id_course}')
    assert response.status_code == 200
    assert response.data[0]['id'] == id_course


@pytest.mark.django_db
def test_get_filter_course_name(client, courses):
    name_course = [item.name for item in courses][random.randint(0, 9)]
    response = client.get(f'/api/v1/courses/?name={name_course}')
    assert response.status_code == 200
    assert response.data[0]['name'] == name_course


@pytest.mark.django_db
def test_create_course(client):
    count_courses_start = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'name': 'First course'}, format='json')
    assert response.status_code == 201
    assert Course.objects.count() == count_courses_start + 1


@pytest.mark.django_db
def test_update_course(client, course):
    new_name = course.name[::-1]
    response = client.patch(f'/api/v1/courses/{course.id}/', data={'name': new_name}, format='json')
    assert response.status_code == 200
    update_course = Course.objects.filter(id=course.id).first()
    assert course.name != update_course.name

@pytest.mark.django_db
def test_delete_course(client, course):
    count_courses = Course.objects.count()
    response = client.delete(f'/api/v1/courses/{course.id}/')
    assert response.status_code == 204
    assert Course.objects.count() == count_courses - 1