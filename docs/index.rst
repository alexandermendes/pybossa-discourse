pybossa-discourse
*****************

A PyBossa plugin for Discourse integration.


Installation
============

Copy the **pybossa_discourse** folder into your PyBossa plugins directory, configure
the plugin as below and restart the server.


Configuration
=============

The following configuration settings should all be added to your main PyBossa
configuration file:

=================================== ==========================================================
`DISCOURSE_SECRET`                  Secret string of at least 10 characters used to
                                    encrypt/decrypt SSO information.
=================================== ==========================================================
`DISCOURSE_API_USERNAME`            Username of an administrator of your Discourse
                                    application.
=================================== ==========================================================
`DISCOURSE_API_KEY`                 The Discourse API key generated for the same Discourse
                                    administrator as above (visit the user's profile and click
                                    the **Admin** button).
=================================== ==========================================================
`DISCOURSE_URL`                     The base URL of your Discourse application
                                    (e.g. http://discuss.example.com).
=================================== ==========================================================

In order to enable SSO you should also ensure that the following your Discourse
application is configured, via the **Admin** section, as follows:

=================================== ==========================================================
`enable_sso`                        Enabled
=================================== ==========================================================
`sso_url`                           http://{your-server-ip-address}/discourse/oauth-authorized
=================================== ==========================================================
`sso_secret`                        The value chosen for `DISCOURSE_SECRET`.
=================================== ==========================================================
`sso_overides_email`                Enabled
=================================== ==========================================================
`sso_overides_username`             Enabled 
=================================== ==========================================================
`sso_overrides_name`                Enabled
=================================== ==========================================================
`sso_overrides_avatar`              Enabled
=================================== ==========================================================
`allow_uploaded_avatars`            Disabled    
=================================== ==========================================================
`logout_redirect`                   http://{your-server-ip-address}/discourse/signout
=================================== ==========================================================


Theme Integration
=================

To achieve better integration with your main PyBossa theme you can update it
as follows:

Links to Discourse:

.. code-block:: HTML+Django

    {% if 'pybossa_discourse' in plugins %}
        <a href="{{ url_for('discourse.index') }}">Community</a>
    {% endif %}


Sign out:

.. code-block:: HTML+Django
    
    {% if 'pybossa_discourse' in plugins %}
        <a href="{{ url_for('discourse.signout') }}">Sign out</a>
    {% endif %}


SSO
===

Once Single sign-on is configured users that sign in via your PyBossa application
will be automatically signed in to Discourse.

Discourse accounts will be created automatically the first time any of the
following this happen:

- The user visits http://{pybossa-site-url}/discourse/index.
- The user clicks the **Log In** button from within the Discourse application.
- An API call is made regarding the user, such as one to retrieve their notifications.


Discourse Global Environment Variable
=====================================

The plugin provides a global environment variable for easier interaction with
the Discourse API. This variable will be made available to all templates of your
PyBossa application. It returns the result of an API call in JSON format, for
example, the following will return all categories, if the plugin is enabled:

.. code-block:: HTML+Django

    {% if 'pybossa_discourse' in plugins %}
        {{ discourse.categories }}
    {% endif %}

See the API documentation below for full details of the methods available.


API
===

.. module:: pybossa_discourse

.. autoclass:: DiscourseClient
   :members:

