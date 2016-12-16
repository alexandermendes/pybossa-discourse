pybossa-discourse
*****************

A PyBossa plugin for Discourse integration.

Features:
- Use SSO to sign your PyBossa users into Discourse
- Make Discourse API requests from your PyBossa theme
- Embed Discourse comments into your PyBossa theme


Installation
============

Copy the **pybossa_discourse** folder into your PyBossa plugins directory, configure
the plugin as below and restart the server.


Configuration
=============

The following settings should all be added to your PyBossa configuration file:

=================================== ==============================================================
`DISCOURSE_SECRET`                  Secret string of your choice (at least 10 characters).

`DISCOURSE_API_USERNAME`            Username of an administrator of your Discourse application.

`DISCOURSE_API_KEY`                 The API key generated for the same Discourse administrator.

`DISCOURSE_URL`                     The base URL of your Discourse application
=================================== ==============================================================

In order to enable SSO you should also ensure that your Discourse application is configured,
via the **Admin** section, as follows:

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

To achieve better integration with your PyBossa theme you should navigation
links as follows:

.. code-block:: HTML+Django

    <!-- Go to your Discourse homepage -->
    {% if 'pybossa_discourse' in plugins %}
        <a href="{{ url_for('discourse.index') }}">Community</a>
    {% endif %}

.. code-block:: HTML+Django

    <!-- Sign a user out of Discourse when they sign out of PyBossa -->
    {% if 'pybossa_discourse' in plugins %}
        <a href="{{ url_for('discourse.signout') }}">Sign out</a>
    {% endif %}


SSO
===

With the plugin enabled, users that sign in via your PyBossa application will
be automatically signed in to Discourse. Discourse accounts will be created
automatically the first time any of the following things happen:

- The user visits ``http://{pybossa-site-url}/discourse/index``.
- The user clicks the **Log In** button from within the Discourse application.
- An API call is made regarding the user, such as one to retrieve their notifications.


API Environment Variable
========================

The plugin provides a global environment variable for easier interaction with
the Discourse API, which could be useful for adding things like this to your
PyBossa theme:

.. code-block:: HTML+Django

    <!-- Navigation link showing the current user's unread notification count -->
    <li class="nav-link">
        {% if 'pybossa_discourse' in plugins %}
        <a href="{{ url_for('discourse.index')}}">Community
            <span id="notifications" class="badge badge-info">
                {{ discourse.user_unread_notifications_count() }}
            </span>
        </a>
        {% else %}
        <a href="{{ url_for('account.index')}}">Community</a>
        {% endif %}
    </li>

See the API documentation below for full details of the methods available.


Embedding Comments
==================

To embed Discourse comments in your PyBossa theme:

1. Visit **Admin > Customize > Embedding** in your Discourse application.
2. Create an embeddable host using your PyBossa domain as the hostname, not
   including the `http://` or path (e.g. `www.example.com`).
3. Enter the name of the Discourse user who will create topics in the **Embed by Username** field.
4. Use the following snippet wherever you want comments to appear in your PyBossa theme.

.. code-block:: HTML+Django
    {% if 'pybossa_discourse' in plugins %}
        {{ discourse.comments() }}
    {% endif %}

A new Discourse topic will be created for each page on which the above snippet appears the first time
that someone visits. When people post in that topic, their comments will show up on the page where that
topic is embedded.


API
===

.. module:: pybossa_discourse

.. autoclass:: DiscourseClient
   :members:
