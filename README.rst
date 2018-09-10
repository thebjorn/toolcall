

toolcall - call external tool and get results
==================================================

This project is set up to demonstrate the toolcall api.

Create a new virtualenv and install the requirements, and the toolcall
package in dev mode::

    toolcall> pip install -r requirements.txt
    toolcall> pip install -e .

To create the sqlite database with syncdb, but answer no to the superuser
question::

    (toolcall) go|c:\github\toolcall> python manage.py syncdb
    Operations to perform:
      Synchronize unmigrated apps: toolcall
      Apply all migrations: admin, contenttypes, auth, sessions
    Synchronizing apps without migrations:
      Creating tables...
        Creating table toolcall_client
        Creating table toolcall_tool
        Creating table toolcall_toolcall
        Creating table toolcall_toolcalllog
        Creating table toolcall_toolcallresult
      Installing custom SQL...
      Installing indexes...
    Running migrations:
      Applying contenttypes.0001_initial... OK
      Applying auth.0001_initial... OK
      Applying admin.0001_initial... OK
      Applying sessions.0001_initial... OK

    You have installed Django's auth system, and don't have any superusers defined.
    Would you like to create one now? (yes/no): no

Load the included fixture::

    (toolcall) go|c:\github\toolcall> python manage.py loaddata dumpdata.json
    Installed 50 object(s) from 1 fixture(s)

The fixture contains a superuser with username/password == admin/admin, and
a regular user with username/password == user/user.

Run the server::

    python manage.py runserver

There is one client defined which you can view at:
http://127.0.0.1:8000/admin/toolcall/client/1/
(in production it is a requirement that the urls use a https transport with a valid
certificate).

The endpoints are declared at http://127.0.0.1:8000/.api/toolcall/v2/
It is not necessary to discover these (i.e. they can be manually read and hard-coded
into your client). We will update the api version if any of the urls change.

Open the start page at http://127.0.0.1:8000/ Since both the server and the client
are running on the same host here, it is better if you use a separate web browser from
the one you opened the admin site in.

Step 1: user clicks button to start tool/exam
---------------------------------------------
view: toolcall.views.home

The button opens a new window for running the exam. The window is opened with ``noopener``.

.. note:: as a shortcut I've re-used the admin site's login template for user logins.


Step 2: user is redirected to client with access_token
------------------------------------------------------
view toolcall.tooluser.views.start_tool

This view will normally redirect directly to the client, but here it presents
a page with some debug information. Click the "start tool" link at the bottom to
proceed.  In debug mode you have 200 seconds (``toolcall.defaults.TOOLCALL_TOKEN_TIMEOUT_SECS``
before the token is invalid).

Step 3: client
--------------
Clients need to implement the urls/views in toolcall/toolimplementor.

There are two urls that need to be implemented. Here they're called::

    url(r'^start-token/$', views.receive_start_token),
    url(r'^result-token/$', views.send_result_data),

which correspond to the values in the Client model.

``start-token`` is called after step 2 when the user is redirected with an access_token.
Check ``toolcall/toolimplementor/views.py:receive_start_token`` for a sample implementation.
I would suggest creating auth.Users and logging them in.

.. note:: You'll need to save some of the start data values so you can return them to us
          with the result.

The client runs the exam
~~~~~~~~~~~~~~~~~~~~~~~~
I've illustrated this by a redirect to ``toolcall.toolimplementor.views.run_my_tool``
that only creates a token and a result structure, store them in redis, and sends the token
to the server's result token url (the client name is also sent).

Step 4: the server sends result token
-------------------------------------
The server immediately sends the token back to the client to the
``toolcall.toolimplementor.views.send_result_data`` view (``result-token/`` url, as defined
in the Client model).

The client fetches the result data from redis and returns it.


Comments
--------
- I've used redis for token storage because it's part of our stack. The client is of course
  free to use any other solution.
- the persnr/unique ID algorithm here is not the one we use, but creates similar looking
  unique IDs that are unique and durable per user.
- I've kept the client code simple for pedagogical reasons. ``toolcall.views`` is more similar
  to what we use in production.
- The ToolcallResult model is not used here (it normally stores the result data verbatim.
- The progress records (ToolCall, ToolCallLog) are functional but not safe (the transitions
  are neither correct nor checked - but they are logged..)





































