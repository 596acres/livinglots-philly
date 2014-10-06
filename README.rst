Living Lots Philly
==================

A vacant lot viewer and organizing platform for Philadelphia, roughly based on
`596 Acres <http://596acres.org/>`_.


Installation
------------

Install `mapnik <https://github.com/mapnik/mapnik/wiki/Mapnik-Installation>`_.

Living Lots Philly uses `Django <http://djangoproject.org/>`_ and 
`GeoDjango <http://geodjango.org/>`_. The rest of the requirements are in 
`requirements.txt`::

    pip install -r requirements/base.txt
    pip install -r requirements/local.txt

Once the requirements are installed, create a PostGIS database as described in 
`settings/base.py`. Then get Django running on that database::

    django-admin.py syncdb
    django-admin.py migrate

Then fire up the server (we're using `django-extensions
<http://django-extensions.readthedocs.org/en/latest/>`_ for nice in-browser
debugging)::

    django-admin.py runserver_plus


Organization
------------

Apps specific to Philadelphia's data are grouped in the package `phillydata`.

Apps that deal with generic "places" are grouped in the package `places`.


License
-------

Living Lots Philly is released under the GNU `Affero General Public License,
version 3 <http://www.gnu.org/licenses/agpl.html>`_.
