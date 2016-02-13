============
Scrapy Cloud
============

*Scrapy Cloud* is a Scrapinghub service to deploy and run `Scrapy`_ spiders and
:ref:`custom python scripts <sc-scripts>`.

Plans & Pricing
===============

Scrapy Cloud has four types of plans available:

* The *Free* plan is completely free and allows 1 concurrent crawl. Data is retained for 7 days.
* The *Shared* plan offers 30 day data retention and lets you run up to 4 concurrent crawls.
* *Dedicated* plans provide a dedicated server for running your spiders with more resources. Dedicated plans can run a larger number of concurrent crawls and have longer data retention periods (60+ days).
* An *Enterprise* plan is a custom plan tailored to your needs.

Check the `Scrapinghub Pricing`_ page for more details.

Creating a Scrapy Spider
========================

Let's start by creating our Scrapy spider. If you already have a Scrapy project, you can skip this section.

This assumes you have Scrapy already installed, otherwise please refer to the `Scrapy installation guide`_.

For this example, we will build a spider to scrape the *CrunchBase* directory. For simplicity sake, we are going to restrict it to the *Pets* category:

    https://www.crunchbase.com/companies?q=pets

We begin by creating a Scrapy project which we will call ``companies``::

    $ scrapy startproject companies

Then we create a spider for ``crunchbase.com``::

    $ scrapy genspider crunchbase crunchbase.com -t basic
    Created spider 'crunchbase' using template 'basic' in module:
      companies.spiders.crunchbase

Then we edit the spider::

    $ scrapy edit crunchbase

Here is the code (for simplicity we are defining the item in the same file):

.. literalinclude:: _static/sc-crunchbase.py

For more information about Scrapy please refer to the `Scrapy documentation`_.

.. _deploy:

Deploying a Scrapy Spider
=========================

.. note::
    You will need the :ref:`Scrapinghub command line client <shub>` to deploy
    projects to Scrapy Cloud, so install it if you have not done so yet.

The next step is to deploy your Scrapy project to Scrapinghub. You will need
your API key and the numeric ID of your Scrapinghub project. You can find both
of these on your project's *Deploy* page. First, run::

    $ shub login

to save your API key to a local file (``~/.scrapinghub.yml``). You can delete
it from there anytime via ``shub logout``. Next, run::

    $ shub deploy

to be guided through a wizard that will set up the project configuration file
(``scrapinghub.yml``) for you. After the wizard, your project will be uploaded
to Scrapinghub. You can re-trigger deployment (without having to go through the
wizard again) anytime via another call to ``shub deploy``.

Now you can schedule your spider to run on Scrapinghub::

    $ shub schedule crunchbase
    Spider crunchbase scheduled, job ID: 12345/1/1
    Watch the log on the command line:
        shub log -f 1/1
    or print items as they are being scraped:
        shub items -f 1/1
    or watch it running in Scrapinghub's web interface:
        https://dash.scrapinghub.com/p/12345/job/1/1

And watch it run (replace ``1/1`` with the job ID ``shub`` gave you on the
previous command, you can leave out the project ID)::

    shub log -f 1/1

Alternatively, you can go to your project page and schedule the spider there:

.. image:: _static/sc-schedule.png
   :width: 300px

|

Once the job has finished, or while it's running, you can click on the job to
review the scraped data and other information about the job:

.. image:: _static/sc-items-scraped.png
   :width: 500px

|

Dependencies and External Libraries
===================================

The Scrapy Cloud platform comes with some libraries pre-installed that you can
use in your code without uploading an egg. `This support article
<http://support.scrapinghub.com/topic/205467-supported-libraries-on-scrapy-cloud/>`_
describes exactly which library versions are available, and you can also
subscribe to get notified of changes to such libraries.

If your project needs code from an external Python library, you need to upload
a Python egg of that dependency. If available, you can simply import the
library from PyPI (e.g. the ``requests`` library)::

    shub deploy-egg --from-pypi requests

Alternatively, you can point to a repository URL::

    shub deploy-egg --from-url https://github.com/kennethreitz/requests.git

If you want to provide your own library for your project, proceed as follows:

#. Write your code.
#. Add a ``setup.py`` file in the base package folder, e.g.::

    from setuptools import setup, find_packages
    setup(
        name = "mylibrary",
        version = "0.1",
        packages = find_packages(),
    )

#. Run ``shub deploy-egg PROJECTID`` to deploy to your project. (Note that you
   need to add the project ID since you usually are no longer within the Scrapy
   project's directory tree.)

See `setuptools`_ for details about egg concepts, preparation and building.

.. _sc-scripts:

Running custom python scripts
=============================

You can also run custom python scripts (ie. non Scrapy spiders) on Scrapy
Cloud. They need to be declared in the ``scripts`` section of your project
``setup.py`` file.

.. note:: Keep in mind that the project deployed needs to be a Scrapy project. This is a limitation for now, which will be removed in the future.

Here is a ``setup.py`` example for a project that ships a ``hello.py`` script::

    from setuptools import setup, find_packages

    setup(
        name         = 'myproject',
        version      = '1.0',
        packages     = find_packages(),
        scripts      = ['bin/hello.py'],
        entry_points = {'scrapy': ['settings = myproject.settings']},
    )

After you :ref:`deploy <deploy>` your project, you will see the ``hello.py``
script right below the list of spiders, in the schedule box (on Scrapinghub
dashboard).

You can also setup periodic jobs to run the script or do it via the API.

For running the script through the API, you need to use a private API (which may subject to change in the future). Here is an example using ``curl``::

    curl -X POST -d '{"job_cmd": ["py:hello.py"]}' https://storage.scrapinghub.com/jobq/1/push


.. _Scrapy: http://scrapy.org
.. _Scrapy installation guide: http://doc.scrapy.org/en/latest/intro/install.html
.. _Scrapy documentation: http://doc.scrapy.org/
.. _setuptools: http://peak.telecommunity.com/DevCenter/setuptools
.. _Scrapinghub Pricing: http://scrapinghub.com/pricing/
