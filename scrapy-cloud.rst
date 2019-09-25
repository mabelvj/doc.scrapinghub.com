.. _scrapycloud:

================
Scrapy Cloud API
================

.. note:: Check also the `Help Center`_ for general guides and articles.

Scrapy Cloud provides an HTTP API for interacting with your spiders, jobs and scraped data.

Getting started
===============

Authentication
--------------

You'll need to authenticate using your `API key <https://app.scrapinghub.com/account/apikey>`_.

There are two ways to authenticate:

HTTP Basic::

    $ curl -u APIKEY: https://storage.scrapinghub.com/foo

URL Parameter::

    $ curl https://storage.scrapinghub.com/foo?apikey=APIKEY

Example
-------

Running a spider is simple::

    $ curl -u APIKEY: https://app.scrapinghub.com/api/run.json -d project=PROJECT -d spider=SPIDER

Where ``APIKEY`` is your API key, ``PROJECT`` is the spider's project ID, and ``SPIDER`` is the name of the spider you want to run.

It's possible to override Scrapy settings for a job::

    $ curl -u APIKEY: https://app.scrapinghub.com/api/run.json -d project=PROJECT -d spider=SPIDER \
        -d job_settings='{"LOG_LEVEL": "DEBUG"}'

``job_settings`` should be a valid JSON and will be merged with project and spider settings provided for given spider.


API endpoints
=============

.. _api-overview-ep-dash:

app.scrapinghub.com
-------------------

.. toctree::
   :maxdepth: 2

   api/jobs
   api/comments

.. _api-overview-ep-storage:

storage.scrapinghub.com
-----------------------

.. toctree::
   :maxdepth: 2

   api/jobq
   api/jobmeta
   api/items
   api/logs
   api/requests
   api/activity
   api/collections
   api/frontier

.. _python-client:

Python client
-------------

You can use the `python-scrapinghub`_ library to interact with Scrapy Cloud API.
Check the `documentation`__ for installation instructions and usage examples.

.. _python-scrapinghub: https://github.com/scrapinghub/python-scrapinghub
__ https://python-scrapinghub.readthedocs.io/

.. _api-overview-pagination:

Pagination
==========

You can paginate the results for the majority of the APIs using a number of parameters.
The pagination parameters differ depending on the target host for a given endpoint.

app.scrapinghub.com
-------------------

========== ==================================================================
Parameter  Description
========== ==================================================================
count      Number of results per page.
offset     Offset to retrieve specific records.
========== ==================================================================

storage.scrapinghub.com
-----------------------

========== ==================================================================
Parameter  Description
========== ==================================================================
count      Number of results per page.
index      Offset to retrieve specific records. Multiple values supported.
start      Skip results before the given one. See a note about format below.
startafter Return results after the given one. See a note about format below.
========== ==================================================================

.. note:: The parameters naming inconsistency is caused by historical reasons and will be fixed in the coming platform updates.

.. note:: While ``index`` parameter is just a short ``<entity_id>`` (ex: ``index=4``), ``start`` and ``startafter`` parameters should have the full form ``<project_id>/<spider_id>/<job_id>/<entity_id>`` (ex: ``start=1/2/3/4``, ``startafter=1/2/3/3``).

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

.. _Help center: https://support.scrapinghub.com/support/home
