coverage run -m pytest
coverage report --omit="*/test*,*/__init__.py,database.py,*/conftest.py"