# url_shortener

How to start:
* clone this repo;
* Go to the repo folder `url_shortener`;
* Create a virtual environment `python -m venv url_shortener`  (instead of `python` you might need `python3`);
* Activate it `source url_shortener/bin/activate`
* Install the requirements `pip install -r requirements.txt`;
* Set PYTHONPATH with current directory to `export PYTHONPATH=current_folder/app`
* In current folder file with environment variables can be created. As an example the one in a repo can be used.
* You can start an app with `python run.py`
* Form for creation a short url is accessle at `http://127.0.0.1:5000/` if default env settings are used.
* To use it, you'll need to send a post request to `http://localhost:5000/shorten` with url and (optional) shortcode you want to use in form-data.

* You also can run tests with command `pytest` from the same folder (application should be stopped)

Next steps:
* Security: even obvious sending lots of requests won't end well for this application. It would be nice (at least) to limit amount of requests form one address, or make a authorization or something like that;
* Proper deployment. First step would be Docker containers with application and database (if we get rid of sqlite);
* Proper delpoyment-2. Now it runs in Flask debug mode which is not acceptable for production. We will have to use WSGI server.
* Proper database. Now it's sqlite, which is not the smartest choice. Since it's a key-value storage, Redis would work fine.
Also, Redis would be nice if we wanted to delete shortcodes after some time (like 24h) because Redis can do it easily;
* Conflicts resolve: there are not so much of these shortcodes and if we do it a lot of times, we probably will have a conflict in database; Now in this case we'll have a unhandled error, but it would be nice to resolve it smarter;
* Security-2: since we're putting in our database user input, we have to handle malicious inputs, like js-injections, sql-injections etc. 
