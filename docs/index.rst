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

=================================== ==============================================================
`DISCOURSE_SECRET`                  Secret string of your choice (at least 10 characters).

`DISCOURSE_API_USERNAME`            Username of an administrator of your Discourse application.

`DISCOURSE_API_KEY`                 The API key generated for the same Discourse administrator.

`DISCOURSE_URL`                     The base URL of your Discourse application
=================================== ==============================================================

In order to enable SSO you should also ensure that the following your Discourse
application is configured, via the **Admin** section, as follows:

=================================== ==============================================================
`enable_sso`                        Enabled

`sso_url`                           ``http://{your-server-ip-address}/discourse/oauth-authorized``

`sso_secret`                        The value chosen for `DISCOURSE_SECRET`.

`sso_overides_email`                Enabled

`sso_overides_username`             Enabled

`sso_overrides_name`                Enabled

`sso_overrides_avatar`              Enabled

`allow_uploaded_avatars`            Disabled

`logout_redirect`                   ``http://{your-server-ip-address}/discourse/signout``
=================================== ==============================================================

In order for the API client to work you should also make sure that the IP address of your server
is added to the Discourse whitelist, via **Admin > Logs > Screened IPs**.


Theme Integration
=================

To achieve better integration with your main PyBossa theme you can any navigation
links as follows:

.. code-block:: HTML+Django

    {% if 'pybossa_discourse' in plugins %}
        <a href="{{ url_for('discourse.index') }}">Community</a>
    {% endif %}

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

- The user visits ``http://{pybossa-site-url}/discourse/index``.
- The user clicks the **Log In** button from within the Discourse application.
- An API call is made regarding the user, such as one to retrieve their notifications.


Global Environment Variable
===========================

The plugin provides a global environment variable for easier interaction with
the Discourse API. This could be useful for doing things like this::

.. code-block:: HTML+Django

    <!-- Navigation link with current user's unread notification count -->
    <li class="nav-link">
        {% if 'pybossa_discourse' in plugins %}
        <a href="{{ url_for('discourse.index')}}">
            Community <span id="notifications" class="badge badge-info"></span>
        </a>
        <script>
            var notifications = {{ discourse.user_unread_notifications_count() }};
            if (notifications > 0) {
                $('#notifications').html(notifications);
            }
        </script>
        {% else %}
        <a href="{{ url_for('account.index')}}">Community</a>
        {% endif %}
    </li>

See the API documentation below for full details of the methods available.


API
===

.. module:: pybossa_discourse

.. autoclass:: DiscourseClient
   :members:
