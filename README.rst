YouShouldRead
=============

|ci| |docs| |uptime| |version|

.. |ci| image:: https://img.shields.io/circleci/project/github/TheKevJames/you-should-read/master.svg?style=flat-square
    :alt: CI Status
    :target: https://circleci.com/gh/TheKevJames/you-should-read/tree/master

.. |docs| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat-square
    :alt: Documentation Status
    :target: https://youshouldread.readthedocs.io/en/latest

.. |uptime| image:: https://img.shields.io/uptimerobot/ratio/7/m779314084-c8169da99e52393100a228f2.svg?style=flat-square
    :alt: Deployment Uptime
    :target: https://youshouldread.thekev.in

.. |version| image:: https://img.shields.io/github/release/TheKevJames/you-should-read.svg?style=flat-square
    :alt: Version
    :target: https://github.com/TheKevJames/you-should-read/releases/latest

Development
-----------

To build and run YouShouldRead for local development, run::

    docker-compose up --build

To apply database migrations, we use `sqitch`_. To update your local database to
the most recent version, run::

    cd database/
    sqitch deploy

To fill your database with testset data, run::

    psql -h localhost -U postgres postgres -f database/testset.sql

.. _`sqitch`: http://sqitch.org/
