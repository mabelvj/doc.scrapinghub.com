.. _api-jobq:

========
JobQ API
========

The JobQ API allows you to retrieve finished jobs from the queue.

.. include:: client_library.rst

jobq/:project_id/count
----------------------

Count the jobs for the specified project.

========= ========================================================== ========
Parameter Description                                                Required
========= ========================================================== ========
spider    Filter results by spider name.                             No
state     Filter results by state (pending/running/finished/deleted) No
startts   UNIX timestamp at which to begin results, in millisecons.  No
endts     UNIX timestamp at which to end results, in millisecons.    No
has_tag   Filter results by existing tags                            No
lacks_tag Filter results by missing tags                             No
========= ========================================================== ========

.. hint:: It's possible to repeat ``has_tag``, ``lacks_tag`` multiple times. In this case ``has_tag`` works as an ``OR`` operation, while ``lacks_tag`` works as an ``AND`` operation.

HTTP (assuming only 2 jobs, where 1st one is marked with ``tagA``, 2nd - with ``tagB``)::

    $ curl -u APIKEY: "https://storage.scrapinghub.com/jobq/53/count"
    2
    $ curl -u APIKEY: "https://storage.scrapinghub.com/jobq/53/count?has_tag=tagA&has_tag=tagB"
    2
    $ curl -u APIKEY: "https://storage.scrapinghub.com/jobq/53/count?lacks_tag=tagA&lacks_tag=tagB"
    0

====== ===================================== =================================================
Method Description                           Supported parameters
====== ===================================== =================================================
GET    Count jobs for the specified project. spider, state, startts, endts, has_tag, lacks_tag
====== ===================================== =================================================

**Count jobs for a given project**

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/jobq/53/count
    32110

jobq/:project_id/list
---------------------

Lists the jobs for the specified project, in order from most recent to last.

===== =================================================
Field Description
===== =================================================
ts    The time at which the job was added to the queue.
===== =================================================

========= ========================================================== ========
Parameter Description                                                Required
========= ========================================================== ========
spider    Filter results by spider name.                             No
state     Filter results by state (pending,running,finished,deleted) No
startts   UNIX timestamp at which to begin results, in millisecons.  No
endts     UNIX timestamp at which to end results, in millisecons.    No
count     Limit results by a given number of jobs                    No
start     Skip N first jobs from results                             No
stop      The job key at which to stop showing results.              No
key       Get job data for a given set of job keys                   No
has_tag   Filter results by existing tags                            No
lacks_tag Filter results by missing tags                             No
========= ========================================================== ========

====== ==================================== ====================
Method Description                          Supported parameters
====== ==================================== ====================
GET    List jobs for the specified project. startts, endts, stop
====== ==================================== ====================

Examples
^^^^^^^^

**List jobs for a given project**

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/jobq/53/list
    {"key":"53/7/81","ts":1397762393489}
    {"key":"53/7/80","ts":1395111612849}
    {"key":"53/7/78","ts":1393972804722}
    {"key":"53/7/77","ts":1393972734215}

Python (:ref:`python-hubstorage<api-overview-ep-storage>`)::

    >>> jobs = hc.get_project('53').jobq.list()


**List jobs finished between two timestamps**

If you pass the ``startts`` and ``endts`` parameters, the API will return only the jobs finished between them.

HTTP::

    $ curl -u APIKEY: "https://storage.scrapinghub.com/jobq/53/list?startts=1359774955431&endts=1359774955440"
    {"key":"53/6/7","ts":1359774955439}
    {"key":"53/3/3","ts":1359774955437}
    {"key":"53/9/1","ts":1359774955431}

Python (:ref:`python-hubstorage<api-overview-ep-storage>`)::

    >>> jobs = hc.get_project('53').jobq.list(startts=1359774955431, endts=1359774955440)



**Retrieve jobs finished after some job**

JobQ returns the list of jobs, with the most recently finished first. We recommend associating the key of the most recently finished job with the downloaded data. When you want to update your data later on, you can list the jobs and stop at the previously downloaded job, through the ``stop`` parameter.

Using HTTP::

    $ curl -u APIKEY: "https://storage.scrapinghub.com/jobq/53/list?stop=53/7/81"
    {"key":"53/7/83","ts":1403610146780}
    {"key":"53/7/82","ts":1397827910849}

Using Python (:ref:`python-hubstorage<api-overview-ep-storage>`)::

    >>> jobs = hc.get_project('53').jobq.list(stop='53/7/81')


.. _`python-hubstorage`: http://github.com/scrapinghub/python-hubstorage
