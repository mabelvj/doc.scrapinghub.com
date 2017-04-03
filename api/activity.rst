.. _api-activity:

============
Activity API
============

Scrapinghub keeps track of certain project events such as when spiders are run
or new spiders are deployed. This activity log can be accessed in the dashboard by
clicking on **Activity** in the left sidebar, or programmatically through the
API described below.

activity/:project_id
--------------------

Retrieve messages for a specified project. Results are returned in reverse order.

=========  ==================================== ========
Parameter  Description                          Required
=========  ==================================== ========
count      Maximum number of results to return. No
=========  ==================================== ========

====== =============================================== ====================
Method Description                                     Supported parameters
====== =============================================== ====================
GET    Returns the messages for the specified project. count
POST   Creates a message.
====== =============================================== ====================

GET example::

    $ curl -u APIKEY: https://storage.scrapinghub.com/activity/1111111/?count=2
    {"event":"job:completed","job":"1111111/3/4","user":"jobrunner"}
    {"event":"job:cancelled","job":"1111111/3/4","user":"example"}

POST example::

    $ curl -d '{"foo": 2}' https://storage.scrapinghub.com/activity/1111111/
    {"foo":4}
    {"foo":3}

activity/projects
-----------------

Retrieve messages for multiple projects.

Results are returned in reverse order.

========= ================================================================== ========
Parameter Description                                                        Required
========= ================================================================== ========
count     Maximum number of results to return.                               No
p         Project ID. Multiple values supported.                             No
pcount    Maximum number of results to return per project.                   No
meta      Meta parameter to add to results. See :ref:`api-overview-metapar`. No
========= ================================================================== ========

====== ================================================ ======================
Method Description                                      Supported parameters
====== ================================================ ======================
GET    Returns the messages for the specified projects. count, p, pcount, meta
====== ================================================ ======================

GET example::

    # Retrieve a single result for projects 1111111 and 2222222, using the ``meta`` parameter to include the project ID in the results.
    $ curl -u APIKEY: https://storage.scrapinghub.com/activity/projects/?pcount=1&meta=_project&p=1111111&p=2222222
    {"_project": 2222222, "bar": 1}
    {"_project": 1111111, "foo": 4}


