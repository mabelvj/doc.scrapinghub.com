.. _api-collections:

===============
Collections API
===============

Scrapinghub's *Collections* provide a way to store an arbitrary number of records indexed by a key. They're often used by Scrapinghub projects as a single place to write information from multiple scraping jobs.

The *Collections API* allows storing arbitrary objects in named sets. For example::

    $ curl -u APIKEY: -X POST -d '{"_key": "foo", "value": "bar"}' \
        https://storage.scrapinghub.com/collections/78/s/my_collection

Will post an object to the ``my_collection`` collection. You can submit multiple objects by separating them with newlines. The ``_key`` field is required and used to identify the item and should be unique.

The ``/s/`` in the path represents the collection type. See below for more details. 

Collection types
----------------

In the above example,  The following
collection types are available:

====  ===================== ================================================================
Type  Full name             Description
====  ===================== ================================================================
s     store                 Basic set store
cs    cached store          Items expire after a month
vs    versioned store       Up to 3 copies of each item will be retained
vcs   versioned cache store Multiple copies are retained, and each one expires after a month
====  ===================== ================================================================

collections/:project_id/:type/:collection
-----------------------------------------

Read or write items from or to a collection.

=========== ========================================================= ========
Parameter   Description                                               Required
=========== ========================================================= ========
key         Read items with specified key. Multiple values supported. No
prefix      Read items with specified key prefix.                     No
prefixcount Maximum number of values to return per prefix.            No
startts     UNIX timestamp at which to begin results.                 No
endts       UNIX timestamp at which to end results.                   No
=========== ========================================================= ========

====== ========================================= ========================================
Method Description                               Supported parameters
====== ========================================= ========================================
GET    Read items from the specified collection. key, prefix, prefixcount, startts, endts
POST   Write items to the specified collection.
====== ========================================= ========================================

.. note:: Pagination and meta parameters are supported, see :ref:`api-overview-pagination` and :ref:`api-overview-metapar`.

GET examples::

    $ curl -u APIKEY: "https://storage.scrapinghub.com/collections/78/s/my_collection?key=foo1&key=foo2"
    {"value":"bar1"}
    {"value":"bar2"}
    $ curl -u APIKEY: https://storage.scrapinghub.com/collections/78/s/my_collection?prefix=f
    {"value":"bar"}
    $ curl -u APIKEY: "https://storage.scrapinghub.com/collections/78/s/my_collection?startts=1402699941000&endts=1403039369570"
    {"value":"bar"}

Prefix filters, unlikely other filters, use indexes and should be used when possible. You can use the ``prefixcount`` parameter to limit the number of values returned for each prefix.

A common pattern is to download changes within a certain time period. You can use the ``startts`` and ``endts`` parameters to select records within a certain time window.

The current timestamp can be retrieved like so::

    $ curl https://storage.scrapinghub.com/system/ts
    1403039369570

.. note:: Timestamp filters may perform poorly when selecting a small number of records from a large collection.


collections/:project_id/:type/:collection/:item
-----------------------------------------------

Read an individual item.

GET example::

    $ curl -u APIKEY: https://storage.scrapinghub.com/collections/78/s/my_collection/foo
    {"value":"bar"}

collections/:project_id/:type/:collection/:item/value
-----------------------------------------------------

Read an individual item value.

GET example::

    $ curl -u APIKEY: https://storage.scrapinghub.com/collections/78/s/my_collection/foo/value
    bar
