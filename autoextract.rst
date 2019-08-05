.. _autoextract:

===============
AutoExtract API
===============

The AutoExtract API is a service for automatically extracting information
from web content.
You provide the URLs that you are interested in, and what type of content
you expect to find there (product or article).
The service will then fetch the content, and apply a number of techniques
behind the scenes to extract as much information as possible.
Finally, the extracted information is returned to you in structured form.

Before you Begin
================

You will need to obtain an API key before you can start using the AutoExtract
API. You should receive one when you complete the signup process.
If you haven't received one, you can contact the AutoExtract support team directly
at autoextract-support@scrapinghub.com.

.. note:: In all of the examples below, you will need to replace the string
          '[api key]' with your unique key.

Basic Usage
===========

Currently, the API has a single endpoint:
https://autoextract.scrapinghub.com/v1/extract.
A request is composed of one or more queries.
Each query contains a URL to extract from, and a page type
that indicates what the extraction result should be (product or article).
Requests and responses are transmitted in JSON format over HTTPS.
Authentication performed using HTTP Basic Authentication
where your API key is the username and the password is empty.

::

    curl --verbose \
        --user '[api key]':'' \
        --header 'Content-Type: application/json' \
        --data '[{"url": "https://blog.scrapinghub.com/gopro-study", "pageType": "article"}]' \
        https://autoextract.scrapinghub.com/v1/extract

Or, in Python

.. code-block:: python

    import requests
    response = requests.post(
        'https://autoextract.scrapinghub.com/v1/extract',
         auth=('[api key]', ''),
         json=[{'url': 'https://blog.scrapinghub.com/gopro-study', 'pageType': 'article'}])
    print(response.json())


Requests
--------

Requests are comprised of a JSON array of queries.
Each query is a map containing the following fields:

==================  ========  =======  ===========
Name                Required  Type     Description
==================  ========  =======  ===========
``url``             Yes       String   URL of web page to extract from. Must be a valid ``http://`` or ``https://`` URL.
``pageType``        Yes       String   Type of extraction to perform. Must be ``article`` or ``product``.
``meta``            No        String   User UTF-8 string, which will be passed through the extraction pipeline and returned in the query result. Max size 4 Kb.
``articleBodyRaw``  No        boolean  Whether or not to include article HTML in article extractions. True by default. Setting this to false can reduce response significantly if HTML is not required.
==================  ========  =======  ===========

Responses
---------

API responses are wrapped in a JSON array
(this is to facilitate query batching; see below).
A query response for a single article extraction looks like this
(some large fields are truncated):

.. code-block:: json

	[
	  {
	    "query": {
	      "id": "1564747029122-9e02a1868d70b7a1",
	      "domain": "scrapinghub.com",
	      "userQuery": {
		"url": "https://blog.scrapinghub.com/2018/06/19/a-sneak-peek-inside-what-hedge-funds-think-of-alternative-financial-data",
		"pageType": "article"
	      }
	    },
	    "article": {
	      "articleBody": "Unbeknownst to many..",
	      "articleBodyRaw": "<span id=...",
	      "headline": "A Sneak Peek Inside What Hedge Funds Think of Alternative Financial Data",
	      "inLanguage": "en",
	      "datePublished": "2018-06-19T00:00:00",
	      "datePublishedRaw": "June 19, 2018",
	      "author": "Ian Kerins",
	      "authorsList": [
		"Ian Kerins"
	      ],
	      "mainImage": "https://blog.scrapinghub.com/hubfs/conference-1038x576.jpg#keepProtocol",
	      "images": [
		"https://blog.scrapinghub.com/hubfs/conference-1038x576.jpg"
	      ],
	      "description": "A Sneak Peek Inside What Hedge Funds Think of Alternative Financial Data",
	      "url": "https://blog.scrapinghub.com/2018/06/19/a-sneak-peek-inside-what-hedge-funds-think-of-alternative-financial-data",
	      "probability": 0.7369686365127563
	    }
	  }
	]


Output fields
=============

Query
-----
All API responses include the original query along with some additional information such as the query ID:

.. code-block:: python

    # Enriched query
    print(response.json()[0]['query'])

 

Product Extraction
------------------

If you requested a product extraction, and the extraction succeeds,
then the ``product`` field will be available in the query result:

.. code-block:: python

    import requests

    response = requests.post(
        'https://autoextract.scrapinghub.com/v1/extract',
        auth=('[api key]', ''),
        json=[{'url': 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html', 'pageType': 'product'}])
    print(response.json()[0]['product'])

The following fields are available for products:


======================   =======================================  ===========
Name                     Type                                     Description
======================   =======================================  ===========
``name``                 String                                   The name of the product.
``offers``               List of dictionaries with ``price``,     Offers of the product.
                         ``currency`` and ``availability``        All fields are optional but one of ``price`` or ``availability`` is present.
                         string fields                            ``price`` field is a string with a valid number (dot is a decimal separator).
                                                                  ``currency`` is currency as given on the web site, without extra normalization
                                                                  (for example both "$" and "USD" are possible currencies).
                                                                  It is present only if price is also present.
                                                                  ``availability`` is product availability, currently it can either be
                                                                  ``"InStock"`` or ``"OutOfStock"``. ``"InStock"`` includes the following cases:
                                                                  in-stock, limited availability, pre-sale (indicates that the item is available
                                                                  for ordering and delivery before general availability), pre-order (indicates that
                                                                  the item is available for pre-order, but will be delivered when generally
                                                                  available), in-store-only (indicates that the item is available only at
                                                                  physical locations). ``"OutOfStock"`` includes following cases: out-of-stock, dis-continued
                                                                  and sold-out.
``sku``                  String                                   Stock Keeping Unit identifier for the product assigned by the seller.
``mpn``                  String                                   Manufacturer part number identifier for product.
                                                                  It is issued by the manufacturer and is same across different websites for a product.
``gtin``                 List of dict with ``type`` and           Standardized GTIN product identifier which is unique
                         ``value`` string fields                  for a product across different sellers. It includes the following
                                                                  ``type``: isbn10, isbn13, issn, ean13, upc, ismn, gtin8, gtin14.
                                                                  gtin14 corresponds to former names EAN/UCC-14, SCC-14, DUN-14, UPC Case Code,
                                                                  UPC Shipping Container Code. ean13 also includes the jan (japnese article
                                                                  number). E.g. ``[{'type': 'isbn13', 'value': '9781933624341'}]``
``brand``                String                                   Brand or manufacturer of the product.
``breadcrumbs``          List of dictionaries with ``name``       A list of breadcrumbs (a specific navigation element) with optional name and URL.
                         and ``link`` optional string fields

``mainImage``            String                                   A URL or data URL value of the main image of the product.
``images``               List of strings                          A list of URL or data URL values of all images of the product (may include the main image).
``description``          String                                   Description of the product.
``aggregateRating``      Dictionary with ``ratingValue``,         ``ratingValue`` is the average rating value.
                         ``bestRating`` float fields and          ``bestRating`` is the best possible rating value.
                         ``reviewCount`` int field                ``reviewCount`` is the number of reviews or ratings for the product.
                                                                  All fields are optional but one of ``reviewCount`` or ``ratingValue`` is present.
``additionalProperty``   List of dictionaries with ``name``       A list of product properties or characteristics, ``name`` field contains the property name,
                         and ``value`` fields                     and ``value`` field contains the property value.
``probability``          Float                                    Probability that the requested page is a single product page.
``url``                  String                                   URL of page where this product was extracted.
======================   =======================================  ===========

All fields are optional, except for ``url`` and ``probability``. Fields without a valid value (null or empty array) are excluded from extraction results.

Below is an example response with all product fields present:

.. code-block:: json

    [
      {
        "product": {
          "name": "Product name",
          "offers": [
            {
              "price": "42",
              "currency": "USD",
              "availability": "InStock"
            }
          ],
          "sku": "product sku",
          "mpn": "product mpn",
          "gtin": [
            {
              "type": "ean13",
              "value": "978-3-16-148410-0"
            }
          ],
          "brand": "product brand",
          "breadcrumbs": [
            {
              "name": "Level 1",
              "link": "http://example.com"
            }
          ],
          "mainImage": "http://example.com/image.png",
          "images": [
            "http://example.com/image.png"
          ],
          "description": "product description",
          "aggregateRating": {
            "ratingValue": 4.5,
            "bestRating": 5.0,
            "reviewCount": 31
          },
          "additionalProperty": [
            {
              "name": "property 1",
              "value": "value of property 1"
            }
          ],
          "probability": 0.95,
          "url": "https://example.com/product"
        },
        "query": {
          "id": "1564747029122-9e02a1868d70b7a2",
          "domain": "example.com",
          "userQuery": {
            "pageTypeHint": "product",
            "url": "https://example.com/product"
          }
        }
      }
    ]

Article Extraction
------------------

If you requested an article extraction, and the extraction succeeds,
then the ``article`` field will be available in the query result:

.. code-block:: python

    import requests

    response = requests.post(
        'https://autoextract.scrapinghub.com/v1/extract',
        auth=('[api key]', ''),
        json=[{'url': 'https://blog.scrapinghub.com/2016/08/17/introducing-scrapy-cloud-with-python-3-support',
               'pageType': 'article'}])
    print(response.json()[0]['article'])


The following fields are avaialable for articles:

======================   =======================================  ===========
Name                     Type                                     Description
======================   =======================================  ===========
``headline``             String                                   Article headline or title.
``datePublished``        String                                   Date, ISO-formatted with 'T' separator, may contain a timezone.
``datePublishedRaw``     String                                   Same date but before parsing, as it appeared on the site.
``author``               String                                   Author (or authors) of the article.
``authorsList``          List of strings                          All authors of the article split into separate strings, for example the
                                                                  ``author`` value might be ``"Alice and Bob"`` and ``authorList`` value
                                                                  ``["Alice", "Bob"]``, while for a single author
                                                                  ``author`` value might be ``"Alice Johnes"`` and ``authorList`` value
                                                                  ``["Alice Johnes"]``.
``inLanguage``           String                                   Language of the article, as an ISO 639-1 language code.
``breadcrumbs``          List of dictionaries with                A list of breadcrumbs (a specific navigation element) with optional name and URL.
                         ``name`` and ``link`` optional
                         string fields
``mainImage``            String                                   A URL or data URL value of the main image of the article.
``images``               List of strings                          A list of URL or data URL values of all images of the article (may include the main image).
``description``          String                                   A short summary of the article, human-provided if available, or auto-generated.
``articleBody``          String                                   Text of the article, including sub-headings and image captions, with newline separators.
``articleBodyRaw``       String                                   html of the article body.
``videoUrls``            List of strings                          A list of URLs of all videos inside the article body.
``audioUrls``            List of strings                          A list of URLs of all audios inside the article body.
``probability``          Float                                    Probability that this is a single article page.
``url``                  String                                   URL of page where this article was extracted.
======================   =======================================  ===========

All fields are optional, except for ``url`` and ``probability``. The ``articleBodyRaw`` field will only be returned if you pass ``"articleBodyRaw": true`` as
as query parameter. Fields without a valid value (null or empty array) are excluded from extraction results.

Below is an example response with all article fields present:

.. code-block:: json


    [
      {
        "article": {
          "headline": "Article headline",
          "datePublished": "2019-06-19T00:00:00",
          "datePublishedRaw": "June 19, 2018",
          "author": "Article author",
          "authorsList": [
            "Article author"
          ],
          "inLanguage": "en",
          "breadcrumbs": [
            {
              "name": "Level 1",
              "link": "http://example.com"
            }
          ],
          "mainImage": "http://example.com/image.png",
          "images": [
            "http://example.com/image.png"
          ],
          "description": "Article summary",
          "articleBody": "Article body ...",
          "articleBodyRaw": "<div>html of article body ...",
          "videoUrls": [
            "https://example.com/video"
          ],
          "audioUrls": [
            "https://example.com/audio"
          ],
          "probability": 0.95,
          "url": "https://example.com/article"
        },
        "query": {
          "id": "1564747029122-9e02a1868d70b7a3",
          "domain": "example.com",
          "userQuery": {
            "pageTypeHint": "article",
            "url": "https://example/article"
          }
        }
      }
    ]

Errors
======

Errors fall into two broad categories: request-level and query-level.
Request-level errors occur when the HTTP API server can't process
the input that it receives. Query-level errors occur when specific query
cannot be processed. You can detect these by checking the ``error``
field in query results.

Request-level
-------------

Examples include:

- Authentication failure
- Malformed request JSON
- Too many queries in request
- Request payload size too large

If a request-level error occurs,
the API server will return a 4xx or 5xx response code.
If possible, a JSON response body with content type
``application/problem+json`` will be returned that describes the error
in accordance with
`RFC-7807 - Problem Details for HTTP APIs <https://tools.ietf.org/html/rfc7807>`_

.. code-block:: python

    import requests

    # Send a request with 101 queries
    response = requests.post(
        'https://autoextract.scrapinghub.com/v1/extract',
         auth=('[api key]', ''),
         json=[{'url': 'http://www.example.com', 'pageType': 'product'}] * 101)

    print(response.status_code == requests.codes.ok)  # False
    print(response.status_code)                       # 413
    print(response.headers['content-type']            # application/problem+json
    print(response.json()['title'])                   # Limit of 100 queries per request exceeded
    print(response.json()['type'])                    # http://errors.xod.scrapinghub.com/queries-limit-reached


In the above example of the queries-limit problem (identified by the URI type) the reason for 413 is indicated
in the ``title``. The ``type`` field should be used to check the error type as this will not change in
subsequent versions. There could be more specific fields depending on the error providing additional details, e.g.
delay before retrying next time. Such responses can be easily parsed and used for programmatic error handling.

If it is not possible to return a JSON description of the error, then no content type header will be set for the
response and the response body will be empty.

Query-level
-----------

If the ``error`` field is present in an extraction result, then an error has occurred and the extraction result will not be available.

.. code-block:: python

    import requests

    response = requests.post(
        'https://autoextract.scrapinghub.com/v1/extract',
        auth=('[api key]', ''),
        json=[{'url': 'http://www.example.com/this-page-does-not-exist', 'pageType': 'article'}])

    print('error' in response.json()[0])        # True
    print(response.json()[0]['error'])          # Downloader error: http404


Reference
---------

Request-level
^^^^^^^^^^^^^
=======================================================================  ============================================================
Type                                                                     Short description
=======================================================================  ============================================================
http://errors.xod.scrapinghub.com/queries-limit-reached.html             Limit of 100 queries per request exceeded
http://errors.xod.scrapinghub.com/malformed-json.html                    Could not parse request JSON
http://errors.xod.scrapinghub.com/rate-limit-exceeded.html               System-wide rate limit exceeded
http://errors.xod.scrapinghub.com/user-rate-limit-exceeded.html          User rate limit exceeded
http://errors.xod.scrapinghub.com/account-disabled.html                  Account has been disabled - contact support
http://errors.xod.scrapinghub.com/unrecognized-content-type.html         Unsupported request content type: should be application/json
http://errors.xod.scrapinghub.com/empty-request.html                     Empty request body - should be JSON document
http://errors.xod.scrapinghub.com/malformed-request.html                 Unparseable request
http://errors.xod.scrapinghub.com/http-pipelining-not-supported.html     Attempt to second HTTP request over TCP connection
http://errors.xod.scrapinghub.com/unknown-uri.html                       Invalid API endpoint
http://errors.xod.scrapinghub.com/method-not-allowed.html                Invalid HTTP method (only POST is supported)
=======================================================================  ============================================================

Query-level
^^^^^^^^^^^
===============================================================  =======================================================
error contains                                                   Description
===============================================================  =======================================================
query timed out                                                  10 minute time out for query reached
malformed url                                                    Requested URL cannot be parsed
non-HTTP schemas are not allowed                                 Only http and https schemas are allowed
Domain ... is occupied, please retry in ... seconds              Per-domain rate limiting was applied. It is recommended to retry after the specified interval.
Downloader error: No response (network301)                       Redirects are not supported
Downloader error: No visible elements                            There are no visible elements in downloaded content
Downloader error: http304                                        Remote server returned HTTP status code 304 (not modified)
Downloader error: http404                                        Remote server returned HTTP status code 404 (not found)
Downloader error: http500                                        Remote server returned HTTP status code 404 (internal server error)
Downloader error: No response (network5)                         Remote server closed connection before transfer was finished
Proxy error: ssl_tunnel_error                                    SSL proxy tunneling error
Proxy error: banned                                              Crawlera made several retries, but was unable to avoid banning. This flags antiban measures in actions, but doesn't mean the proxy pool is exhausted. Retry is recommended.
Proxy error: domain_forbidden                                    Domain is forbidden on Crawlera side
Proxy error: internal_error                                      Internal proxy error
Proxy error: nxdomain                                            Crawlera wasn't able to resolve domain through DNS
===============================================================  =======================================================

There could be also other, more rare errors.


Restrictions and Failure Modes
==============================

- A maximum of 100 queries may be submitted in a single request.
  The total size of the request body cannot exceed 128KB.
- There is a global timeout of 10 minutes for queries.
  Queries can time out for a number of reasons,
  such as difficulties during content download.
  If a query in a batched request times out,
  the API will return the results of the extractions
  that did succeed along with errors for those that timed out.
  We therefore recommend that you set the HTTP timeout for API requests
  to over 10 minutes.



Batching Queries
================

Multiple queries can be submitted in a single API request,
resulting in an equivalent number of query results.

.. note::
    When using batch requests, each query is accounted towards usage limits
    separately. For example, sending a batch request with 10 queries incur
    the same cost as sending 10 requests with 1 query each.

.. code-block:: python

    import requests

    response = requests.post(
        'https://autoextract.scrapinghub.com/v1/extract',
        auth=('[api key]', ''),
        json=[{'url': 'https://blog.scrapinghub.com/2016/08/17/introducing-scrapy-cloud-with-python-3-support', 'pageType': 'article'},
              {'url': 'https://blog.scrapinghub.com/spidermon-scrapy-spider-monitoring', 'pageType': 'article'},
              {'url': 'https://blog.scrapinghub.com/gopro-study', 'pageType': 'article'}])

    for query_result in response.json():
        print(query_result['article']['headline'])

Note that query results are not necessarily returned
in the same order as the original queries.
If you need an easy way to associate the results with the queries
that generated them, you can pass an additional ``meta`` field in the query.
The value that you pass will appear as the ``query/userQuery/meta`` field
in the corresponding query result.
For example, you can create a dictionary keyed on the ``meta`` field
to match queries with their corresponding results:

.. code-block:: python

    import requests

    queries = [
        {'meta': 'query1', 'url': 'https://blog.scrapinghub.com/2016/08/17/introducing-scrapy-cloud-with-python-3-support', 'pageType': 'article'},
        {'meta': 'query2', 'url': 'https://blog.scrapinghub.com/spidermon-scrapy-spider-monitoring', 'pageType': 'article'},
        {'meta': 'query3', 'url': 'https://blog.scrapinghub.com/gopro-study', 'pageType': 'article'}]

    response = requests.post(
        'https://autoextract.scrapinghub.com/v1/extract',
        auth=('[api key]', ''),
        json=queries)

    query_results = {result['query']['userQuery']['meta']: result for result in response.json()}

    for query in queries:
        query_result = query_results[query['meta']]
        print(query_result['article']['headline'])



