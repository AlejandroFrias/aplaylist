# aplayist: an album playlist for Spotify

## Setup

### Requirements

Python 3.6+

### Local dev setup

Get the repo and install the python packages
```
# Clone the repo
git clone https://github.com/AlejandroFrias/aplaylist.git
cd aplaylist

# Setup python virtual env and packages
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Setup your environment variables
```
# environment variables (add to bashrc/bash_profile if you don't want to do this everytime)
export SOCIAL_AUTH_SPOTIFY_KEY=<your-client-id>
export SOCIAL_AUTH_SPOTIFY_SECRET=<your-secret>
export DJANGO_SECRET_KEY=<any-50-character-long-string>
```

Setup the django app
```
# Setup database (that's it)
./manage.py migrate
```

Run the app at http://localhost:8000
```
./manage.py runserver
```
