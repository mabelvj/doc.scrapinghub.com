.. _autoextract:

===============
AutoExtract API
===============

The AutoExtract API is a service for automatically extracting information
from web content.
You provide the URLs that you are interested in, and what type of content
you expect to find there (product or article).
The API will then fetch the content, and apply a number of techniques
behind the scenes to extract as much information as possible.
Finally, the downloaded content is returned to you,
along with the extracted information in structured form.

Before you Begin
================

You will need to obtain an API key before you can start using the AutoExtract
API. One should be emailed to you by our support team soon after you join
the AutoExtract API beta program.
If you haven't received one, you can contact the beta support team directly
at betatest@scrapinghub.com.

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
========

Requests are composed of a JSON array of queries.
Each query is a map containing the following fields:

============  ========  =======  ===========
Name          Required  Type     Description
============  ========  =======  ===========
``url``       Yes       String   URL of web page to extract from. Must be a valid ``http://`` or ``https://`` URL.
``pageType``  Yes       String   Type of extraction to perform. Must be ``article`` or ``product``.
``meta``      No        String   User UTF-8 string, which will be passed throughout the extraction pipeline and returned in the query result.
============  ========  =======  ===========

Responses
=========

API responses are wrapped in a JSON array
(this is to facilitate query batching; see below).
A query response for a single article extraction looks like this
(some internal fields omitted):

.. code-block:: json

    [
        {
            "article": {
                "articleBody": "Unbeknownst to many, there is a data revolution happening in finance.\n\nIn their never ending search for alpha hedge funds and investment banks are increasingly turning to new alternative sources of data to give them an informational edge over the market.\n\nOn the 31st May, Scrapinghub got ...",
                "articleBodyRaw": "<span id=\"hs_cos_wrapper_post_body\" class=\"hs_cos_wrapper hs_cos_wrapper_meta_field hs_cos_wrapper_type_rich_text\" data-hs-cos-general-type=\"meta_field\" data-hs-cos-type=\"rich_text\"><p><span>Unbeknownst to many, there is a data revolution ... ",
                "audioUrls": null,
                "author": "Ian Kerins",
                "authorsList": [
                    "Ian Kerins"
                ],
                "breadcrumbs": null,
                "datePublished": "2018-06-19T00:00:00",
                "datePublishedRaw": "June 19, 2018",
                "description": "A Sneak Peek Inside What Hedge Funds Think of Alternative Financial Data",
                "headline": "A Sneak Peek Inside What Hedge Funds Think of Alternative Financial Data",
                "images": [
                    "https://blog.scrapinghub.com/hubfs/conference-1038x576.jpg"
                ],
                "inLanguage": "en",
                "mainImage": "https://blog.scrapinghub.com/hubfs/conference-1038x576.jpg#keepProtocol",
                "probability": 0.8376080989837646,
                "url": "https://blog.scrapinghub.com/2018/06/19/a-sneak-peek-inside-what-hedge-funds-think-of-alternative-financial-data",
                "videoUrls": null
            },
            "error": null,
            "html": "<!DOCTYPE html><!-- start coded_template: id:5871566911 path:generated_layouts/5871566907.html --><!-...",
            "product": null,
            "query": {
                "userMeta": "Ku chatlanin!",
                "userQuery": {
                    "pageTypeHint": "article",
                    "url": "https://blog.scrapinghub.com/2018/06/19/a-sneak-peek-inside-what-hedge-funds-think-of-alternative-financial-data"
                }
            }
        }
    ]

Common Result Information
=========================

All API responses will include some basic information about the content
in the query:

.. code-block:: python

    # Enriched query
    print(response.json()[0]['query'])

    # HTML of content
    print(response.json()[0]['html'])

Product Extraction
==================

If you requested a product extraction, and the extraction succeeds,
then the product field will be available in the query result:

.. code-block:: python

    import requests

    response = requests.post(
        'https://autoextract.scrapinghub.com/v1/extract',
        auth=('[api key]', ''),
        json=[{'url': 'http://www.waterbedbargains.com/innomax-perfections-deep-fill-softside-waterbed/', 'pageType': 'product'}])
    print(response.json()[0]['product'])

The following fields will be available for the product:


======================   =======================================  ===========
Name                     Type                                     Description
======================   =======================================  ===========
``name``                 String                                   The name of the product.
``offers``               List of dictionaries with ``price``,     Offers of the product.
                         ``currency`` and ``availability``        All fields are optional but one of ``price`` or ``availability`` is present.
                         string fields                            ``price`` field is a valid number with a dot as a decimal separator.
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
``probability``          Float                                    Probability that this is a single product page.
``url``                  String                                   URL of page where this product was extracted.
======================   =======================================  ===========

All fields are optional, except for ``url`` and ``probability``.

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
              "link": "http://example"
            }
          ],
          "mainImage": "http://example/image.png",
          "images": [
            "http://example/image.png"
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
          "url": "https://example/product"
        },
        "error": null,
        "html": "<!DOCTYPE html><html ...",
        "article": null,
        "query": {
          "userQuery": {
            "pageTypeHint": "product",
            "url": "https://example/product"
          }
        }
      }
    ]

Article Extraction
==================
