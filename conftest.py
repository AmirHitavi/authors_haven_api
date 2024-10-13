import pytest
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from pytest_factoryboy import register

from core_apps.profiles.tests.factories import ProfileFactory
from core_apps.users.tests.factories import UserFactory

register(UserFactory)
register(ProfileFactory)


@pytest.fixture
def normal_user(db, user_factory):
    new_user = user_factory.create()
    return new_user


@pytest.fixture
def super_user(db, user_factory):
    new_user = user_factory.create(is_staff=True, is_superuser=True)
    return new_user


@pytest.fixture
def mock_request():
    factory = RequestFactory()
    request = factory.get("/")

    session_middleware = SessionMiddleware(lambda request: None)
    session_middleware.process_request(request)
    request.session.save()

    auth_middleware = AuthenticationMiddleware(lambda request: None)
    auth_middleware.process_request(request)

    return request


@pytest.fixture
def user_profile(db, profile_factory):
    new_profile = profile_factory()
    return new_profile
