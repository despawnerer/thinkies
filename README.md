thoughts
========

Thing-reviewing site.


Requirements
------------

* python 3.4
* bower
* virtualenv


Setting up or upgrading
-----------------------

Make sure you're within virtualenv.

	$ pip install -r requirements.pip
	$ bower prune && bower install
	$ ./manage.py migrate
