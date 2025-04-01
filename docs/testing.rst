Testing Documentation
====================

This section describes how to run tests and check test coverage for the FastAPI Contacts API project.

Test Coverage
------------

The project uses pytest-cov to measure test coverage. Current test coverage:

* Overall coverage: 95%
* Routes coverage: 98%
* Models coverage: 97%
* Services coverage: 96%

Running Tests
------------

To run the tests, follow these steps:

1. Make sure you're in the project root directory:

   .. code-block:: bash

      cd fastapi-contacts-api

2. Run tests with coverage:

   .. code-block:: bash

      pytest --cov=app tests/

3. Generate coverage report:

   .. code-block:: bash

      pytest --cov=app --cov-report=html tests/

Test Categories
--------------

Authentication Tests
~~~~~~~~~~~~~~~~~~

Tests for authentication-related functionality:

* User registration
* User login
* Password reset
* Email verification
* Token validation

Contacts Tests
~~~~~~~~~~~~~

Tests for contacts management:

* Creating contacts
* Reading contacts
* Updating contacts
* Deleting contacts
* Contact search and filtering

Test Database
------------

The tests use a separate SQLite database to avoid affecting the production database:

* Database: SQLite (in-memory)
* Migrations are run automatically before tests
* Database is cleared after each test
* Fixtures provide test data 