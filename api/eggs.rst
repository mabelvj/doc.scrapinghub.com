.. _api-eggs:

========
Eggs API
========

You can use the eggs API to upload Python eggs to your project. This is typically used for managing external dependencies.

eggs/add.json
-------------

Adds a Python egg to a project.

========= ============ ========
Parameter Description  Required
========= ============ ========
project   Project ID.  Yes
name      Egg name.    Yes
version   Egg version. Yes
egg       Egg file.    Yes
========= ============ ========

====== ==================================== ===========================
Method Description                          Supported parameters
====== ==================================== ===========================
POST   Add Python egg to the given project. project, name, version, egg
====== ==================================== ===========================

Example::

    $ curl -u APIKEY: https://dash.scrapinghub.com/api/eggs/add.json -F project=123 -F name=somelib -F version=1.0 -F egg=@somelib-1.0.py2.6.egg

eggs/delete.json
----------------

Deletes a Python egg from a project.

========= =========== ========
Parameter Description Required
========= =========== ========
project   Project ID. Yes
name      Egg name.   Yes
========= =========== ========

====== ========================================= ====================
Method Description                               Supported parameters
====== ========================================= ====================
POST   Delete Python egg from the given project. project, name
====== ========================================= ====================

Example::

  $ curl -u APIKEY: https://dash.scrapinghub.com/api/eggs/delete.json -d project=123 -d name=somelib

eggs/list.json
--------------

Lists the eggs contained in a project.

========= =========== ========
Parameter Description Required
========= =========== ========
project   Project ID. Yes
========= =========== ========

====== =========================================== ====================
Method Description                                 Supported parameters
====== =========================================== ====================
GET    List Python eggs for the specified project. project
====== =========================================== ====================

Example::

  $ curl -u APIKEY: "https://dash.scrapinghub.com/api/eggs/list.json?project=123"
