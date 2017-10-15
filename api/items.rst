.. _api-items:

=========
Items API
=========

.. note:: Even though these APIs support writing, they are most often used for reading. The crawlers running on Scrapinghub cloud are the ones that write to these endpoints. However, both operations are documented here for completion.

The Items API lets you interact with the items stored in the hubstorage backend for your projects. For example, you can download all the items for the job ``'53/34/7'`` through::

    $ curl -u APIKEY: https://storage.scrapinghub.com/items/53/34/7

.. include:: client_library.rst

Item object
-----------

=============== =======================================================================
Field           Description
=============== =======================================================================
_type           The item definition.
_template       The template matched against. Portia only.
_cached_page_id Cached page ID. Used to identify the scraped page in storage.
=============== =======================================================================

Scraped fields will be top level alongside the internal fields listed above.

items/:project_id[/:spider_id][/:job_id][/:item_no][/:field_name]
-----------------------------------------------------------------

Retrieve or insert items for a project, spider, or job. Where ``item_no`` is the index of the item.

========= ==================================================================== ========
Parameter Description                                                          Required
========= ==================================================================== ========
format    Results format. See :ref:`api-overview-resultformats`.               No
meta      Meta keys to show.                                                   No
nodata    If set, no data will be returned other than specified ``meta`` keys. No
========= ==================================================================== ========

.. note:: Pagination and meta parameters are supported, see :ref:`api-overview-pagination` and :ref:`api-overview-metapar`.

============= ==========================================================
Header        Description
============= ==========================================================
Content-Range Can be used to specify a start index when inserting items.
============= ==========================================================

====== =================================================== ====================
Method Description                                         Supported parameters
====== =================================================== ====================
GET    Retrieve items for a given project, spider, or job. format, meta, nodata
POST   Insert items for a given job                        N/A
====== =================================================== ====================

.. note:: Please always use pagination parameters (``start``, ``startafter`` and ``count``) to limit amount of items in response to prevent timeouts and different performance issues. See pagination examples below for more details.

.. _items-examples:

Examples
^^^^^^^^

**Retrieve all items from a given job**

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/items/53/34/7


**Retrive first item from a given job**

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/items/53/34/7/0


**Retrieve values from a single field**

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/items/53/34/7/fieldname


**Retrieve all items from a given spider**

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/items/53/34


**Retrieve all items from a given project**

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/items/53/

**[Pagination] Retrieve first N items from a given job**

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/items/53/34/7?count=10

**[Pagination] Retrieve N items from a given job starting from the given item**

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/items/53/34/7?count=10&start=53/34/7/20

**[Pagination] Retrieve N items from a given job starting from the item following to the given one**

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/items/53/34/7?count=10&startafter=53/34/7/19

**[Pagination] Retrieve a few items from a given job by their IDs**

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/items/53/34/7?index=5&index=6


**Get meta field from items**

To get only metadata from items, pass the ``nodata=1`` parameter along with the meta field that you want to get.

HTTP::

    $ curl -u APIKEY: "https://storage.scrapinghub.com/items/53/1/7?meta=_key&nodata=1"
    {"_key":"53/1/7/0"}
    {"_key":"53/1/7/1"}
    {"_key":"53/1/7/2"}

**Get items in a specific format**

Check the available formats in the :ref:`api-overview-resultformats` section at the API Overview.

JSON::

    $ curl -u APIKEY: "https://storage.scrapinghub.com/items/53/34/7?meta=_key&nodata=1 -H \"Accept: application/json\""
    [{"_key":"28144/1/1/0"},{"_key":"28144/1/1/1"},{"_key":"28144/1/1/2"}, ...]

JSON Lines::

    $ curl -u APIKEY: "https://storage.scrapinghub.com/items/53/34/7?meta=_key&nodata=1 -H \"Accept: application/x-jsonlines\""
    {"_key":"28144/1/1/0"}
    {"_key":"28144/1/1/1"}
    {"_key":"28144/1/1/2"}
    ...


**Add items to a job via POST**

Add the items stored in the file ``items.jl`` (JSON lines format) to the job ``53/34/7``::

    $ curl -u APIKEY: https://storage.scrapinghub.com/items/53/34/7 -X POST -T items.jl

Use the ``Content-Range`` header to specify a start index::

    $ curl -u APIKEY: https://storage.scrapinghub.com/items/53/34/7 -X POST -T items.jl -H "content-range: items 500-/*"

The API will only return ``200`` if the data was successfully stored. There's no limit on the amount of data you can send, but a ``HTTP 413`` response will be returned if any single item is over 1M.


items/:project_id/:spider_id/:job_id/stats
------------------------------------------

Retrieve the item stats for a given job.

=================== ==========================================
Field               Description
=================== ==========================================
counts[field]       The number of times the field was scraped.
totals.input_bytes  The total size of all items in bytes.
totals.input_values The total number of items.
=================== ==========================================

========= ================================= ========
Parameter Description                       Required
========= ================================= ========
all       Include hidden fields in results. No
========= ================================= ========

====== ========================================== ====================
Method Description                                Supported parameters
====== ========================================== ====================
GET    Retrieve item stats for the specified job. all
====== ========================================== ====================


Example
^^^^^^^

**Get the stats from a given job**

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/items/53/34/7/stats
    {"counts":{"field1":9350,"field2":514},"totals":{"input_bytes":14390294,"input_values":10000}}
