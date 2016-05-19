.. _api-comments:

Comments API
============

The comments API lets you add comments directly to scraped data, which can later be viewed on the items page.

Comment object
--------------

======== ======================================
Field    Description
======== ======================================
id       Comment ID.
created  Created date.
archived Archived date.
author   Comment author.
avatar   User gravatar URL.
text     Comment text
editable If set to true, comment can be edited.
======== ======================================

comments/:comment_id
--------------------

Edits or archives a comment.

========== ============= ========
Parameter  Description   Required
========== ============= ========
comment_id Comment ID.   Yes
text       Comment text. PUT
========== ============= ========

====== ==================== ====================
Method Description          Supported Parameters
====== ==================== ====================
PUT    Update comment text. comment_id, text
DELETE Delete comment.      comment_id
====== ==================== ====================

PUT example::

  $ curl -X PUT -u APIKEY: --data 'text=my+new+text' "https://app.scrapinghub.com/api/comments/12"

DELETE example::

  $ curl -X DELETE -u APIKEY: "https://app.scrapinghub.com/api/comments/12"


comments/:project_id/:spider_id/:job_id
---------------------------------------

Retrieves all comments for a job indexed by item or item/field.

Example::

  $ curl -u APIKEY: "https://app.scrapinghub.com/api/comments/14/13/12"
  {
      "0": [comment, comment, ...],
      "0/title": [comment, comment, ...],
      "12/url": [comment, comment, ...],
  }

Where ``comment`` is a comment object as defined above.


comments/:project_id/stats
---------------------------

Retrieves the number of items with unarchived comments for each job of the project.

Example::

  $ curl -u APIKEY: "https://app.scrapinghub.com/api/comments/51/stats"
  {
      "51/422/2": 1,
      "51/414/2": 1,
      "51/421/2": 1,
      "51/423/2": 4,
      "51/413/3": 3,
      "51/418/2": 1
  }

comments/:project_id/:spider_id/:job_id/:item_no[/:field]
---------------------------------------------------------

Retrieves, updates or archives comments.

========== ============= ========
Parameter  Description   Required
========== ============= ========
text       Comment text. POST
========== ============= ========

======= ================================================== ====================
Method  Description                                        Supported parameters
======= ================================================== ====================
GET     Retrieve comments for an item or field.
POST    Update the specified comments with the given text. text
DELETE  Archive the specified comment.
======= ================================================== ====================

GET examples::

  $ curl -u APIKEY: "https://app.scrapinghub.com/api/comments/14/13/12/11"
  $ curl -u APIKEY: "https://app.scrapinghub.com/api/comments/14/13/12/11/logo"

POST examples::

  $ curl -X POST --data 'text=some+text' -u APIKEY: "https://app.scrapinghub.com/api/comments/14/13/12/11"
  $ curl -X POST --data 'text=some+text' -u APIKEY: "https://app.scrapinghub.com/api/comments/14/13/12/11/logo"

DELETE examples::

  $ curl -X DELETE -u APIKEY: "https://app.scrapinghub.com/api/comments/14/13/12/11"
  $ curl -X DELETE -u APIKEY: "https://app.scrapinghub.com/api/comments/14/13/12/11/logo"

