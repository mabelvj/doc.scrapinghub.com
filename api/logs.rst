.. _api-logs:

Logs API
========

The logs API lets you work with logs from your crawls.

.. _log-object:

Log object
----------

======= ==================================================================== ========
Field   Description                                                          Required
======= ==================================================================== ========
message Log message.                                                         Yes
level   Integer log level as defined in the :ref:`table <log-levels>` below. Yes
time    UNIX timestamp of the message, in milliseconds.                      No
======= ==================================================================== ========

.. _log-levels:

Log levels
~~~~~~~~~~

===== =========
Value Log level
===== =========
10    DEBUG
20    INFO
30    WARNING
40    ERROR
50    CRITICAL
===== =========

logs/:project_id/:spider_id/:job_id
-----------------------------------

Retrieve or upload logs for a given job.

========= ====================================================== ========
Parameter Description                                            Required
========= ====================================================== ========
format    Results format. See :ref:`api-overview-resultformats`. No
========= ====================================================== ========

====== ============== ====================
Method Description    Supported parameters
====== ============== ====================
GET    Retrieve logs. format
POST   Upload logs.
====== ============== ====================

Retrieving logs
~~~~~~~~~~~~~~~

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/logs/1111111/1/1/
    {"time":1444822757227,"level":20,"message":"Log opened."}
    {"time":1444822757229,"level":20,"message":"[scrapy.log] Scrapy 1.0.3.post6+g2d688cd started"}


Submitting logs
~~~~~~~~~~~~~~~

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/logs/53/34/7 -X POST -T log.jl
