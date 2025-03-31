.. Cohere Compass SDK documentation master file, created by
   sphinx-quickstart on Wed Mar 26 23:47:45 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Cohere Compass SDK Documentation
===========================================

The Cohere Compass SDK provides a Python interface for interacting with the Cohere Compass API, allowing developers to manage indexes, process documents, search content, and control access to their knowledge bases.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   guides/getting_started
   guides/working_with_indexes
   guides/document_processing
   guides/search_and_retrieval
   guides/access_control
   
   api/clients
   api/models
   api/utilities
   api/exceptions
   
   examples/basic_operations
   examples/advanced_search
   examples/data_sources

Features
--------

* Index creation and management
* Document processing and parsing
* Advanced search and retrieval
* Access control and authorization
* Data source integration

Installation
-----------

.. code-block:: bash

   pip install compass-sdk

Quick Start
----------

.. code-block:: python

   import os
   from cohere_compass.clients import CompassClient
   
   # Initialize the client
   client = CompassClient(
       index_url=os.environ.get("COMPASS_API_URL"),
       bearer_token=os.environ.get("COMPASS_API_BEARER_TOKEN")
   )
   
   # List all indexes
   response = client.list_indexes()
   
   # Display indexes
   if response.result and "indexes" in response.result:
       for idx in response.result["indexes"]:
           print(f"Index: {idx['name']}, Documents: {idx['parent_doc_count']}")

Web Interface
------------

The SDK also includes a web-based test harness that allows interactive testing of the API. To launch it:

.. code-block:: bash

   compass-web-interface --port 8000

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
