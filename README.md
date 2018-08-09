# Django AAD Auth Example

This is an example built from scratch to use django and adal to authenticate into Graph API

## How to run this sample

Clone the repository

``` bash
git clone https://github.com/jwendl/django-aad-graph-example.git
```

Edit config.py to have the right values

``` python
RESOURCE = "https://graph.microsoft.com"  # Add the resource you want the access token for
TENANT = ""  # Enter tenant name, e.g. contoso.onmicrosoft.com
AUTHORITY_HOST_URL = "https://login.microsoftonline.com"
CLIENT_ID = ""  # copy the Application ID of your app from your Azure portal
CLIENT_SECRET = ""  # copy the value of key you generated when setting up the application

# These settings are for the Microsoft Graph API Call
API_VERSION = 'v1.0'
```

Change into the aadsite app

``` bash
cd aadsite
```

Fetch requirements

``` bash
sudo pip install -r requirements.txt
```

> Would love to figure out how to do this automatically

Run the application

``` bash
python3 manage.py runserver
```

Then navigate to http://localhost:8000/main/auth

## Steps to use docker

Run the command above to clone from git

Run the following commands

``` bash
docker build -t graph/aad-example:v1
docker run -p 8000:8000 graph/aad-example:v1
```