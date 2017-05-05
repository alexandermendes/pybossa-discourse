pybossa-discourse
*****************

A PyBossa plugin for Discourse integration.

**Features:**
  - Use SSO to sign your PyBossa users into Discourse
  - Make Discourse API requests from your PyBossa theme
  - Add users' unread Discourse notification counts to your PyBossa theme
  - Embed Discourse comments into your PyBossa theme


Installation
============

Copy the **pybossa_discourse** folder into your PyBossa plugins directory, configure
the plugin as below and restart the server.


Configuration
=============

The following settings should be added to your PyBossa configuration file:

=================================== ==============================================================
`DISCOURSE_SECRET`                  Secret string of your choice (at least 10 characters).

`DISCOURSE_API_USERNAME`            Username of an administrator of your Discourse application.

`DISCOURSE_API_KEY`                 The API key generated for the same Discourse administrator.

`DISCOURSE_URL`                     The base URL of your Discourse application.
=================================== ==============================================================

In order to enable SSO you should also ensure that your Discourse application is configured  as follows
(via **Admin > Settings**):

=================================== ==============================================================
`enable_sso`                        Enabled

`sso_url`                           ``http://{your-pybossa-domain}/discourse/oauth-authorized``

`sso_secret`                        The value chosen for `DISCOURSE_SECRET`.

`sso_overides_email`                Enabled

`sso_overides_username`             Enabled

`sso_overrides_name`                Enabled

`sso_overrides_avatar`              Enabled

`allow_uploaded_avatars`            Disabled

`logout_redirect`                   ``http://{your-pybossa-domain}/discourse/signout``
=================================== ==============================================================

In order for the API client to work you should also make sure that the IP address of your server
is added to the Discourse whitelist (via **Admin > Logs > Screened IPs**).


Theme Integration
=================

To achieve better integration with your PyBossa theme you can add navigation
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


Notification counts
===================

You can add a user's unread Discourse notification count to your PyBossa theme
with the following snippet:

.. code-block:: HTML+Django

    {% if 'pybossa_discourse' in plugins %}
        {{ discourse.notifications() }}
    {% endif %}


Embedding Comments
==================

To embed Discourse comments in your PyBossa theme:

1. Visit **Admin > Customize > Embedding** in your Discourse application.
2. Create an embeddable host using your PyBossa domain as the hostname.
3. Enter the name of the Discourse user who will create the topics in the **Embed by Username** field.
4. Use the following snippet wherever you want comments to appear in your PyBossa theme:

.. code-block:: HTML+Django

    {% if 'pybossa_discourse' in plugins %}
        {{ discourse.comments() }}
    {% endif %}

The above function takes a single optional parameter that specifies the URL of the page that will be
crawled to create a topic. By default this is set to the URL of the page where the snippet is embedded.


You can also create a new topic by category ID and embed these comments on multiple pages using this snippet:

.. code-block:: HTML+Django

    {% if 'pybossa_discourse' in plugins %}
        {{ discourse.category_comments(1) }}
    {% endif %}

The pages that will be crawled to create these topics are those at::

    http://{pybossa-site-url}/project/category/{category-short-name}


API variable
============

You can make API calls directly from your PyBossa theme via the **discourse.api**
variable, for example:

.. code-block:: HTML+Django

    <!-- List the latest topics -->
    {% if 'pybossa_discourse' in plugins %}
    <ul>
        {% for topic in discourse.api.latest_topics() %}
        <li>{{ topic['title'] }}</li>
        {% endfor %}
    </ul>
    {% endif %}

The variable points to an instance of **pybossa_discourse.client.DiscourseClient**.

.. module:: pybossa_discourse.client

.. autoclass:: DiscourseClient
   :members:
