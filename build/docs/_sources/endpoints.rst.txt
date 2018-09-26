.. _endpoints:

endpoints
---------

Server
..........
The server has two endpoints. The endpoints are defined in
toolcall/toolcall-api.yaml and are also available from
http://127.0.0.1:8000/.api/toolcall/v2/

.. todo:: the production server is not ready for v2 yet, but this sample
          package does.

start_data
~~~~~~~~~~~~~~
In this sample app it is: http://localhost:8000/fetch-token/
It should be called with the start-data token as a GET parameter
named ``access_token``, e.g.::

    http://localhost:8000/fetch-token/?access_token=1W6ofOChZt1AS4bdpkbOVKpdptVi0YDB48-UAZXz8PuB06cvNtwoiXBM20

result_token
~~~~~~~~~~~~~
In this sample app it is: http://localhost:8000/result/
It should be called with the result token as a GET parameter
named ``access_token``, and the client name in a GET parameter
named ``client``, e.g.::

    http://localhost:8000/result/?access_token=3525841484&client=testclient

Client
..........
The client has two endpoints. The endpoints are defined in the
:class:`toolcall.models.tool_models.Client` model.

receive_start_token_url
~~~~~~~~~~~~~~~~~~~~~~~~~
Url where we redirect the end user with a token. In the sample client this is:
http://localhost:8000/client/start-token/


receive_result_token_url
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Url where we return the result token and expect result data in return.
In the sample client this is:
http://localhost:8000/client/result-token/

