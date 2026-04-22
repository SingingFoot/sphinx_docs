Getting Started with the SDK
=============================

Welcome to the **RedCore SDK** quickstart guide. This page will help you set up your development environment and make your first API call in minutes.

.. contents:: Table of Contents
   :depth: 2
   :local:
   :backlinks: none

Prerequisites
-------------

Before diving into the code, ensure you have the following ready:

* **Python 3.8+** installed on your machine.
* A valid ``API_KEY`` from the `RedCore Dashboard <https://example.com/dashboard>`_.
* A basic understanding of RESTful services.

Installation
------------

The easiest way to get started is by installing the SDK via ``pip``. We recommend using a **virtual environment** to keep your dependencies clean.

.. code-block:: bash

   # Create a virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install the SDK
   pip install redcore-sdk

Basic Configuration
-------------------

To initialize the client, you need to provide your credentials. You can set them as environment variables or pass them directly to the constructor.

.. important::
   Never hardcode your secrets in public repositories. Use environment variables instead.

.. code-block:: python
   :caption: app.py
   :emphasize-lines: 4

   from redcore import Client

   # Initialize the SDK client
   client = Client(api_key="YOUR_SECRET_KEY")

   print("SDK is ready to go!")

Your First Request
------------------

Here is a quick example of how to fetch your profile information:

.. code-block:: python

   try:
       user = client.users.get_me()
       print(f"Logged in as: {user.name}")
   except Exception as e:
       print(f"Error: {e}")

Next Steps
----------

Now that you're set up, consider exploring these sections:

:doc:`/sdk/authentication`
    Learn about different auth methods, including **OAuth** and **SAML**.

:doc:`/sdk/api_endpoints`
    A full reference of available methods and data models.

.. seealso::
   Check out our :ref:`architecture` diagrams for a high-level overview of how the SDK interacts with our servers.
