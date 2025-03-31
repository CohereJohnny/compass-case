Getting Started
===============

This guide provides a quick introduction to the Cohere Compass SDK and demonstrates how to perform basic operations.

Installation
-----------

Install the SDK using pip:

.. code-block:: bash

   pip install compass-sdk

Alternatively, you can install from source:

.. code-block:: bash

   git clone https://github.com/cohere-ai/compass-sdk.git
   cd compass-sdk
   pip install -e .

Configuration
------------

To use the SDK, you'll need to configure it with your Compass API credentials. The recommended way is to use environment variables:

.. code-block:: bash

   # API URLs
   export COMPASS_API_URL=https://your-compass-api-url
   export COMPASS_PARSER_URL=https://your-compass-parser-url
   
   # Authentication tokens
   export COMPASS_API_BEARER_TOKEN=your-api-token
   export COMPASS_PARSER_BEARER_TOKEN=your-parser-token

Alternatively, you can use a .env file:

.. code-block:: bash

   # .env
   COMPASS_API_URL=https://your-compass-api-url
   COMPASS_PARSER_URL=https://your-compass-parser-url
   COMPASS_API_BEARER_TOKEN=your-api-token
   COMPASS_PARSER_BEARER_TOKEN=your-parser-token

And then load it in your code:

.. code-block:: python

   import dotenv
   dotenv.load_dotenv()

Creating a Client
----------------

To interact with the Compass API, you'll need to create a client:

.. code-block:: python

   import os
   from cohere_compass.clients import CompassClient
   
   client = CompassClient(
       index_url=os.environ.get("COMPASS_API_URL"),
       bearer_token=os.environ.get("COMPASS_API_BEARER_TOKEN")
   )

Basic Operations
--------------

Here are some basic operations you can perform with the client:

Listing Indexes
~~~~~~~~~~~~~~

.. code-block:: python

   # List all indexes
   response = client.list_indexes()
   
   if response.error:
       print(f"Error: {response.error}")
   else:
       indexes = response.result["indexes"]
       for idx in indexes:
           print(f"Index: {idx['name']}, Documents: {idx['parent_doc_count']}, Chunks: {idx['count']}")

Creating an Index
~~~~~~~~~~~~~~~

.. code-block:: python

   # Create a new index
   from cohere_compass.models.config import IndexConfig
   
   config = IndexConfig(
       embedding_model="embed-english-v3.0",
       max_chunks_per_doc=100
   )
   
   response = client.create_index(
       index_name="my-new-index",
       index_config=config
   )
   
   if response.error:
       print(f"Error: {response.error}")
   else:
       print("Index created successfully")

Next Steps
---------

Now that you're familiar with the basics, you can explore more advanced functionality:

* :doc:`/guides/working_with_indexes` - Learn more about creating and managing indexes
* :doc:`/guides/document_processing` - Learn how to process and index documents
* :doc:`/guides/search_and_retrieval` - Learn how to search for content in your indexes 