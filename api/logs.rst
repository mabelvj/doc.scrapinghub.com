.. _api-logs:

Logs API
========

The logs API lets you work with logs from your crawls.

Log object
----------

======= ===================================================
Field   Description
======= ===================================================
message Log message.
level   Log level as defined in the Python logging library.
time    UNIX timestamp of the message.
======= ===================================================

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

Python::

	>>> job = hc.get_job('123/5/1')
	>>> logs = job.logs.iter_values(count=10)
	>>> for log in logs:
	...     print(log)
	...
	{u'_key': u'123/5/1/0', u'message': u'Log opened.', u'level': 20, u'time': 1451863263099}
	{u'_key': u'123/5/1/1', u'message': u'[scrapy.log] Scrapy 1.0.3.post6+g2d688cd started', u'level': 20, u'time': 1451863263103}

Submitting logs
~~~~~~~~~~~~~~~

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/logs/53/34/7 -X POST -T log.jl
