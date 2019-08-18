.. _unified_schema:

============================
Unified Schema
============================


The Unified Schema project aims to provide a standard definition for the different types of data such as products,
articles, reviews, jobs etc. extracted across websites.

.. note::

    All fields in the AutoExtract have the exact same definition in the Unified Schema. We also aim to maintain
    backward compatibility while adding new fields. We also try our best to adhere to schema.org, only diverging when
    there is a reasonable benefit in doing so.

New schema definitions can be proposed in our github_ repository.


Product Schema
============================

The following fields are available for products:

======================= ================================ ===============================================================
  Field                 Format                           Description
======================= ================================ ===============================================================
  aggregateRating       - Type: ``Dictionary``           The overall rating, based on a collection of reviews or ratings
                        - Fields:
                                                         |rating|

                          1. ratingValue ``Number``      .. code-block:: javascript
                          2. bestRating ``Number``
                          3. reviewCount ``Number``        {
                                                            'ratingValue': 4.0,
                                                            'bestRating': 5.0,
                                                            'reviewCount': 23
                                                           }

  additionalProperty    - Type: ``List``                 This name-value pair field holds information pertaining to
                        - Items: ``Dictionary``          product specific features that have no matching property in the
                        - Fields:                        Product schema.
                           1. name ``String``
                           2. value ``String``
                              ``Float`` ``List``         |product_info|
                              ``Dictionary``
                                                         .. code-block:: javascript

                                                          [{"name": "batteries",
                                                            "value": "1 Lithium ion batteries required. (included)"},
                                                           {"name": "Item model number",
                                                            "value": "SM-A105G/DS"}]

  brand                 - Type: ``String``               The brand associated with the product

                                                         |brand|

                                                         .. code-block:: javascript

                                                            {"brand": "Samsung"}

                                                         |brand_not|

                                                         **No brand is returned**

  breadCrumbs           - Type: ``List``                 A list of breadcrumbs with optional name and URL.
                        - Fields:
                           1. name ``String``            .. code-block:: javascript
                           2. link ``String``
                                                          [{"name": ""Cell Phones & Accessories"",
                                                            "link": "https://amz.com/cell-phones-accessories"}...]

  description           - Type: ``String``               A description of the product

  gtin                  - Type: ``List``
                        - Items: ``Dictionary``          Standardized GTIN product identifier which is unique for a
                        - Fields:                        product across different sellers. It includes the following
                           1. type ``String``            type: isbn10, isbn13, issn, ean13, upc, ismn, gtin8, gtin14.
                           2. value ``String``           gtin14 corresponds to former names EAN/UCC-14, SCC-14, DUN-14,
                                                         UPC Case Code, UPC Shipping Container Code.ean13 also includes
                                                         the jan (japnese article number)

                                                         .. code-block:: javascript

                                                           [{'type': 'isbn13', 'value': '9781933624341'}]

  images                - Type: ``List``                 A list of URL or data URL values of all images of the product
                        - Items: ``String``              (may include the main image).

  mainImage             - Type: ``String``               A URL or data URL value of the main image of the product.


  mpn                   - Type: ``String``               The Manufacturer Part Number (MPN) of the product. The product
                                                         would have the same MPN across different e-commerce websites.

  name                  - Type: ``String``               The name of the product

  offers_               - Type: ``List``                 This field contains rich information pertaining to all the
                        - Items: ``Dictionary``          buying options offered on a product. Detailed information
                        - Fields:                        regarding all the properties returned in this field is
                           1. availability ``String``    available in the offers_ section. |offers2|
                           2. currency ``String``
                           3. listPrice ``String``       .. code-block:: javascript
                           4. price ``String``
                           5. eligibleQuantity_             [{
                           6. seller_                           "availability":"InStock",
                           7. shippingInfo_                     "price":"129.99",
                           8. availableAtOrFrom_                "currency":"$"
                           9. areaServed_                       "itemCondition":{
                           10. itemCondition_                   "type":"used",
                                                             "description":"Used - Very Good"
                                                             },
                                                             "seller":{
                                                             "name":"Java Junkie",
                                                             "url":"https://amz.com/gp/aag/main/seller=A8K32FFKI51FKN",
                                                             "identifier":"A8K32FFKI51FKN",
                                                             "aggregateRating":{
                                                             "reviewCount":479,
                                                             "bestRating":5
                                                             },
                                                             "shippingInfo":{
                                                             "minDays":"15",
                                                             "maxDays":"30",
                                                             "description":"Arrives between September 3-18."
                                                             }
                                                             }
                                                             }]


  ratingHistogram       - Type: ``List``                 This fields provides the detailed distribution of ratings
                        - Items: ``Dictionary``          across the entire rating scale
                        - Fields:
                           1. ratingValue ``String``     |histogram|
                           2. ratingCount ``Number``
                           3. ratingPercentage           .. code-block:: javascript
                              ``Number``
                                                           [{"ratingValue": "5", "ratingPercentage": 61},
                                                            {"ratingValue": "4", "ratingPercentage": 12}
                                                            {"ratingValue": "3", "ratingPercentage": 6},
                                                            {"ratingValue": "2", "ratingPercentage": 5}
                                                            {"ratingValue": "1", "ratingPercentage": 16}]

  releaseDate                                            Date on which the product was released or listed on the website
                                                         in ISO 8601 date format

                                                         .. code-block:: javascript

                                                           {"releaseDate": "2016-12-18"}

  relatedProducts       - Type: ``List``                 This field captures all products that are recommended by the
                        - Items: ``Dictionary``          website while browsing the product of interest.
                        - Fields:                        Related products can thus be used to gauge customer buying
                           1. relationshipName           behaviour, sponsored products as well best sellers in the
                              ``String``                 same category.
                           2. products ``List``          The ``relationshipName`` field describes the relationship while
                                                         the ``products`` field contains a list of items have the same
                                                         ``product`` schema, thus extracting all available fields as
                                                         defined in this table

                                                         |related_products|

  variants              - Type: ``List``                 This field returns a list of variants of the product.
                        - Items: ``Product``             Each variant has the same schema as the Product schema defined
                                                         in this table.

  sku                   - Type: ``String``               The Stock Keeping Unit (SKU) i.e. a merchant-specific
                                                         identifier for the product

                                                         |sku|

                                                         .. code-block:: javascript

                                                           {"sku": "B07QHQ2JJC"}

  width                 - Type: ``String``               The width of the product

  height                - Type: ``String``               The height of the product

  depth                 - Type: ``String``               The depth of the product

  weight                - Type: ``String``               The weight of the product

  volume                - Type: ``String``               The volume of the product

  url                   - ``Required``                     The URL of the product
                        - Type: ``String``
======================= ================================ ===============================================================



.. _offers:

offers
_______

The offers field contains several fields as explained below that can be leveraged to get deep insights into the
various product offerings, associated seller information as well as inventory.


.. _eligibleQuantity:

**eligibleQuantity**

This field gives details about bulk purchase offers available for the product.

======================= ================================ ===============================================================
  Field                 Format                           Description
======================= ================================ ===============================================================
 maxValue               ``Number``                        Maximum value allowed.
 minValue               ``Number``                        Minimum value required
 value                  ``Number``                        Exact value required
 unitText               ``String``                        Unit of measurement
 description            ``String``                        Free text from where this range was extracted
======================= ================================ ===============================================================

Let's take the following example to examine the aforementioned fields

|bulk_offer|

.. code-block:: javascript

    {'offers': [
       {'price': '11,98', 'currency': '$'},
       {'price': '10,78', 'currency': '$', 'eligibleQuantity': {'min_value': '48', 'description': 'Buy 44 or more $9.33'}}
      ]
    }

.. _availableAtOrFrom:

**availableAtOrFrom**

The place(s) from which the offer can be obtained (e.g. store locations). It could contain a string, i.e.: online_only

.. _postalAddress:

======================= ================================ ===============================================================
  Field                 Format                           Description
======================= ================================ ===============================================================
 postalCode              ``String``                       Postal code of the address
 streetAddress           ``String``                       The street address. For example, 1600 Amphitheatre Pkwy.
 addressCountry          ``String``                       The country. For example, USA. You can also provide the
                                                          two-letter ISO 3166-1 alpha-2 country code.
                                                          https://en.wikipedia.org/wiki/ISO_3166-1
 addressLocality        ``String``                        The locality in which the street address is, and which is in
                                                          the region. For example, Mountain View.
 addressRegion          ``String``                        The region in which the locality is, and which is in the
                                                          country. For example, California.
======================= ================================ ===============================================================

.. _areaServed:

**areaServed**

The geographic area where a service or offered item is provided. The fields and the definition is the same as
availableAtOrFrom_.

.. _shippingInfo:

**shippingInfo**


======================= ================================ ===============================================================
  Field                 Format                           Description
======================= ================================ ===============================================================
currency                ``String``                       Currency associated to the price
price                   ``String``                       Cost of shipping
minDays                 ``Number``                       Minimum number of days estimated for the delivery
maxDays                 ``Number``                       Maximum number of days estimated for the delivery
averageDays             ``Number``                       Average days for a delivery
description             ``String``                       Any associated text describing the shipping info
originAddress           ``String``  or postalAddress_    Location of the warehouse where the item is shipped from
======================= ================================ ===============================================================

.. _seller:

**seller**

This field provides the seller details including rating.

======================= ================================ ===============================================================
  Field                 Format                           Description
======================= ================================ ===============================================================
name                    ``String``                       Name of the seller
url                     ``String``                       URL for the seller's page
identifier              ``String``                       Unique identifier assigned to the seller on the website
aggregateRating         ``Dictionary``                   The sellers rating. Same as aggregateRating in the product
                                                         schema.
======================= ================================ ===============================================================


.. _itemCondition:

**itemCondition**

A predefined value and a textual description of the condition of the product included

======================= ================================ ===============================================================
  Field                 Format                           Description
======================= ================================ ===============================================================
type                    ``String``                       A predefined value of the condition of the product included
                                                         in the offer.
                                                         Takes on one of the following enumerated values
                                                         ``['NewCondition', 'DamagedCondition', 'RefurbishedCondition',
                                                         'UsedCondition']``
description             ``String``                       A textual description of the condition of the product included
                                                         in the offer
======================= ================================ ===============================================================

Article Schema
============================

The following fields are available for articles:

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


.. |histogram| image:: https://dl.dropboxusercontent.com/s/tqgvuujk362ztse/histogram.png
.. |related_products| image:: https://dl.dropboxusercontent.com/s/phzqh33r6pyjel0/related_products.png
.. |offers| image:: https://dl.dropboxusercontent.com/s/nvdjwwfyoo7hk6x/offers.png
.. |offers2| image:: https://dl.dropboxusercontent.com/s/s165a738ez4vsdq/offers2.png
.. |product_info| image:: https://dl.dropboxusercontent.com/s/aqgdfeuvrrdjfek/product_info.png
.. |brand| image:: https://dl.dropboxusercontent.com/s/esun7ckldock2b2/brand.png
.. |brand_not| image:: https://dl.dropboxusercontent.com/s/q4l3qesmsqzvd8s/brand_not.png
.. |rating| image:: https://dl.dropboxusercontent.com/s/jgxjtnss6y68j78/rating.png
.. |sku| image:: https://dl.dropboxusercontent.com/s/3ymj186jxdaax8e/sku.png
.. |bulk_offer| image:: https://dl.dropboxusercontent.com/s/p1n2chkai13b9ww/bulk_offer.png
    :height: 300
.. _github: https://github.com/scrapinghub/unified-schema