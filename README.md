Django privacyIDEA authentication backend
=========================================

Authenticate against a privacyIDEA server. (https://www.privacyidea.org/)

Install
-------

    virtualenv --python=python3.5 Django_python3.5
    source Django_python3.5/bin/activate
    pip install django-privacyidea-auth

Or from github

    virtualenv --python=python3.5 Django_python3.5
    source Django_python3.5/bin/activate
    git clone https://github.com/jeweber/django-privacyidea-auth.git
    pip install django-privacyidea-auth/


Quick start
-----------

Add the following to your project/settings.py:

    AUTHENTICATION_BACKENDS =  ('django.contrib.auth.backends.ModelBackend',
                                'django_privacyidea_auth.privacyidea_auth.PrivacyIDEA', )
    PRIVACYIDEA = {
        'url' : 'https://privacyidea/validate/samlcheck',
        'timeout' : 5,
        'ssl_verify' : False,
        'create_user' : False,
        'update_attributes': True,
        'realm': None,
        'enforce_realm': False,
        }

'url': url of privacyIDEA server to validate the user

'timeout': validation timeout in seconds

'ssl_verify': certificate verification, set to True is strongly advised

'create_user': if set to True, the user in the django DB will be created, if PrivacyIDEA returns a successful authentication

'update_attributes': if set to True, the user attributes in the django DB will be updated, if privacyidea samlcheck returns user attributes

'realm': if set, the realm of the user, who tries to authenticate. If the realm is None, the user is looked up in the default realm

'enforce_realm': if set, login name must contains '@' too separates realm from the username