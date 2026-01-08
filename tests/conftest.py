import django
import pytest
from django.conf import settings


def pytest_configure() -> None:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        SITE_ID=1,
        SECRET_KEY='test',
        USE_I18N=True,
        STATIC_URL='/static/',
        ROOT_URLCONF='tests.app.urls',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    'debug': True,  # We want template errors to raise
                },
            },
        ],
        MIDDLEWARE=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'rest_framework',
            'permission_manager_drf',
            'tests.app',
        ),
        PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher',),
    )

    django.setup()


@pytest.fixture
def admin_client(client):
    from django.contrib.auth.models import User  # noqa: PLC0415

    user = User.objects.create_user(
        username='admin',
        password='qwerty',
        is_staff=True,
    )
    client.force_login(user)
    return client


@pytest.fixture
def user_client(client):
    from django.contrib.auth.models import User  # noqa: PLC0415

    user = User.objects.create_user(
        username='user',
        password='qwerty',
        is_staff=False,
    )
    client.force_login(user)
    return client
