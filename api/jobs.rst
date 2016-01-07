.. _api-jobs:

========
Jobs API
========

The jobs API makes it easy to work with your spider's jobs and lets you schedule, stop, update and delete them.

.. include:: client_library.rst

jobs/run.json
-------------

Schedules a job for a given spider.

============ ====================================================================== ========
Parameter    Description                                                            Required
============ ====================================================================== ========
project      Project ID.                                                            Yes
job          Job ID.                                                                No
spider       Spider name.                                                           Yes
add_tag      Add specified tag to job                                               No
priority     Job priority. Supported values: 0 (lowest) to 4 (highest). Default: 2. No
job_settings JSON array of job settings.                                            No
============ ====================================================================== ========

.. note:: Any other parameter will be treated as a spider argument.

====== ============================== =======================================
Method Description                    Supported parameters
====== ============================== =======================================
POST   Schedule the specified spider. project, job, spider, add_tag, priority
====== ============================== =======================================

Example::

	$ curl -u APIKEY: https://dash.scrapinghub.com/api/run.json -d project=123 -d spider=somespider -d add_tag=sometag -d spiderarg1=example -d job_settings='{ "setting1": "value1", "setting2": "value2" }'
	{"status": "ok", "jobid": "123/1/1"}


jobs/list.{json,jl}
-------------------

Retrieve job information for a given project, spider, or specific job.

========= ==================================== ========
Parameter Description                          Required
========= ==================================== ========
project   Project ID.                          Yes
job       Job ID.                              No
spider    Spider name.                         No
state     Return jobs with specified state.    No
has_tag   Return jobs with specified tag.      No
lacks_tag Return jobs that lack specified tag. No
========= ==================================== ========

Supported ``state`` values: ``pending``, ``running``, ``finished``, ``deleted``.

====== ========================= ===============================================
Method Description               Supported parameters
====== ========================= ===============================================
GET    Retrieve job information. project, job, spider, state, has_tag, lacks_tag
====== ========================= ===============================================

Examples::

    # Retrieve the latest 3 finished jobs
    $ curl -u APIKEY: "https://dash.scrapinghub.com/api/jobs/list.json?project=123&spider=somespider&state=finished&count=3"
    {
      "status": "ok",
      "count": 3,
      "total": 3,
      "jobs": [
        {
          "responses_received": 1,
          "items_scraped": 2,
          "close_reason": "finished",
          "logs": 29,
          "tags": [],
          "spider": "somespider",
          "updated_time": "2015-11-09T15:21:06",
          "priority": 2,
          "state": "finished",
          "version": "1447064100",
          "spider_type": "manual",
          "started_time": "2015-11-09T15:20:25",
          "id": "123/45/14544",
          "errors_count": 0,
          "elapsed": 138399
        },
        {
          "responses_received": 1,
          "items_scraped": 2,
          "close_reason": "finished",
          "logs": 29,
          "tags": [
            "consumed"
          ],
          "spider": "somespider",
          "updated_time": "2015-11-09T14:21:02",
          "priority": 2,
          "state": "finished",
          "version": "1447064100",
          "spider_type": "manual",
          "started_time": "2015-11-09T14:20:25",
          "id": "123/45/14543",
          "errors_count": 0,
          "elapsed": 3433762
        },
        {
          "responses_received": 1,
          "items_scraped": 2,
          "close_reason": "finished",
          "logs": 29,
          "tags": [
            "consumed"
          ],
          "spider": "somespider",
          "updated_time": "2015-11-09T13:21:08",
          "priority": 2,
          "state": "finished",
          "version": "1447064100",
          "spider_type": "manual",
          "started_time": "2015-11-09T13:20:31",
          "id": "123/45/14542",
          "errors_count": 0,
          "elapsed": 7034158
        }
      ]
    }

    # Retrieve all running jobs
    $ curl -u APIKEY: "https://dash.scrapinghub.com/api/jobs/list.json?project=123&state=running"
    {
      "status": "ok",
      "count": 2,
      "total": 2,
      "jobs": [
        {
          "responses_received": 483,
          "items_scraped": 22,
          "logs": 20,
          "tags": [],
          "spider": "somespider",
          "elapsed": 17442,
          "priority": 2,
          "state": "running",
          "version": "1447064100",
          "spider_type": "manual",
          "started_time": "2015-11-09T15:25:07",
          "id": "123/45/13140",
          "errors_count": 0,
          "updated_time": "2015-11-09T15:26:43"
        },
        {
          "responses_received": 207,
          "items_scraped": 207,
          "logs": 468,
          "tags": [],
          "spider": "someotherspider",
          "elapsed": 4085,
          "priority": 3,
          "state": "running",
          "version": "1447064100",
          "spider_type": "manual",
          "started_time": "2015-11-09T13:00:46",
          "id": "123/67/11952",
          "errors_count": 0,
          "updated_time": "2015-11-09T15:26:57"
        }
      ]
    }


    # Retrieve all jobs with the tag ``consumed``
    $ curl -u APIKEY: "https://dash.scrapinghub.com/api/jobs/list.json?project=123&lacks_tag=consumed" 
    {
      "status": "ok",
      "count": 3,
      "total": 3,
      "jobs": [
        {
          "responses_received": 208,
          "items_scraped": 208,
          "logs": 471,
          "tags": ["sometag"],
          "spider": "somespider",
          "elapsed": 1010,
          "priority": 3,
          "state": "running",
          "version": "1447064100",
          "spider_type": "manual",
          "started_time": "2015-11-09T13:00:46",
          "id": "123/45/11952",
          "errors_count": 0,
          "updated_time": "2015-11-09T15:28:27"
        },
        {
          "responses_received": 619,
          "items_scraped": 22,
          "close_reason": "finished",
          "logs": 29,
          "tags": ["sometag"],
          "spider": "someotherspider",
          "updated_time": "2015-11-09T15:27:20",
          "priority": 2,
          "state": "finished",
          "version": "1447064100",
          "spider_type": "manual",
          "started_time": "2015-11-09T15:25:07",
          "id": "123/67/13140",
          "errors_count": 0,
          "elapsed": 67409
        },
        {
          "responses_received": 3,
          "items_scraped": 20,
          "close_reason": "finished",
          "logs": 58,
          "tags": ["sometag", "someothertag"],
          "spider": "yetanotherspider",
          "updated_time": "2015-11-09T15:25:28",
          "priority": 2,
          "state": "finished",
          "version": "1447064100",
          "spider_type": "manual",
          "started_time": "2015-11-09T15:25:07",
          "id": "123/89/1627",
          "errors_count": 0,
          "elapsed": 179211
        }
      ]
    }

Python::

  >>> project = hc.get_project('123')
  >>> jobs_metadata = project.jobq.list()
  >>> [j['key'] for j in jobs_metadata]
  ['1111111/1/3', '1111111/1/2', '1111111/1/1']

jobs/update.json
----------------

Updates information about jobs.

========== ============================== ========
Parameter  Description                    Required
========== ============================== ========
project    Project ID.                    Yes
job        Job ID.                        Yes
add_tag    Add specified tag to job.      No
remove_tag Remove specified tag from job. No
========== ============================== ========

====== ======================= =================================
Method Description             Supported parameters
====== ======================= =================================
POST   Update job information. project, job, add_tag, remove_tag
====== ======================= =================================

Example::

  $ curl -u APIKEY: https://dash.scrapinghub.com/api/jobs/update.json -d project=123 -d job=123/1/2 -d add_tag=consumed

Python::

  >>> job = hc.get_job('123/1/2')
  >>> job.update(add_tag='consumed')

jobs/delete.json
----------------

Deletes one or more jobs.

=========  ============================== ========
Parameter  Description                    Required
=========  ============================== ========
project    Project ID.                    Yes
job        Job ID.                        Yes
=========  ============================== ========

====== ============== =================================
Method Description    Supported parameters
====== ============== =================================
POST   Delete job(s). project, job
====== ============== =================================

Example::

  $ curl -u APIKEY: https://dash.scrapinghub.com/api/jobs/delete.json -d project=123 -d job=123/1/2 -d job=123/1/3

Python::

  >>> job = hc.get_job('123/1/2')
  >>> job.delete()
  1

jobs/stop.json
--------------

Stops one or more running jobs.

=========  ============================== ========
Parameter  Description                    Required
=========  ============================== ========
project    Project ID.                    Yes
job        Job ID.                        Yes
=========  ============================== ========

====== ============ =================================
Method Description  Supported parameters
====== ============ =================================
POST   Stop job(s). project, job
====== ============ =================================

Example::

  $ curl -u APIKEY: https://dash.scrapinghub.com/api/jobs/stop.json -d project=123 -d job=123/1/1 -d job=123/1/2

Python::

  >>> job = hc.get_job('123/1/1')
  >>> job.stop()
  True
