# YelpCamp Python
YelpCamp final project from the course translated into Python using Flask.

Run the app with:
```bash
export FLASK_APP=app
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run
```
and open https://127.0.0.1:5000/

## Installation
I recommend using a virtual environment:
```bash
python3 -m virtualenv .venv
source .venv/bin/activate
```

```bash
python3 -m pip install -r requirements.txt
```

### Setup
Before running the app, configure the following APIs:
- Register to MongoDB atlas and set the following environment variables:
```bash
export MONGOURI="mongodb+srv://rw:¿?@¿?.mongodb.net/yelpCamp?retryWrites=true&w=majority"
```
- Register at cloudinary.com and set the following environment variables:
```bash
export CLOUDINARY_NAME="¿?"
export CLOUDINARY_KEY="¿?"
export CLOUDINARY_SECRET="¿?"
```
- Register at mapbox and set the following environment variables:
```bash
export MAPBOX_ACCESS_TOKEN="¿?"
```
- Set a secret for the app:
```bash
export YELP_CAMP_SECRET="¿?"
```

### Seeding
Fill the database with fake data:
```bash
python3 -m seeds.main
```

## References
- Flask: https://flask.palletsprojects.com/en/2.0.x/quickstart/
- Mongoengine: https://docs.mongoengine.org/
- Flask-Talisman: https://github.com/GoogleCloudPlatform/flask-talisman
