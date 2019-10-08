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

.. _Product:

**Product**
====================
The following fields are available for products:

=======================  =======================================================================  ================================================================================================================================================================================================================
Fields                   Format                                                                   Description
=======================  =======================================================================  ================================================================================================================================================================================================================
`aggregateRating`_       anyOf required: ratingValue, bestRating, reviewCount                     The overall rating, based on a collection of reviews or ratings.

                         - Type: ``object``

                         - **Fields:**                                                            |rating|

                           1. ratingValue: ``number``                                             .. code-block:: javascript
                           2. bestRating: ``number``
                           3. reviewCount: ``integer``                                              {
                                                                                                    'ratingValue': 4.0,
                                                                                                    'bestRating': 5.0,
                                                                                                    'reviewCount': 23
                                                                                                    }
                                                                                                       
`ratingHistogram`_       - Type: ``array``                                                        This fields provides the detailed distribution of ratings across the entire rating scale

                         - Items: ``ratingHistogram``

                         - **Fields:**                                                            |histogram|

                           1. ratingOption: ``string``                                            .. code-block:: javascript
                           2. ratingCount: ``number``
                           3. ratingPercentage: ``number``                                          [{'ratingValue': '5', 'ratingPercentage': 61},
                                                                                                     {'ratingValue': '4', 'ratingPercentage': 12},
                                                                                                     {'ratingValue': '3', 'ratingPercentage': 6},
                                                                                                     {'ratingValue': '2', 'ratingPercentage': 5},
                                                                                                     {'ratingValue': '1', 'ratingPercentage': 16}
                                                                                                    ]
                                                                                                       
brand                    - Type: ``string``                                                       The brand associated with the product.





                                                                                                  |brand|

                                                                                                  .. code-block:: javascript

                                                                                                    {'brand': 'Samsung'}

                                                                                                  |brand_not|

                                                                                                  **No brand is returned**
                                                                                                       
`breadcrumbs`_           - Type: ``array``                                                        A list of breadcrumbs with optional name and URL.

                         - Items: ``breadcrumb``                                                  .. code-block:: javascript

                         - **Fields:**                                                              [{'name': 'Cell Phones & Accessories',
                                                                                                      'link': 'https://amz.com/cell-phones-accessories'}...]
                           1. name: ``string``                                                         
                           2. link: ``string``
                              
description              - Type: ``string``                                                       A description of the product     
images                   - Type: ``array``                                                        list of URL or data URL values of all images of the product (may include the main image).     

                         - Items: ``url``     
mainImage                - Type: ``url``                                                          A URL or data URL value of the main image of the product.     

                         - Format: ``uri``     
name                     - Type: ``string``                                                       The name of the product     
`offers`_                - Type: ``array``                                                        This field contains rich information pertaining to all the buying options offered on a product.
                                                                                                  Detailed information regarding all the properties returned in this field is available in the `offers`_ section.
                         - Items: ``offer``

                         - **Fields:**
                                                                                                  |offers2|
                           1. availability: ``string``
                           2. currency: ``string``                                                .. code-block:: javascript
                           3. regularPrice: ``string``
                           4. price: ``string``                                                     [{'availability': 'InStock',
                           5. `eligibleQuantity`_: ``object``                                         'price':'129.99',
                           6. `seller`_: ``object``                                                   'currency': '$'
                           7. `shippingInfo`_: ``object``                                             'itemCondition':
                           8. `itemCondition`_: ``object``                                              {
                           9. `pricePerUnit`_: ``object``                                               'type': 'used',
                                                                                                        'description': 'Used - Very Good'
                                                                                                        },
                                                                                                        'seller':{
                                                                                                                   'name':'Java Junkie',
                                                                                                                   'url': 'https://amz.com/gp/aag/main/seller=A8K32FFKI51FKN',
                                                                                                                   'identifier': 'A8K32FFKI51FKN',
                                                                                                                   'aggregateRating':{
                                                                                                                   'reviewCount':479,
                                                                                                                   'bestRating':5
                                                                                                                   },
                                                                                                                   'shippingInfo':{
                                                                                                                   'minDays':'15',
                                                                                                                   'maxDays':'30',
                                                                                                                   'description':'Arrives between September 3-18.'
                                                                                                                   }
                                                                                                                  }
                                                                                                    }]
                                                                                                       
`additionalProperty`_    - Type: ``array``                                                             

                         - Items: ``name_value``

                         - **Fields:**

                           1. name: ``string``
                           2. value: ``number``, ``string``, ``boolean``, ``object``, ``array``
                              
sku                      - Type: ``string``                                                            
mpn                      - Type: ``string``                                                       The Manufacturer Part Number (MPN) of the product. The product would have the same MPN across different e-commerce websites.     
`gtin`_                  - Type: ``array``                                                        Standardized GTIN product identifier which is unique for a product across different sellers.
                                                                                                  It includes the following ype: isbn10, isbn13, issn, ean13, upc, ismn, gtin8, gtin14.
                         - Items: ``dictionary``                                                  gtin14 corresponds to former names EAN/UCC-14, SCC-14, DUN-14,UPC Case Code, UPC Shipping Container Code.
                                                                                                  ean13 also includes the jan (japanese article number)
                         - **Fields:**
                                                                                                  .. code-block:: javascript
                         - **Fields:**
                           1. type: ``string``                                                      [{'type': 'isbn13', 'value': '9781933624341'}]
                           2. value: ``string``                                                        

                         Required: ``type``, ``value``
                              
manufacturer             - Type: ``string``                                                       The manufacturer of the product.     
size                     - Type: ``string``                                                       Denotes the size of the product. Pertinent to products such as garments, shoes, accessories etc     
`height`_                anyOf required: maxValue, minValue, value                                A value or interval for product characteristics and other purposes     

                         - Type: ``quantitativeValue``

                         - **Fields:**

                           1. maxValue: ``number``
                           2. minValue: ``number``
                           3. value: ``number``
                           4. unitText: ``string``
                           5. description: ``string``
                              
`width`_                 anyOf required: maxValue, minValue, value                                A value or interval for product characteristics and other purposes     

                         - Type: ``quantitativeValue``

                         - **Fields:**

                           1. maxValue: ``number``
                           2. minValue: ``number``
                           3. value: ``number``
                           4. unitText: ``string``
                           5. description: ``string``
                              
`depth`_                 anyOf required: maxValue, minValue, value                                A value or interval for product characteristics and other purposes     

                         - Type: ``quantitativeValue``

                         - **Fields:**

                           1. maxValue: ``number``
                           2. minValue: ``number``
                           3. value: ``number``
                           4. unitText: ``string``
                           5. description: ``string``
                              
`weight`_                anyOf required: maxValue, minValue, value                                A value or interval for product characteristics and other purposes     

                         - Type: ``quantitativeValue``

                         - **Fields:**

                           1. maxValue: ``number``
                           2. minValue: ``number``
                           3. value: ``number``
                           4. unitText: ``string``
                           5. description: ``string``
                              
`volume`_                anyOf required: maxValue, minValue, value                                A value or interval for product characteristics and other purposes     

                         - Type: ``quantitativeValue``

                         - **Fields:**

                           1. maxValue: ``number``
                           2. minValue: ``number``
                           3. value: ``number``
                           4. unitText: ``string``
                           5. description: ``string``
                              
url                      - Type: ``url``                                                               

                         - Format: ``uri``     
releaseDate              - Type: ``string``                                                       Date on which the product was released or listed on the website in ISO 8601 date format

                         - Format: ``date``                                                       .. code-block:: javascript

                                                                                                    {'releaseDate': '2016-12-18'}
                                                                                                       
color                    - Type: ``string``                                                       The color of the product     
relatedProducts          - Type: ``array``                                                        This field captures all products that are recommended by the website while browsing the product of interest. Related products can thus be used to gauge customer buying description:
                                                                                                  The ``relationshipName`` field describes the relationship while the ``products`` field contains a list of items have the same ``product`` schema, thus extracting all available fields as defined in this table.
                         - Items: ``relatedProduct``

                         - **Fields:**
                                                                                                  |related_products|
                           1. relationshipName: ``string``                                             
                           2. products: ``array``
                              
variants                 - Type: ``array``                                                        This field returns a list of variants of the product. Each variant has the same schema as the `Product`_ schema defined in this table.  

                         - Items: ``variant``     
reviews                  - Type: ``array``                                                             
=======================  =======================================================================  ================================================================================================================================================================================================================




allOf:

- baseProduct


- relatedProducts


- variants


- reviews




.. _additionalProperty:

**additionalProperty**


==========  ===================================================================  =============
Fields      Format                                                               Description
==========  ===================================================================  =============
name        - Type: ``string``                                                        
value       - Type: ``['number', 'string', 'boolean', 'object', 'array']``            
==========  ===================================================================  =============






.. _aggregateRating:

**aggregateRating**


================  ========================  =============
Fields            Format                    Description
================  ========================  =============
ratingValue       - Type: ``number``             
bestRating        - Type: ``number``             
reviewCount       - Type: ``integer``            
================  ========================  =============






.. _breadcrumbs:

**breadcrumbs**


=========  =======================  =============
Fields     Format                   Description
=========  =======================  =============
name       - Type: ``string``            
link       - Type: ``url``               

           - Format: ``uri``     
=========  =======================  =============






.. _depth:

**depth**


================  =======================  ==================================================
Fields            Format                   Description
================  =======================  ==================================================
maxValue          - Type: ``number``       Maximun value allowed     
minValue          - Type: ``number``       Minimun value required     
value             - Type: ``number``       Exact value required     
unitText          - Type: ``string``       Unit of measurement     
description       - Type: ``string``       Free text from where this range was extracted     
================  =======================  ==================================================






.. _gtin:

**gtin**


==========  =======================  =============
Fields      Format                   Description
==========  =======================  =============
type        - Type: ``string``            
value       - Type: ``string``            
==========  =======================  =============






.. _height:

**height**


================  =======================  ==================================================
Fields            Format                   Description
================  =======================  ==================================================
maxValue          - Type: ``number``       Maximun value allowed     
minValue          - Type: ``number``       Minimun value required     
value             - Type: ``number``       Exact value required     
unitText          - Type: ``string``       Unit of measurement     
description       - Type: ``string``       Free text from where this range was extracted     
================  =======================  ==================================================






.. _offers:

**offers**


======================  =========================================  ============================================================================================================
Fields                  Format                                     Description
======================  =========================================  ============================================================================================================
availability            - Type: ``string``                              
currency                - Type: ``string``                              
regularPrice            - Type: ``string``                         The price at which the product was being offered and which is presented as a reference to the current price.
                                                                   It may be represented by original price, list price or maximum retail price for which the product is sold.
                                                                   This field is only returned if it is explicitly mentioned in the offer or the product page.
                                                                        
price                   - Type: ``string``                         The price at which the product is being offered. If there is only one price associated with the offer, it
                                                                   is this field in which it is returned.
                                                                        
`eligibleQuantity`_     anyOf required: maxValue, minValue, value  A value or interval for product characteristics and other purposes     

                        - Type: ``quantitativeValue``

                        - **Fields:**

                          1. maxValue: ``number``
                          2. minValue: ``number``
                          3. value: ``number``
                          4. unitText: ``string``
                          5. description: ``string``
                             
`seller`_               anyOf required: name, url, identifier           

                        - Type: ``seller``

                        - **Fields:**

                          1. name: ``string``
                          2. url: ``string``
                          3. identifier: ``string``
                          4. aggregateRating: ``object``
                             
`shippingInfo`_         anyOf required: price, description              

                        - Type: ``shippingInfo``

                        - **Fields:**

                          1. currency: ``string``
                          2. price: ``string``
                          3. minDays: ``number``
                          4. maxDays: ``number``
                          5. averageDays: ``number``
                          6. description: ``string``
                             
`availableAtOrFrom`_    anyOf:                                          

                        - Type: ``postalAddress``

                          Fields:

                          1. postalCode: ``string``

                          2. streetAddress: ``string``

                          3. addressCountry: ``string``

                          4. addressLocality: ``string``

                          5. addressRegion: ``string``

                        - Type: ``string``     
`areaServed`_           anyOf:                                          

                        - Type: ``postalAddress``

                          Fields:

                          1. postalCode: ``string``

                          2. streetAddress: ``string``

                          3. addressCountry: ``string``

                          4. addressLocality: ``string``

                          5. addressRegion: ``string``

                        - Type: ``string``     
`itemCondition`_        - Type: ``object``                         A predefined value and a textual description of the condition of the product included in the offer     

                        - **Fields:**

                          1. type: ``string``
                          2. description: ``string``


                        Required: ``type``, ``description``
                             
`pricePerUnit`_         - Type: `pricePerUnit`_                         

                        - **Fields:**

                          1. price: ``string``
                          2. currency: ``string``
                          3. unit: ``string``


                        Required: ``unit``
                             
======================  =========================================  ============================================================================================================






.. _ratingHistogram:

**ratingHistogram**


=====================  =======================  =================================================================
Fields                 Format                   Description
=====================  =======================  =================================================================
ratingOption           - Type: ``string``       A quantitative or qualitative value depicting the rating     
ratingCount            - Type: ``number``       The number of reviews/ratings for a certain rating value     
ratingPercentage       - Type: ``number``       The percentage of reviews/ratings for a certain rating value     
=====================  =======================  =================================================================






.. _volume:

**volume**


================  =======================  ==================================================
Fields            Format                   Description
================  =======================  ==================================================
maxValue          - Type: ``number``       Maximun value allowed     
minValue          - Type: ``number``       Minimun value required     
value             - Type: ``number``       Exact value required     
unitText          - Type: ``string``       Unit of measurement     
description       - Type: ``string``       Free text from where this range was extracted     
================  =======================  ==================================================






.. _weight:

**weight**


================  =======================  ==================================================
Fields            Format                   Description
================  =======================  ==================================================
maxValue          - Type: ``number``       Maximun value allowed     
minValue          - Type: ``number``       Minimun value required     
value             - Type: ``number``       Exact value required     
unitText          - Type: ``string``       Unit of measurement     
description       - Type: ``string``       Free text from where this range was extracted     
================  =======================  ==================================================






.. _width:

**width**


================  =======================  ==================================================
Fields            Format                   Description
================  =======================  ==================================================
maxValue          - Type: ``number``       Maximun value allowed     
minValue          - Type: ``number``       Minimun value required     
value             - Type: ``number``       Exact value required     
unitText          - Type: ``string``       Unit of measurement     
description       - Type: ``string``       Free text from where this range was extracted     
================  =======================  ==================================================






.. _areaServed:

**areaServed**


====================  =======================  =================================================================================================================================================
Fields                Format                   Description
====================  =======================  =================================================================================================================================================
postalCode            - Type: ``string``       Postal code of the address     
streetAddress         - Type: ``string``       The street address. For example, 1600 Amphitheatre Pkwy.     
addressCountry        - Type: ``string``       The country. For example, USA. You can also provide the two-letter ISO 3166-1 alpha-2 country code. https://en.wikipedia.org/wiki/ISO_3166-1     
addressLocality       - Type: ``string``       The locality in which the street address is, and which is in the region. For example, Mountain View.     
addressRegion         - Type: ``string``       The region in which the locality is, and which is in the country. For example, California.     
====================  =======================  =================================================================================================================================================




anyOf:

- postalAddress


- postalCode


- string




.. _availableAtOrFrom:

**availableAtOrFrom**


====================  =======================  =================================================================================================================================================
Fields                Format                   Description
====================  =======================  =================================================================================================================================================
postalCode            - Type: ``string``       Postal code of the address     
streetAddress         - Type: ``string``       The street address. For example, 1600 Amphitheatre Pkwy.     
addressCountry        - Type: ``string``       The country. For example, USA. You can also provide the two-letter ISO 3166-1 alpha-2 country code. https://en.wikipedia.org/wiki/ISO_3166-1     
addressLocality       - Type: ``string``       The locality in which the street address is, and which is in the region. For example, Mountain View.     
addressRegion         - Type: ``string``       The region in which the locality is, and which is in the country. For example, California.     
====================  =======================  =================================================================================================================================================




anyOf:

- postalAddress


- postalCode


- string




.. _eligibleQuantity:

**eligibleQuantity**


================  =======================  ==================================================
Fields            Format                   Description
================  =======================  ==================================================
maxValue          - Type: ``number``       Maximun value allowed     
minValue          - Type: ``number``       Minimun value required     
value             - Type: ``number``       Exact value required     
unitText          - Type: ``string``       Unit of measurement     
description       - Type: ``string``       Free text from where this range was extracted     
================  =======================  ==================================================


Let's take the following example to examine the aforementioned fields

.. |bulk_offer| image:: https://dl.dropboxusercontent.com/s/p1n2chkai13b9ww/bulk_offer.png
  :height: 300

|bulk_offer|

.. code-block:: javascript

  {'offers': [
    {'price': '11,98', 'currency': '$'},
    {'price': '10,78', 'currency': '$',
     'eligibleQuantity': {'min_value': '48',
                          'description': 'Buy 44 or more $9.33'}
    }
  ]




.. _itemCondition:

**itemCondition**


================  =======================  ================================================================================
Fields            Format                   Description
================  =======================  ================================================================================
type              - Type: ``string``       A predefined value of the condition of the product included in the offer     
description       - Type: ``string``       A textual description of the condition of the product included in the offer     
================  =======================  ================================================================================






.. _pricePerUnit:

**pricePerUnit**


=============  =======================  =============
Fields         Format                   Description
=============  =======================  =============
price          - Type: ``string``            
currency       - Type: ``string``            
unit           - Type: ``string``            
=============  =======================  =============






.. _seller:

**seller**


====================  ====================================================  ================================================================
Fields                Format                                                Description
====================  ====================================================  ================================================================
name                  - Type: ``string``                                    Name of the `seller`_  
url                   - Type: ``url``                                       URL for the `seller`_'s page  

                      - Format: ``uri``     
identifier            - Type: ``string``                                    Unique identifier assigned to the `seller`_ on the website  
`aggregateRating`_    anyOf required: ratingValue, bestRating, reviewCount  The overall rating, based on a collection of reviews or ratings.

                      - Type: ``aggregateRating``

                      - **Fields:**                                         |rating|

                        1. ratingValue: ``number``                          .. code-block:: javascript
                        2. bestRating: ``number``
                        3. reviewCount: ``integer``                           {
                                                                              'ratingValue': 4.0,
                                                                              'bestRating': 5.0,
                                                                              'reviewCount': 23
                                                                              }
                                                                                 
====================  ====================================================  ================================================================






.. _shippingInfo:

**shippingInfo**


==================  =================================  =============
Fields              Format                             Description
==================  =================================  =============
currency            - Type: ``string``                      
price               - Type: ``string``                      
minDays             - Type: ``number``                      
maxDays             - Type: ``number``                      
averageDays         - Type: ``number``                      
description         - Type: ``string``                      
`originAddress`_    anyOf:                                  

                    - Type: ``postalAddress``

                      Fields:

                      1. postalCode: ``string``

                      2. streetAddress: ``string``

                      3. addressCountry: ``string``

                      4. addressLocality: ``string``

                      5. addressRegion: ``string``

                    - Type: ``string``     
==================  =================================  =============






.. _originAddress:

**originAddress**


====================  =======================  =================================================================================================================================================
Fields                Format                   Description
====================  =======================  =================================================================================================================================================
postalCode            - Type: ``string``       Postal code of the address     
streetAddress         - Type: ``string``       The street address. For example, 1600 Amphitheatre Pkwy.     
addressCountry        - Type: ``string``       The country. For example, USA. You can also provide the two-letter ISO 3166-1 alpha-2 country code. https://en.wikipedia.org/wiki/ISO_3166-1     
addressLocality       - Type: ``string``       The locality in which the street address is, and which is in the region. For example, Mountain View.     
addressRegion         - Type: ``string``       The region in which the locality is, and which is in the country. For example, California.     
====================  =======================  =================================================================================================================================================




anyOf:

- postalAddress


- postalCode


- string




.. |rating| image:: https://dl.dropboxusercontent.com/s/jgxjtnss6y68j78/rating.png
.. |brand| image:: https://dl.dropboxusercontent.com/s/esun7ckldock2b2/brand.png
.. |offers2| image:: https://dl.dropboxusercontent.com/s/s165a738ez4vsdq/offers2.png
.. |histogram| image:: https://dl.dropboxusercontent.com/s/tqgvuujk362ztse/histogram.png
.. |brand_not| image:: https://dl.dropboxusercontent.com/s/q4l3qesmsqzvd8s/brand_not.png
.. |related_products| image:: https://dl.dropboxusercontent.com/s/phzqh33r6pyjel0/related_products.png
.. _Review:

**Review**
====================


===================  ===================================  =============
Fields               Format                               Description
===================  ===================================  =============
itemReviewed         - Type: ``string``                        
name                 - Type: ``string``                        
reviewBody           - Type: ``string``                        
`reviewRating`_      - Type: ``object``                        

                     - **Fields:**

                       1. ratingValue: ``textOrNumber``
                       2. bestRating: ``textOrNumber``
                       3. worstRating: ``textOrNumber``


                     Required: ``ratingValue``
                          
`author`_            - Type: ``object``                        

                     - **Fields:**

                       1. name: ``string``
                          
dateCreated          anyOf format: date-time, date             

                     - Type: ``dateOrDatetime``     
datePublished        anyOf format: date-time, date             

                     - Type: ``dateOrDatetime``     
dateModified         anyOf format: date-time, date             

                     - Type: ``dateOrDatetime``     
url                  - Type: ``url``                           

                     - Format: ``uri``     
votedHelpful         - Type: ``integer``                       
votedUnhelpful       - Type: ``integer``                       
isIncentivised       - Type: ``boolean``                       
isVerified           - Type: ``boolean``                       
===================  ===================================  =============






.. _author:

**author**


=========  =======================  =============
Fields     Format                   Description
=========  =======================  =============
name       - Type: ``string``            
=========  =======================  =============






.. _reviewRating:

**reviewRating**


================  =============================  =============
Fields            Format                         Description
================  =============================  =============
ratingValue       oneOf type: string, number          

                  - Type: ``textOrNumber``     
bestRating        oneOf type: string, number          

                  - Type: ``textOrNumber``     
worstRating       oneOf type: string, number          

                  - Type: ``textOrNumber``     
================  =============================  =============






