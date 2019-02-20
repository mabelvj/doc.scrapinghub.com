.. _crawlera-stats:

==================
Crawlera Stats API
==================

Use the stats HTTP API to access crawlera usage data.

Authentication
==============

This API uses HTTP Basic authentication. You’ll need to use your `API key <https://app.scrapinghub.com/account/apikey>`_.

API endpoints
=============

root url: "crawlera-stats.scrapinghub.com"

/stats
-----

Crawlera usage stats.

Stats object
------------

============ ===============================================
Field        Description
============ ===============================================
time_gte     Start of interval. ISO 8601 formatted date
clean        Number of successful responses
failed       Number of unsuccessful responses
concurrency  80 percentile of concurrent connections
total_time   80 percentile of response time (milliseconds)
traffic      Total traffic (bytes)
============ ================================================

Parameters
----------

=========== ======================================================== ========
Field       Description                                              Required
=========== ======================================================== ========
start_date  ISO 8601 formatted date. Defaults to 7 days ago from now No
end_date    ISO 8601 formatted date. Defaults to UTC now             No
groupby     How to group results. Defaults to no grouping.           No
            Available values: max, hour, day, month, year
            "max" means group by the most granular
            datetime precision possible (5min)
users       Only fetch data for this set of users (comma separated)  No
limit       Number of desired items per page. Defaults to 500        No
after       Token for requesting next items on timeline              No
=========== ======================================================== ========

Examples
--------

Last 7 days traffic::

    $ curl -u APIKEY: 'https://crawlera-stats.scrapinghub.com/stats'
    {
        "limit":500,
        "after":””,
        "results": [
        {
            "time_gte":"2018-12-12T11:05:00+00:00",
            "failed":112275,
            "traffic":125085476006,
            "concurrency":2,
            "total_time":1930,
            "clean":3758963
        }]
    }

Last 7 days traffic max resolution::

    $ curl -u APIKEY: 'https://crawlera-stats.scrapinghub.com/stats?groupby=max'
    {
        "limit":500,
        "after":"MHgxLjcwNWYzMmMwMDAwMDBwKzMw",
        "results": [
        {
            "clean":175,
            "total_time":2032,
            "time_gte":"2018-12-17T15:30:00+00:00",
            "failed":16,
            "concurrency":2,
            "traffic":3554065
        }
        ....
        {
            "clean":166,
            "total_time":2036,
            "time_gte":"2018-12-17T16:15:00+00:00",
            "failed":4,
            "concurrency":1,
            "traffic":11257159
        }]
    }

Consume next page::

    $ curl -u APIKEY: 'https://crawlera-stats.scrapinghub.com/stats?groupby=max&after=MHgxLjcwNWYzMmMwMDAwMDBwKzMw'
    {
        "limit":500,
        "after":"MHgxLjcwNWYzNzcwMDAwMDBwKzMw",
        "results":[....]
    }

One day traffic per hour::

    $ curl -u APIKEY: 'https://crawlera-stats.scrapinghub.com/stats?start_date=2019-01-01T00%3A00&end_date=2019-01-01T23%3A59&groupby=hour'
    {
        “limit":500,
        “after”: “”,
        "results":[....]
    }
