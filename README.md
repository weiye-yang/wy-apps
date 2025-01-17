OpenLDBWS Rail Tools
========================

This repository uses the National Rail Live
Departure Boards Web Service (OpenLDBWS), located at the following URL:
* https://lite.realtime.nationalrail.co.uk/OpenLDBWS/

To use the service, you will need a token which is available by
signing up at the following URL:
* https://realtime.nationalrail.co.uk/OpenLDBWSRegistration/

You will need to add this as an `RAIL_TOKEN` environment variable. You can add it to
a `.env` file in the root directory which is loaded into the environment variables
by the `python-dotenv` package.

For phone push notifications, you will also need to set up a Pushover account:
* https://pushover.net/

And add the token and user id as environment variables `PUSHOVER_TOKEN` and 
`PUSHOVER_USER` respectively.

Updating the WSDL
-----------------

Periodically, a new version of the WSDL will be released at:

* https://lite.realtime.nationalrail.co.uk/OpenLDBWS/

This code is written for version 2021-11-01.  To update it to use a
later version, edit `client.py` and change the `wsdl` argument.  

Support
-------

This code has been tested on Python 3.12.6.

For support and questions with using the OpenLDBWS, please use the
forum at the following URL:
 
 * https://groups.google.com/group/openraildata-talk