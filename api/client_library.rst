**Client Library**

Most of the features provided by the API are also available through the :ref:`python-hubstorage<api-overview-ep-storage>` client library, as you can see below in :ref:`items-examples`. You have to authenticate yourself to create a ``HubstorageClient`` object to interact with hubstorage::

    >>> from hubstorage import HubstorageClient
    >>> hc = HubstorageClient(auth=APIKEY)
