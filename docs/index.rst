.. FastAPI Contacts API documentation master file, created by
   sphinx-quickstart on Fri Mar 28 08:22:37 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to FastAPI Contacts API's documentation!
===============================================

This is the documentation for the FastAPI Contacts API project.

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api
   database
   models
   main
   testing

Installation
------------

To get started with the FastAPI Contacts API, follow these steps:

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/yourusername/fastapi-contacts-api.git
      cd fastapi-contacts-api

2. Create a virtual environment:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

API Documentation
----------------

The API documentation is organized into the following sections:

* Authentication
* Contacts Management
* User Profile
* Avatar Management

For detailed information about each endpoint, please refer to the :doc:`api` section.

Features
--------

* User Authentication and Authorization
* Contact Management (CRUD operations)
* Email Verification
* Password Reset Functionality
* User Roles (Admin/User)

Testing
-------

For information about testing, please refer to the :doc:`testing` section.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
