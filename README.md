A command line utility for working with the [Unlocking the Airwaves] project.

Download the latest [release], unzip and then:

    sudo python setup.py install

Then you can publish an item that has been cataloged in our AirTable database:

    airwaves naeb-b110-f04-03 naeb-b110-f04-03.zip

The first time you run airwaves it will prompt you for the Airtable and Internet
Archive API keys.

If you want to see all the NAEB items by searching the [AAPB] website you can:

    airwaves items

[AAPB]: http://americanarchive.org/

[Unlocking the Airwaves]: https://mith.umd.edu/mith-receives-neh-grant-for-unlocking-the-airwaves-revitalizing-an-early-public-and-educational-radio-collection/

[release]: https://github.com/umd-mith/airwaves/releases/
