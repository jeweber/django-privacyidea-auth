=========================================
Django privacyIDEA authentication backend
=========================================

Authenticate against a privacyIDEA server. (https://www.privacyidea.org/)

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
        }

'url': url of privacyIDEA server to validate the user

'timeout': validation timeout in seconds

'ssl_verify': certificate verification, set to True is strongly advised

'create_user': if set to True, the user in the django DB will be created, if PrivacyIDEA returns a successful
    authentication

'update_attributes': if set to True, the user attributes in the django DB will be updated, if privacyidea samlcheck
    returns user attributes

'realm': if set, the realm of the user, who tries to authenticate. If the realm is None, the user is looked up in
    the default realm.