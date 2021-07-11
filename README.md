*airwaves-cli* is a small, single purpose command line utility for uploading data to the Internet Archive for the [Unlocking the Airwaves] project. Page scans of digitized archival folders are packaged into a zip file and then uploaded to the [Media History] collection at the Internet Archive using their API. The uploaded data includes metadata for the folder which is being curated in an Airtable database.

## Install

For convenience the airwaves-cli is distributed on the Python Package Index. Once you have Python installed you can:

    pip install airwaves

## Run

Once the airwaves package is installed you can publish an item that has been cataloged in
our AirTable database by giving the *upload* subcommand a folder identifier and the name of the zip file containing the page scans for that folder.

    airwaves upload naeb-b110-f04-03 naeb-b110-f04-03.zip

The first time you run airwaves it will prompt you for the Airtable and Internet
Archive API keys since these are private to the project.

If you want to see all the NAEB items by searching the [AAPB] website you can:

    airwaves items

[AAPB]: http://americanarchive.org/
[Unlocking the Airwaves]: https://mith.umd.edu/mith-receives-neh-grant-for-unlocking-the-airwaves-revitalizing-an-early-public-and-educational-radio-collection/
[release]: https://github.com/umd-mith/airwaves/releases/
[Media History]: https://archive.org/details/mediahistory
