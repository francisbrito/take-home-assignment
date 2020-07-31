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
     :alt: GitHub top language

.. image:: https://img.shields.io/github/license/francisbrito/tesorio-assignment
     :alt: GitHub

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

Testing
-------

Code coverage
^^^^^^^^^^^^^

Settings
--------

See settings_ for a list of available environment settings.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

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
