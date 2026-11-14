import sys
from setuptools import setup, find_packages

NAME = "habit_tracker"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.0.2",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="Habit Tracker API",
    author_email="",
    url="",
    keywords=["OpenAPI", "Habit Tracker API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['habit_tracker=habit_tracker.__main__:main']},
    long_description="""\
    API трекера привычек: пользователь заводит привычки, смотрит их список, правит и удаляет. Подход API first — сначала контракт, потом код.  Правило контракта: метод &#x3D; намерение · статус &#x3D; результат · форма &#x3D; DTO. Внутренние поля сущности (ownerId, служебные флаги, даты удаления) наружу не отдаются — клиент видит только схемы из components.  Ошибки доступа: * **401** — «не знаю, кто ты»: нет токена или он недействителен; * **403** — «знаю — нельзя»: токен в порядке, но привычка чужая. 
    """
)

