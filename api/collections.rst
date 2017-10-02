.. _api-collections:

===============
Collections API
===============

Scrapinghub's *Collections* are key-value stores for arbitrary large
number of records. They are especially useful to store information
produced and/or used by multiple scraping jobs.

.. note:: The frontier API is best suited to store queues of urls
          to be processed by scraping jobs.


Quickstart
==========

A **collection** is identified by a *project id*, a *type* and a *name*.
A **record** can be any json dictionnary. They are identified by a ``_key`` field.

*In the following we use project id* ``78`` *, the regular storage type* ``s``
*for the collection named* ``my_collection``.

.. note:: Avoid using multiple collections with the same name and different type like ``/s/my_collection`` and ``/cs/my_collection``. During operations on an entire collection, like renaming or deleting, Hubstorage will treat homonyms as a single entity and rename or delete both.


Create/Update a record:
-----------------------

.. code:: shell

    $ curl -u $APIKEY: -X POST -d '{"_key": "foo", "value": "bar"}' \
        https://storage.scrapinghub.com/collections/78/s/my_collection


Access a record:
----------------

.. code:: shell

    $ curl -u $APIKEY: -X GET \
        https://storage.scrapinghub.com/collections/78/s/my_collection/foo


Delete a record:
----------------

.. code:: shell

    $ curl -u $APIKEY: -X DELETE \
        https://storage.scrapinghub.com/collections/78/s/my_collection/foo


List records:
-------------

.. code:: shell

    $ curl -u $APIKEY: -X GET \
        https://storage.scrapinghub.com/collections/78/s/my_collection


Create/Update multiple records:
-------------------------------

We use the ``jsonline`` format by default (json objects separated by a newline):

.. code:: shell

    $ curl -u $APIKEY: -X POST -d '{"_key": "foo", "value": "bar"}\n{"_key": "goo", "value": "baz"}' \
        https://storage.scrapinghub.com/collections/78/s/my_collection


=======
Details
=======

The following collection types are available:

====  ===================== ========================== ================================================================
Type  Full name             Hubstorage method          Description
====  ===================== ========================== ================================================================
s     store                 new_store                  Basic set store
cs    cached store          new_cached_store           Items expire after a month
vs    versioned store       new_versioned_store        Up to 3 copies of each item will be retained
vcs   versioned cache store new_versioned_cached_store Multiple copies are retained, and each one expires after a month
====  ===================== ========================== ================================================================

.. note:: Avoid using multiple collections with the same name and different type like ``/s/my_collection`` and ``/cs/my_collection``. During operations on an entire collection, like renaming or deleting, Hubstorage will treat homonyms as a single entity and rename or delete, both.

Records are ``json`` objects, with the following constraints:

- Their serialized size can't be larger than ``10Mo``;
- Javascript's ``inf`` values are not supported;
- Floating-point numbers can't be larger than ``2^64 - 1``.


API
===

collections/:project_id/list
----------------------------

List all collections.

.. code:: shell

    $ curl -u APIKEY: https://storage.scrapinghub.com/collections/78/list
    {"type":"s","name":"my_collection"}
    {"type":"s","name":"my_collection_2"}
    {"type":"cs","name":"my_other_collection"}


collections/:project_id/:type/:collection
-----------------------------------------

Read, write or remove items in a collection.

=========== ========================================================== ========
Parameter   Description                                                Required
=========== ========================================================== ========
key         Read items with specified key. Multiple values supported.  No
prefix      Read items with specified key prefix.                      No
prefixcount Maximum number of values to return per prefix.             No
startts     UNIX timestamp at which to begin results, in milliseconds. No
endts       UNIX timestamp at which to end results, in milliseconds.   No
=========== ========================================================== ========

====== =========================================== ===========================================================
Method Description                                 Supported parameters
====== =========================================== ===========================================================
GET    Read items from the specified collection.   key, prefix, prefixcount, startts, endts
POST   Write items to the specified collection.
DELETE Delete items from the specified collection. key, prefix, prefixcount, startts, endts
====== =========================================== ===========================================================

.. note:: Pagination and meta parameters are supported,
          see :ref:`api-overview-pagination` and :ref:`api-overview-metapar`.

GET examples::

    $ curl -u APIKEY: "https://storage.scrapinghub.com/collections/78/s/my_collection?key=foo1&key=foo2"
    {"value":"bar1"}
    {"value":"bar2"}
    $ curl -u APIKEY: https://storage.scrapinghub.com/collections/78/s/my_collection?prefix=f
    {"value":"bar"}
    $ curl -u APIKEY: "https://storage.scrapinghub.com/collections/78/s/my_collection?startts=1402699941000&endts=1403039369570"
    {"value":"bar"}

Prefix filters, unlike other filters, use indexes and should be used
when possible. You can use the ``prefixcount`` parameter to limit the
number of values returned for each prefix.

A common pattern is to download changes within a certain time period.
You can use the ``startts`` and ``endts`` parameters to select records
within a certain time window.

The current timestamp can be retrieved like so::

    $ curl https://storage.scrapinghub.com/system/ts
    1403039369570

.. note:: Timestamp filters may perform poorly when selecting a small number
          of records from a large collection.


collections/:project_id/:type/:collection/count
-----------------------------------------------

Count the number of items in a collection.

.. code:: shell

    $ curl -u APIKEY: https://storage.scrapinghub.com/collections/78/s/my_collection/count
    {"count":972,"scanned":972}%

If the collection is large, the result may contain a ``nextstart`` field that
is used for pagination, see :ref:`api-overview-pagination`.


collections/:project_id/:type/:collection/:item
-----------------------------------------------

Read Write or Delete an individual item.

====== ===========================================
Method Description
====== ===========================================
GET    Read the item with the given key
POST   Write the item with the given key
DELETE Delete the item with the given key
====== ===========================================

.. code:: shell

    $ curl -u $APIKEY: https://storage.scrapinghub.com/collections/78/s/my_collection/foo
    {"value":"bar"}


collections/:project_id/:type/:collection/:item/value
-----------------------------------------------------

Read an individual item value.

.. code:: shell

    $ curl -u APIKEY: https://storage.scrapinghub.com/collections/78/s/my_collection/foo/value
    bar


collections/:project_id/:type/:collection/deleted
-----------------------------------------------------

``POST`` with a list of item key to delete them.

.. note:: This endpoint is designed to delete a large number of
          non-consecutive items. To delete consecutives items
          prefer the faster ``DELETE`` based endpoints.

.. code:: shell

    $ curl -u $APIKEY: -X POST -d 'TODO' \
        https://storage.scrapinghub.com/collections/78/s/my_collection/deleted

collections/:project_id/delete?name=:collection
-----------------------------------------------

Delete an entire collection immediately.

.. code:: shell

    $ curl -u APIKEY: -X POST https://storage.scrapinghub.com/collections/78/delete?name=my_collection

collections/:project_id/rename?name=:collection&new_name=:new_name
------------------------------------------------------------------

Rename a collection and move all its items immediately.

.. code:: shell

    $ curl -u APIKEY: -X POST https://storage.scrapinghub.com/collections/rename?name=my_collection&new_name=my_collection_renamed
