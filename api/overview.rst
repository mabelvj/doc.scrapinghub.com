.. _api-overview:

===============
Scrapinghub API
===============

Scrapinghub's API provides an interface for interacting with your spiders, jobs and scraped data.

Getting started
===============

Authentication
--------------

You'll need to authenticate using your `API key <https://dash.scrapinghub.com/account/apikey>`_. 

There are two ways to authenticate:

HTTP Basic::

	$ curl -u APIKEY: https://storage.scrapinghub.com/foo

URL Parameter::

    $ curl https://storage.scrapinghub.com/foo?apikey=APIKEY

Example
-------

Scheduling a spider is simple::

	$ curl -u APIKEY: https://dash.scrapinghub.com/api/schedule.json -d project=PROJECT -d spider=SPIDER

Where ``APIKEY`` is your API key, ``PROJECT`` is the spider's project ID, and ``SPIDER`` is the name of the spider you want to schedule.


Endpoints
=========

.. _api-overview-ep-dash:

dash.scrapinghub.com
---------------------

.. toctree::
   :maxdepth: 2

   comments
   eggs
   jobs

You can use the `python-scrapinghub <https://github.com/scrapinghub/python-scrapinghub>`_ library to interface with these endpoints. To install with pip::

	$ pip install scrapinghub

.. _api-overview-ep-storage:

storage.scrapinghub.com
-----------------------

.. toctree::
   :maxdepth: 2

   activity
   collections
   frontier
   items
   jobq
   logs
   requests

You can use the `python-hubstorage <https://github.com/scrapinghub/python-hubstorage>`_ library to interface with these endpoints. To install with pip::

	$ pip install hubstorage

.. _api-overview-pagination:

Pagination
==========

You can paginate the results for the majority of the APIs using a number of parameters.

========= ====================================================================
Parameter Description
========= ====================================================================
start     The offset from which to start retrieving results.
count     Number of results per page.
index     Can be used to retrieve specific records. Multiple values supported.
========= ====================================================================

.. _api-overview-resultformats:

Result formats
==============

There are two ways to specify the format of results: Using the ``Accept`` header, or using the ``format`` parameter.

The ``Accept`` header supports the following values:

* application/x-jsonlines
* application/json
* application/xml
* text/plain
* text/csv

The ``format`` parameter supports the following values:

* json
* jl
* xml
* csv
* text

`XML-RPC data types <http://en.wikipedia.org/wiki/XML-RPC#Data_types>`_ are used for XML output.

CSV parameters
--------------

================ ======================================================================= ========
Parameter        Description                                                             Required
================ ======================================================================= ========
fields           Comma delimited list of fields to include, in order from left to right. Yes
include_headers  When set to '1' or 'Y', show header names in first row.                 No
sep              Separator character.                                                    No
quote            Quote character.														 No
escape           Escape character.														 No
lineend          Line end string.													     No
================ ======================================================================= ========

When using CSV, you will need to specify the ``fields`` parameter to indiciate required fields and their order. Example::

    $ curl -u APIKEY: "https://storage.scrapinghub.com/items/53/34/7?format=csv&fields=id,name&include_headers=1"

Headers
=======

*gzip* compression is supported. A client can specify that *gzip* responses can be handled using the ``accept-encoding: gzip`` request header. ``content-encoding: gzip`` header must be present in the response to signal the *gzip* content encoding.

You can use the ``saveas`` request parameter to specify a filename for browser downloads. For example, specifying ``?saveas=foo.json`` will cause a header of ``Content-Disposition: Attachment; filename=foo.json`` to be returned.

.. _api-overview-metapar:

Meta parameters
===============

You can use the ``meta`` parameter to return metadata for the record in addition to its core data.

The following values are available:

=========  =======================================================================
Parameter  Description
=========  =======================================================================
_key       The item key in the format ``:project_id/:spider_id/:job_id/:item_no``.
_ts        Timestamp in milliseconds for when the item was added.
=========  =======================================================================

Example::

    $ curl "https://storage.scrapinghub.com/items/53/34/7?meta=_key&meta=_ts"
    {"_key":"1111111/1/1/0","_ts":1342078473363, ... }

.. note:: If the data contains fields with the same name as the requested fields, they will both appear in the result.
