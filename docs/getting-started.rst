Getting Started
===============

To install the most recent stable release:

.. code-block:: shell

    pip install wt-django-tools

To install the development branch from GitHub:

.. code-block:: shell

    pip install -e "wt-django-tools @ git+https://github.com/ian-wt/wt-django-tools.git@master"

Once installed, add ``wt_tools`` to ``INSTALLED_APPS`` in your ``settings.py`` module.

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'wt_tools',
    ]

.. note::

    While adding ``wt_tools`` to ``INSTALLED_APPS`` is the easiest way to get up and running,
    this isn't required for many of the included tools.
