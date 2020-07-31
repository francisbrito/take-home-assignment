Tesorio - Assignment
====================

A take-home assignment for candidates applying for a backend position.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style
.. image:: https://img.shields.io/github/license/francisbrito/tesorio-assignment
     :target: https://github.com/francisbrito/tesorio-assignment
     :alt: GitHub
.. image:: https://img.shields.io/github/languages/top/francisbrito/tesorio-assignment
     :target: https://github.com/francisbrito/tesorio-assignment
     :alt: GitHub top language
.. image:: https://img.shields.io/github/last-commit/francisbrito/tesorio-assignment
     :target: https://github.com/francisbrito/tesorio-assignment
     :alt: GitHub last commit

Installation
------------

System requirements
^^^^^^^^^^^^^^^^^^^

* Git_
* Python_ 3.6+
* PostgreSQL_ 10.x
* Redis_ 3.x

.. _Git: https://git-scm.com/
.. _Python: https://www.python.org/
.. _PostgreSQL: https://www.postgresql.org/
.. _Redis: https://redis.io/

Project Setup
^^^^^^^^^^^^^

1. Clone the project:

.. code-block:: shell

    $ git clone git@github.com:francisbrito/tesorio-assignment.git
    $ cd tesorio-assignment

2. Create a virtual-environment_:

.. code-block:: shell

    $ python3 -m venv venv

3. Activate the virtual-environment:

.. code-block:: shell

    $ source venv/bin/activate

4. Install dependencies:

.. code-block:: shell

    $ pip install -r requirements/local.txt

.. _virtual-environment: https://docs.python.org/3/tutorial/venv.html

**Important**: from now on, all commands assume the virtual-environment is active.
If not, please make it so by following step 3.

Running
-------

In order to run the project, at minimum, the following environment variables must be set:

.. code-block:: shell

    $ export CELERY_BROKER_URL="<REDIS_CONNECTION_STRING>"
    $ export DATABASE_URL="<POSTGRESQL_CONNECTION_STRING>"
    $ export GITHUB_ACCESS_TOKEN="<GITHUB_PERSONAL_ACCESS_TOKEN>"

The values for ``CELERY_BROKER_URL`` and ``DATABASE_URL`` can be obtained by following the instructions on how to setup ``redis`` and ``postgresql-server`` respectively.
Please refer to their documentation for more information.

The value for ``GITHUB_ACCESS_TOKEN`` can be obtained by following this_ instructions

.. _this: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

Local Server
^^^^^^^^^^^^

.. code-block:: shell

    $ python manage.py runserver_plus

Testing
-------

.. code-block:: shell

    $ pytest

Code coverage
^^^^^^^^^^^^^

.. code-block:: shell

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Architecture
------------

Directory Structure
^^^^^^^^^^^^^^^^^^^

The directory structure was generated using `Django Cookie-Cutter`_ template. It looks as follows:

.. _Django Cookie-Cutter: https://github.com/pydanny/cookiecutter-django

.. code-block:: shell

    .
    ├── config
    │   └── settings
    ├── devproject
    │   ├── contrib
    │   │   └── sites
    │   │       └── migrations
    │   ├── core
    │   │   ├── api
    │   │   ├── management
    │   │   │   └── commands
    │   │   ├── migrations
    │   │   └── tests
    │   │       ├── selectors
    │   │       ├── services
    │   │       └── views
    │   ├── static
    │   │   ├── css
    │   │   ├── fonts
    │   │   ├── images
    │   │   │   └── favicons
    │   │   ├── js
    │   │   └── sass
    │   ├── templates
    │   │   ├── account
    │   │   ├── pages
    │   │   └── users
    │   ├── users
    │   │   ├── api
    │   │   ├── migrations
    │   │   └── tests
    │   └── utils
    ├── docs
    │   └── _source
    │       └── pycharm
    │           └── images
    ├── locale
    ├── requirements
    └── utility

Django Applications
^^^^^^^^^^^^^^^^^^^

The project consists of two Django sub-applications:

``devproject.core``
~~~~~~~~~~~~~~~~~~~

Holding business logic for "syncing" (scraping) developer and repository information from Github.

``devproject.users``
~~~~~~~~~~~~~~~~~~~~


Holding business logic for managing local users.

Business Logic
^^^^^^^^^^^^^^

The project follows `HackSoftware's Django Style-guide`_'s convention of storing business-logic-related operations and queries in ``services`` and ``selectors`` functions respectively. e.g:

.. code-block:: python

    # A service function:
    def sync_developer(*, login: str) -> Developer:
        """
        Retrieves user information from Github and creates or updates developer information locally.
        :param login:  Github username of the developer
        :return:
        """
        pass

    # A selector function:
    def get_registered_developers() -> "QuerySet[Developer]":
        """
        Retrieves a queryset with all the developers registered locally sorted by login.
        :return: a Developer queryset.
        """
        pass

Please refer to ``devproject/core/services.py`` and ``devproject/core/selectors.py`` for more information on how these functions are implemented.

.. _HackSoftware's Django Style-guide: https://github.com/HackSoftware/Django-Styleguide

Web API
^^^^^^^

The project loosely follows `HackSoftware's Django Style-guide`_'s convention for defining web API views.

Please refer to ``devproject/core/api/views.py`` for more information on how view functions are implemented.

Documentation
~~~~~~~~~~~~~

The project's web API is documented using `OpenAPI Specification`_ (f.k.a Swagger).

A developer-friendly renderization of the spec can be viewed by accessing ``http://localhost:8000/api/documentation``.
Here's a preview:

.. image:: https://raw.githubusercontent.com/francisbrito/tesorio-assignment/master/docs/_static/openapi.png
    :target: https://github.com/francisbrito/tesorio-assignment
    :alt: ReDoc

.. _`OpenAPI Specification`: https://swagger.io/specification/

Settings
--------

See settings_ for a list of available environment settings.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Migrations
^^^^^^^^^^

Creating migrations
~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    $ python manage.py makemigrations

Applying migrations
~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    $ python manage.py migrate

Syncing
^^^^^^^

Developers
~~~~~~~~~~

.. code-block:: shell

    $ python manage.py sync_developers user1 user2 user3 # ...

    # alternatively, in order to sync existing developers
    $ python manage.py sync_developers --registered

Repositories
~~~~~~~~~~~~

.. code-block:: shell

    $ python manage.py sync_repositories name1 name2 name2  # ...

    # alternatively, in order to sync existing repositories
    $ python manage.py sync_repositories --registered


Periodic Tasks
^^^^^^^^^^^^^^

In order to setup periodic (cron-like) tasks, run the following command:

.. code-block:: shell

    $ python manage.py setup_periodic_tasks

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy devproject

Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd devproject
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.




Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. If you choose to use `MailHog`_ when generating the project a local SMTP server with a web interface will be available.

#. `Download the latest MailHog release`_ for your OS.

#. Rename the build to ``MailHog``.

#. Copy the file to the project root.

#. Make it executable: ::

    $ chmod +x MailHog

#. Spin up another terminal window and start it there: ::

    ./MailHog

#. Check out `<http://127.0.0.1:8025/>`_ to see how it goes.

Now you have your own mail server running locally, ready to receive whatever you send it.

.. _`Download the latest MailHog release`: https://github.com/mailhog/MailHog/releases

.. _mailhog: https://github.com/mailhog/MailHog
