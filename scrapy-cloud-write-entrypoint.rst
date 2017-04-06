.. _scrapy-cloud-write-entrypoint:

Scrapy Cloud Write Entrypoint
=============================

Scrapy Cloud Write Entrypoint is a write-only interface to a Scrapy Cloud storage. Its main purpose is to
make it easy to write crawlers and scripts compatible with Scrapy Cloud in different programming languages
using `custom Docker images`_.

Jobs in Scrapy Cloud run inside Docker containers. When a Job container is started, a `named pipe`_ is created
at the location stored in the ``SHUB_FIFO_PATH`` environment variable. The user program -- for example crawler
or script -- can open that named pipe and start writing data following a simple text protocol.

.. _custom Docker images: http://help.scrapinghub.com/scrapy-cloud/custom-docker-images-on-scrapy-cloud
.. _named pipe: http://man7.org/linux/man-pages/man7/fifo.7.html

Protocol
--------

Each message is a line of ASCII characters terminated by a newline character. Message consists of
the following parts:

- a 3-character command (one of "ITM", "LOG", "REQ", "STA", or "FIN"),
- followed by a space character,
- then followed by a payload as a `JSON`_ object,
- and a final newline character ``\n``.

This is how example log message will look like::

    LOG {"time": 1485269941065, "level": 20, "message": "Some log message"}\n

Newline characters are used as message separators. Please make sure that the serialized JSON object payload
doesn't contain newline characters between key/value pairs and that newline characters inside strings
(for both keys and values) are properly escaped::

    LOG {"time": 1485269941065, "level": 20, "message": "Line 1\\nLine 2"}\n

Unicode characters in JSON object MUST be escaped using standard JSON \u four-hex-digits syntax,
e.g. item ``{"ключ": "значение"}`` should look like this::

    ITM {"\\u043a\\u043b\\u044e\\u0447": "\\u0437\\u043d\\u0430\\u0447\\u0435\\u043d\\u0438\\u0435"}\n

The total size of the message MUST not exceed 1 MiB.

.. note::

    For simplicity all the following examples omit the trailing newline character.

ITM command
~~~~~~~~~~~

``ITM`` command stores a single :ref:`item <api-items>` in the Scrapy Cloud storage.
``ITM`` payload has not predefined schema.

Example::

    ITM {"key": "value"}

To support very simple scripts the Scrapy Cloud Write Entrypoint allows sending plain JSON objects as items,
so the following two lines are equivalent::

    ITM {"key": "value"}

::

    {"key": "value"}

Both lines are valid and will produce the item.

LOG command
~~~~~~~~~~~

``LOG`` command stores single :ref:`log <api-logs>` message in the Scrapy Cloud storage.
Fields for ``LOG`` payload are described in :ref:`log-object`.

Example::

    LOG {"level": 20, "message": "Some log message"}


REQ command
~~~~~~~~~~~

``REQ`` command stores single :ref:`request <api-requests>` in the Scrapy Cloud storage.
Fields for ``REQ`` payload are described in :ref:`request-object`.

Example::

    REQ {"url": "http://example.com", "method": "GET", "status": 200, "rs": 10, "duration": 20}

STA command
~~~~~~~~~~~

``STA`` stands for stats and is used to populate job stats page and create graphs on the job details page.

======= =================================================== ========
Field   Description                                         Required
======= =================================================== ========
time    UNIX timestamp of the message, in milliseconds.     No
stats   JSON object with arbitrary keys and values.         Yes
======= =================================================== ========

If following keys are present in the ``STA`` payload -- their values will be used to populate
Scheduled Requests graph on a job details page:

- ``scheduler/enqueued``
- ``scheduler/dequeued``

The keys names are picked for compatibility with `Scrapy stats`_.

.. _Scrapy stats: https://doc.scrapy.org/en/latest/topics/stats.html

Example::

    STA {"time": 1485269941065, "stats": {"key": 0, "key2": 20.5}}

FIN command
~~~~~~~~~~~

``FIN`` command is used to set outcome with when crawl is finished.

======= ======================================================== ========
Field   Description                                              Required
======= ======================================================== ========
outcome String with custom outcome message, limited to 255 chars Yes
======= ======================================================== ========

Example::

   FIN {"outcome": "finished"}

Support for stdout and stderr
-----------------------------

Job output in Scrapy Cloud is converted to log messages -- lines coming to stdout are converted to ``INFO``
level log messages and lines of stderr are converted to ``ERROR`` level log messages. For example,
if script prints ``Hello, world`` to stdout, the resulting `LOG command`_ will look like this::

    LOG {"time": 1485269941065, "level": 20, "message": "Hello, world"}

There's very basic support for multiline standard output -- if output consists of multiple lines where subsequent
lines start from a space character -- such output will be considered as a single log message. For example,
the following traceback in stderr::

    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    NameError: name 'e' is not defined

will produce the following log messages::

    LOG {"time": 1485269941065, "level": 40, "message": "Traceback (most recent call last):\\n  File \\"<stdin>\\", line 1, in <module>"}
    LOG {"time": 1485269941066, "level": 40, "message": "NameError: name 'e' is not defined"}

Resulting log messages are subject to 1 MiB limit -- this means that output longer than 1023 KiB
is likely to cause errors.

.. warning::

    It's recommended to use named pipe as the only way to produce log messages. Due to the way data
    is sent between processes it not possible to maintain order of messages coming from different sources
    (named pipe, stdout, stderr). For example consider 2 lines -- first line is sent to stdout, then shortly
    afterwards another line is sent to stderr. It's possible that on the receiving side line from stderr is received
    first and line for stdout is received afterwards. For high volumes of logs this can lead to confusing results,
    so it's highly recommended to use only named pipe -- this will both guarantee the best performance and guarantee
    that logs are received in exactly the same order they were sent.


How to build compatible scraper
-------------------------------

Scripts or non-Scrapy spiders have to be deployed as `custom Docker images`_.

.. _custom Docker images: https://shub.readthedocs.io/en/stable/deploy-custom-image.html


Each spider needs to follow the pattern:

#. Get path to a named pipe from ``SHUB_FIFO_PATH`` environment variable.
#. Open named pipe for writing. E.g. in Python you do it like this:

   .. code-block:: python

       import os

       path = os.environ['SHUB_FIFO_PATH']
       pipe = open(path, 'w')

#. Write `commands <Protocol>`_ to the pipe. If you want to send command instantly -- don't forget to flush,
   otherwise command may remain in the file buffer. However this is not always required as buffer will be flushed
   once enough data is written or when file object is closed (depends on the programming language you use):

   .. code-block:: python

       # write item
       pipe.write('ITM {"a": "b"}\n')
       pipe.flush()
       # ...
       # write request
       pipe.write('REQ {"time": 1484337369817, "url": "http://example.com", "method": "GET", "status": 200, "rs": 10, "duration": 20}\n')
       pipe.flush()
       # ...
       # write log entry
       pipe.write('LOG {"time": 1484337369817, "level": 20, "message": "Some log message"}\n')
       pipe.flush()
       # ...
       # write stats
       pipe.write('STA {"time": 1485269941065, "stats": {"key": 0, "key2": 20.5}}\n')
       pipe.flush()
       # ...
       # set outcome
       pipe.write('FIN {"outcome": "finished"}\n')
       pipe.flush()

#. Close the named pipe when the crawl is finished:

   .. code-block:: python

       pipe.close()

.. note::

    `scrapinghub-entrypoint-scrapy`__ uses Scrapy Cloud Write Entrypoint, check the code if you need an example.

__ https://github.com/scrapinghub/scrapinghub-entrypoint-scrapy/blob/master/sh_scrapy/writer.py
.. _JSON: http://json.org/
