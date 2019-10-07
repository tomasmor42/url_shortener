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
