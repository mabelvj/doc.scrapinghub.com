.. _api-jobmeta:

================
Job metadata API
================

The Job metadata API allows you to get metadata for the given jobs.

.. include:: client_library.rst

jobs/:project_id/:spider_id/:job_id[/:field_name]
------------------------------------------------

Retrieve job data or specific meta field.

Examples
^^^^^^^^

**Get metadata for the job**

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/jobs/1/2/3

    {
        "close_reason": "finished",
        "completed_by": "jobrunner",
        "deploy_id": 1,
        "finished_time": 1566311833872,
        "pending_time": 1566311800654,
        "priority": 2,
        "project": 1,
        "running_time": 1566311801163,
        "scheduled_by": "testuser",
        "scrapystats": {
            "downloader/request_bytes": 594,
            "downloader/request_count": 2,
            "downloader/request_method_count/GET": 2,
            "downloader/response_bytes": 1866,
            "downloader/response_count": 2,
            "downloader/response_status_count/200": 1,
            "downloader/response_status_count/404": 1,
            "elapsed_time_seconds": 3.211014,
            "finish_reason": "finished",
            "finish_time": 1566311822568.0,
            "item_scraped_count": 1,
            "log_count/DEBUG": 3,
            "log_count/INFO": 11,
            "log_count/WARNING": 1,
            "memusage/max": 72433664,
            "memusage/startup": 72433664,
            "response_received_count": 2,
            "robotstxt/request_count": 1,
            "robotstxt/response_count": 1,
            "robotstxt/response_status_count/404": 1,
            "scheduler/dequeued": 1,
            "scheduler/dequeued/disk": 1,
            "scheduler/enqueued": 1,
            "scheduler/enqueued/disk": 1,
            "start_time": 1566311819357.0
        },
        "spider": "testspider",
        "spider_args": {"arg1": "val1", "arg2": "val2"},
        "spider_type": "manual",
        "started_by": "jobrunner",
        "state": "finished",
        "tags": [
            "tag1",
            "tag2"
        ],
        "units": 2,
        "version": "6d32f52-master"
    }


.. note:: Please consider the example response with caution. Some of the fields
appear only on specific conditions: for example, after finishing/deleting or
restoring a job. Some other highly depend on specific spider and the job outcome.
There also might be some additional fields for internal use only which can be
changed at any given moment without prior notice. 

**Get specific metadata field for the job**

HTTP::

    $ curl -u APIKEY: https://storage.scrapinghub.com/jobs/1/2/3/tags

    [
        "tag1",
        "tag2"
    ]