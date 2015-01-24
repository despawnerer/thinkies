thinkies
========

Microreviewing app


Requirements
------------

* python 3.4
* postgresql 9
* elasticsearch 1.3
* mongodb
* bower (through nodejs)


Setting up or upgrading
-----------------------

Make sure you're within virtualenv.

	$ pip install -r requirements.pip
	$ bower prune && bower install
	$ ./manage.py migrate
