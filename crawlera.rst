.. _crawlera:

============
Crawlera API
============

.. note:: Check also the `Help Center`_ for general guides and articles.

Proxy API
=========

Crawlera works with a standard HTTP web proxy API, where you only need an API
key for authentication. This is the standard way to perform a request via
Crawlera::

    curl -vx proxy.crawlera.com:8010 -U <API key>: http://httpbin.org/ip

Errors
======

When an error occurs, Crawlera sends a response containing an :ref:`x-crawlera-error` header and an error message in the body.

.. note:: These errors are internal to Crawlera and are subject to change at any time, so should not be relied on and only used for debugging.

====================== =============  ======================
X-Crawlera-Error       Response Code  Error Message
====================== =============  ======================
bad_session_id         400            Incorrect session ID
user_session_limit     400            Session limit exceeded
bad_auth               407
too_many_conns         429            Too many connections*
header_auth            470            Unauthorized Crawlera header
\                      500            Unexpected error
nxdomain               502            Error looking up domain
econnrefused           502            Connection refused
econnreset             502            Connection reset
socket_closed_remotely 502            Server closed socket connection
send_failed            502            Send failed
noslaves               503            No available proxies
slavebanned            503            Website crawl ban
serverbusy             503            Server busy: too many outstanding requests
timeout                504            Timeout from upstream server
msgtimeout             504            Timeout processing HTTP stream
domain_forbidden       523            Domain forbidden. Please contact help@scrapinghub.com
bad_header             540            Bad header value for *<some_header>*
====================== =============  ======================

\* Crawlera limits the number of concurrent connections based on your Crawlera plan. See: `Crawlera pricing table <https://scrapinghub.com/pricing/#crawlera>`_ for more information on plans.

.. _sessions-request-limits:

Sessions and Request Limits
===========================

Sessions
--------

Sessions allow reusing the same slave for every request. Sessions expire 30 minutes after their last use and Crawlera limits the number of concurrent sessions to 100 for C10 plans, and 5000 for all other plans.

Sessions are managed using the :ref:`x-crawlera-session` header. To create a new session send::

    X-Crawlera-Session: create

Crawlera will respond with the session ID in the same header::

    X-Crawlera-Session: <session ID>

From then onward, subsequent requests can be made through the same slave by sending the session ID in the request header::

    X-Crawlera-Session: <session ID>

Another way to create sessions is using the `/sessions` endpoint::

    curl -u <API key>: proxy.crawlera.com:8010/sessions -X POST

This will also return a session ID which you can pass to future requests with the `X-Crawlera-Session` header like before. This is helpful when you can't get the next request using `X-Crawlera-Session`. 

If an incorrect session ID is sent, Crawlera responds with a ``bad_session_id`` error.


.. _/sessions:

List sessions
~~~~~~~~~~~~~

Issue the endpoint :ref:`/sessions` with the ``GET`` method to list your sessions. The endpoint returns a JSON document in which each key is a session ID and the associated value is a slave.

*Example*::

    curl -u <API key>: proxy.crawlera.com:8010/sessions
    {"1836172": "<SLAVE1>", "1691272": "<SLAVE2>"}

.. _/sessions/SESSION_ID:

Delete a session
~~~~~~~~~~~~~~~~

Issue the endpoint :ref:`/sessions/SESSION_ID` with the ``DELETE`` method in order to delete a session.

*Example*::

    curl -u <API key>: proxy.crawlera.com:8010/sessions/1836172 -X DELETE

Request Limits
--------------

Crawlera’s default request limit is 5 requests per second (rps) for each website. There is a default delay of 200ms between each request and a default delay of 1 second between requests through the same slave. These delays can differ for more popular domains. If the requests per second limit is exceeded, further requests will be delayed for up to 15 minutes. Each request made after exceeding the limit will increase the request delay. If the request delay reaches the soft limit (120 seconds), then each subsequent request will contain :ref:`x-crawlera-next-request-in` header with the calculated delay as the value.


Request Headers
===============

Crawlera supports multiple HTTP headers to control its behaviour.

Not all headers are available in every plan, here is a chart of the headers available in each plan (C10, C50, etc):

============================== === === ==== ==== ==========
Header                         C10 C50 C100 C200 Enterprise
============================== === === ==== ==== ==========
:ref:`x-crawlera-ua`               ✔   ✔    ✔    ✔
:ref:`x-crawlera-no-bancheck`      ✔   ✔    ✔    ✔
:ref:`x-crawlera-cookies`      ✔   ✔   ✔    ✔    ✔
:ref:`x-crawlera-timeout`      ✔   ✔   ✔    ✔    ✔
:ref:`x-crawlera-session`      ✔   ✔   ✔    ✔    ✔
:ref:`x-crawlera-jobid`        ✔   ✔   ✔    ✔    ✔
:ref:`x-crawlera-max-retries`  ✔   ✔   ✔    ✔    ✔
============================== === === ==== ==== ==========

.. _x-crawlera-ua:

X-Crawlera-UA
-------------
:sub:`Only available on C50, C100, C200 and Enterprise plans.`

This header controls Crawlera User-Agent behaviour. The supported values are:

* ``pass`` - pass the User-Agent as it comes on the client request
* ``desktop`` - use a random desktop browser User-Agent
* ``mobile`` - use a random mobile browser User-Agent

If ``X-Crawlera-UA`` isn’t specified, it will default to ``desktop``. If an unsupported value is passed in ``X-Crawlera-UA`` header, Crawlera replies with a ``540 Bad Header Value``.

More User-Agent types will be supported in the future (``chrome``, ``firefox``) and added to the list above.

.. _x-crawlera-no-bancheck:

X-Crawlera-No-Bancheck
----------------------
:sub:`Only available on C50, C100, C200 and Enterprise plans.`

This header instructs Crawlera not to check responses against its ban rules and pass any received response to the client. The presence of this header (with any value) is assumed to be a flag to disable ban checks.

*Example*::

    X-Crawlera-No-Bancheck: 1

.. _x-crawlera-cookies:

X-Crawlera-Cookies
------------------

This header allows to disable internal cookies tracking performed by Crawlera.

*Example*::

    X-Crawlera-Cookies: disable

.. _x-crawlera-session:

X-Crawlera-Session
------------------

This header instructs Crawlera to use sessions which will tie requests to a particular slave until it gets banned.

*Example*::

    X-Crawlera-Session: create

When ``create`` value is passed, Crawlera creates a new session an ID of which will be returned in the response header with the same name. All subsequent requests should use that returned session ID to prevent random slave switching between requests. Crawlera sessions currently have maximum lifetime of 30 minutes. See :ref:`sessions-request-limits` for information on the maximum number of sessions.

.. _x-crawlera-jobid:

X-Crawlera-JobId
----------------

This header sets the job ID for the request (useful for tracking requests in the Crawlera logs).

*Example*::

    X-Crawlera-JobId: 999

.. _x-crawlera-max-retries:

X-Crawlera-Max-Retries
----------------------

This header limits the number of retries performed by Crawlera.

*Example*::

    X-Crawlera-Max-Retries: 1

Passing ``1`` in the header instructs Crawlera to do up to 1 retry. Default number of retries is 5 (which is also the allowed maximum value, the minimum being 0).

.. _x-crawlera-timeout:

X-Crawlera-Timeout
------------------

This header sets Crawlera's timeout in milliseconds for receiving a response from the target website. The timeout must be specified in milliseconds and be between 30,000 and 180,000. It's not possible to set the timeout higher than 180,000 milliseconds or lower than 30,000 milliseconds, it will be rounded to its nearest maximum or minimum value.

*Example*::

    X-Crawlera-Timeout: 40000

The example above sets the response timeout to 40,000 milliseconds. In the case of a streaming response, each chunk has 40,000 milliseconds to be received. If no response is received after 40,000 milliseconds, a 504 response will be returned. If not specified, it will default to ``30000``.

[Deprecated] X-Crawlera-Use-Https
---------------------------------

Previously the way to perform https requests needed the http variant of the url plus the header `X-Crawlera-Use-Https` with value `1` like the following example:

::

    curl -x proxy.crawlera.com:8010 -U <API key>: http://twitter.com -H x-crawlera-use-https:1

Now you can directly use the https url and remove the `X-Crawlera-Use-Https` header, like this:

::

    curl -x proxy.crawlera.com:8010 -U <API key>: https://twitter.com

If you don't use curl for crawlera you can check the rest of the documentation
and update your scripts in order to continue using crawlera without issues.
Also some programming languages will ask for the Certificate
file :download:`crawlera-ca.crt`. You can install the certificate on your
system or set it explicitely on the script.

Response Headers
================

.. _x-crawlera-next-request-in:

X-Crawlera-Next-Request-In
--------------------------

This header is returned when response delay reaches the soft limit (120 seconds) and contains the calculated delay value. If the user ignores this header, the hard limit (1000 seconds) may be reached, after which Crawlera will return HTTP status code ``503`` with delay value in ``Retry-After`` header.

X-Crawlera-Debug
----------------

This header activates tracking of additional debug values which are returned in response headers. At the moment only ``request-time`` and ``ua`` values are supported, comma should be used as a separator. For example, to start tracking request time send::

    X-Crawlera-Debug: request-time

or, to track both request time and User-Agent send::

    X-Crawlera-Debug: request-time,ua

The ``request-time`` option forces Crawlera to output to the response header a request time (in seconds) of the last request retry (i.e. the time between Crawlera sending request to a slave and Crawlera receiving response headers from that slave)::

    X-Crawlera-Debug-Request-Time: 1.112218

The ``ua`` option allows to obtain information about the actual User-Agent which has been applied to the last request (useful for finding reasons behind redirects from a target website, for instance)::

    X-Crawlera-Debug-UA: Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/533+ (KHTML, like Gecko)

.. _x-crawlera-error:

X-Crawlera-Error
----------------

This header is returned when an error condition is met, stating a particular Crawlera error behind HTTP status codes (4xx or 5xx). The error message is sent in the response body.

*Example*::

    X-Crawlera-Error: user_session_limit

.. note:: Returned errors are internal to Crawlera and are subject to change at any time, so should not be relied on.

.. _crawlera-scrapy-cloud:

Using Crawlera with Scrapy Cloud
================================

To employ Crawlera in Scrapy Cloud projects the *Crawlera* addon is used. Go to **Settings > Addons > Crawlera** to activate.

Settings
--------

========================= ===================================================
CRAWLERA_URL              proxy URL (default: ``http://proxy.crawlera.com:8010``)
CRAWLERA_ENABLED          tick the checkbox to enable Crawlera
CRAWLERA_APIKEY           Crawlera API key
CRAWLERA_MAXBANS          number of bans to ignore before closing the spider (default: ``20``)
CRAWLERA_DOWNLOAD_TIMEOUT timeout for requests (default: ``190``)
========================= ===================================================


Using Crawlera with Selenium and Polipo
=======================================

Since it's not so trivial to set up proxy authentication in Selenium, a popular option is to employ `Polipo <http://www.pps.univ-paris-diderot.fr/~jch/software/polipo/>`_ as a proxy. Update Polipo configuration file ``/etc/polipo/config`` to include Crawlera credentials (if the file is not present, copy and rename ``config.sample`` found in Polipo source folder)::

    parentProxy = "proxy.crawlera.com:8010"
    parentAuthCredentials = "<API key>:"

For password safety reasons this content is displayed as ``(hidden)`` in the Polipo `web interface manager <http://www.pps.univ-paris-diderot.fr/~jch/software/polipo/polipo.html#Web-interface>`_. The next step is to specify Polipo proxy details in the Selenium automation script, e.g. for Python and Firefox:

.. literalinclude:: _static/crawlera-selenium.py
    :language: python

Using Crawlera with CasperJS, PhantomJS and SpookyJS
====================================================

To use session-wide Crawlera proxy with PhantomJs or CasperJS provide ``--proxy=proxy.crawlera.com:8010`` and ``--proxy-auth=<API key>:`` arguments to PhantomJS (CasperJS passes these arguments to PhantomJS).

*Example*::

    casperjs|phantomjs --proxy="proxy.crawlera.com:8010" --proxy-auth="<API KEY>:''" yourscript.js

When making HTTPS requests, you should provide path to :download:`crawlera-ca.crt`.

*Example*::

    phantomjs --ssl-protocol=any --proxy="proxy.crawlera.com:8010" --proxy-auth="<API KEY>:''" --ssl-client-certificate-file=/PATH/CRAWLERA_CA.crt phantomjs/examples/rasterize.js  https://twitter.com twitter.jpg

SpookyJS allows you to spawn multiple instances of CasperJS suites, so ``proxy`` and ``proxy-auth`` arguments should be provided when creating a Spooky object.

*Example*::

    var spooky = new Spooky({
        child: {
            proxy: 'proxy.crawlera.com:8010',
            proxy-auth: '<API key>:'
            /* ... */
        },
        /* ... */
    },

If it's preferred that Crawlera operated only on specific URLs, they should be wrapped according to :ref:`fetch-api`.

*Example in CasperJS*:

.. literalinclude:: _static/crawlera-casperjs.js
    :language: javascript


Using Crawlera with Splash
==========================

You can use `Splash <http://splash.readthedocs.org/en/stable/>`_ with Crawlera to render JavaScript and proxy all requests
issued from Splash. This can be necessary if your crawler makes heavy usage of Splash and target website throttles or blocks requests from Splash.

*How to do it?*

You need to send your requests to Splash. Splash must proxy its requests via Crawlera.

This is best achieved by using Splash ``/execute`` endpoint. You need to create Lua script that will tell Splash to use proxy for requests. Splash provides ``splash:on_request`` callback function that can be used for this purpose.

.. literalinclude:: _static/crawlera-splash.lua
    :language: lua

The previous example rendered a page as a PNG image and the binary content its returned in the HTTP request. The ``/execute`` endpoint reads the automation script in the ``lua_source`` parameter (which is a string containing the full script).

Example (using python requests library):

.. literalinclude:: _static/crawlera-splash.py
    :language: python

Note: in the previous python script Splash was running at address ``192.168.99.100`` default IP from docker container.


Using Crawlera from Different Languages
=======================================

.. warning::

    Some HTTP client libraries including Apache HttpComponents Client and .NET don't send authentication headers by default. This can result in doubled requests so pre-emptive authentication should be enabled where this is the case.

In the following examples we'll be making HTTPS requests to https://twitter.com
through Crawlera. It is assumed that Crawlera Certificate has been installed,
since `CONNECT method <http://doc.scrapinghub.com/crawlera.html#working-with-https>`_
will be employed.

Python
------

Making use of `Requests <http://docs.python-requests.org/en/latest/>`_ HTTP Proxy Authentication:

.. literalinclude:: _static/crawlera-python-requests-httpproxyauth.py
    :language: python

PHP
---

Making use of `PHP binding <http://curl.haxx.se/libcurl/php/examples>`_ for *libcurl* library:

.. literalinclude:: _static/crawlera-php-binding.php
    :language: php

Making use of `Guzzle <https://github.com/guzzle/guzzle>`_, a PHP HTTP client, in the context of `Symfony <https://symfony.com/>`_ framework:

.. literalinclude:: _static/crawlera-php-symfony.php
    :language: php

Ruby
----

Making use of `curb <https://github.com/taf2/curb>`_, a Ruby binding for *libcurl*:

.. literalinclude:: _static/crawlera-curb.rb
    :language: ruby

Making use of `typhoeus <https://github.com/typhoeus/typhoeus>`_, another Ruby binding for *libcurl*:

.. literalinclude:: _static/crawlera-typhoeus.rb
    :language: ruby

Making use of `mechanize <https://github.com/sparklemotion/mechanize>`_, a Ruby library for automated web interaction:
Don't forget to load the Certificate file :download:`crawlera-ca.crt` and set it
using the env variable `export SSL_CERT_FILE=/path/to/crawlera-ca.crt`

.. literalinclude:: _static/crawlera-mechanize.rb
    :language: ruby

Node.js
-------

Making use of `request <https://github.com/request/request>`_, an HTTP client:

.. literalinclude:: _static/crawlera-request.js
    :language: javascript

Java
----

.. note:: Because of `HTTPCLIENT-1649 <https://issues.apache.org/jira/browse/HTTPCLIENT-1649>`_ you should use version 4.5 of HttpComponents Client or later.

Extending an example published at `The Apache HttpComponents™ <http://hc.apache.org/httpcomponents-client-ga/examples.html>`_ project website and inserting Crawlera details:

.. literalinclude:: _static/crawlera-httpc.java
    :language: java

:download:`crawlera-ca.crt` should be added to keystore, for instance with *keytool*:

.. code-block:: text

    keytool -import -file /path/to/crawlera-ca.crt -storepass changeit -keystore $JAVA_HOME/jre/lib/security/cacerts -alias crawleracert

C#
--

.. literalinclude:: _static/crawlera-proxy.cs
    :language: csharp

.. _fetch-api:

Fetch API
=========

.. warning::

    The Fetch API is deprecated and will be removed soon. Use the standard proxy API instead.

Crawlera's fetch API let's you request URLs as an alternative to Crawlera's proxy interface.

Fields
------

.. note:: Field values should always be encoded.

=========== ======== ========================================= ===============================
Field       Required Description                               Example
=========== ======== ========================================= ===============================
url         yes      URL to fetch                              `http://www.food.com/`
headers     no       Headers to send in the outgoing request   `header1:value1;header2:value2`
=========== ======== ========================================= ===============================

Basic example::

    curl -u <API key>: http://proxy.crawlera.com:8010/fetch?url=https://twitter.com

Headers example::

    curl -u <API key>: 'http://proxy.crawlera.com:8010/fetch?url=http%3A//www.food.com&headers=Header1%3AVal1%3BHeader2%3AVal2'

.. _working-with-https:

Working with HTTPS
------------------

See `Crawlera with HTTPS <https://helpdesk.scrapinghub.com/support/solutions/articles/22000188407-crawlera-with-https>`_ in our Knowledge Base

.. _working-with-cookies:

Working with Cookies
--------------------

See `Crawlera and Cookies <https://helpdesk.scrapinghub.com/support/solutions/articles/22000188409-crawlera-and-cookies>`_in our Knowledge Base

.. _Help center: https://helpdesk.scrapinghub.com/support/home
