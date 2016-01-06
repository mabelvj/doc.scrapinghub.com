.. _api-requests:

============
Requests API
============

The requests API allows you to work with request and response data from your crawls.

.. include:: client_library.rst

Request object
--------------

======== ==================================== ========
Field    Description                          Required
======== ==================================== ========
parent   The index of the parent request.     No
duration Request duration in milliseconds.    Yes
status   HTTP response code.                  Yes
method   HTTP method. Default: GET            No
rs       Response size in bytes.              Yes
url      Request URL.                         Yes
fp       Request fingerprint.                 No
======== ==================================== ========

.. note:: Seed requests from start URLs will have no parent field.

requests/:project_id/:spider_id/:job_id
---------------------------------------

Retrieve or insert request data.

Examples
^^^^^^^^

**Get the requests from a given job**

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/requests/53/34/7
    {"parent":0,"duration":12,"status":200,"method":"GET","rs":1024,"url":"http://scrapy.org/","time":1351521736957}

Python (:ref:`python-hubstorage<api-overview-ep-storage>`)::

    >>> reqs = hc.get_job('53/34/7').requests.list()


.. note:: Pagination and meta parameters are supported, see :ref:`api-overview-pagination` and :ref:`api-overview-metapar`.

**Adding requests**

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/requests/53/34/7 -X POST -T requests.jl

Python (:ref:`python-hubstorage<api-overview-ep-storage>`)::

	>>> job = hc.get_job('53/34/7')
	>>> job.requests.add('http://scrapy.org/', 200, GET, 1024, 0, 12, 1351521736957)


requests/:project_id/:spider_id/:job_id/stats
---------------------------------------------

Retrieve request stats for a given job.

=================== ========================================
Field               Description
=================== ========================================
counts[field]       The number of times the field occurs.
totals.input_bytes  The total size of all requests in bytes.
totals.input_values The total number of requests.
=================== ========================================

Example
^^^^^^^

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/requests/53/34/7/stats
    {"counts":{"url":21,"parent":19,"status":21,"method":21,"rs":21,"duration":21,"fp":21},"totals":{"input_bytes":2397,"input_values":21}}

Python (:ref:`python-hubstorage<api-overview-ep-storage>`)::

    >>> print hc.get_job('53/34/7').requests.stats()


.. _`python-hubstorage`: http://github.com/scrapinghub/python-hubstorage
