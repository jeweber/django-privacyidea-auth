from django.conf import settings
from django.contrib.auth.models import User
import logging
import requests

logger = logging.getLogger(__name__)


class PrivacyIDEA(object):
    """
    Authenticate against a privacyidea server.

    Add the following to your project/settings.py
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
    'create_user': if set to True, the user in the django DB will be created, if PrivacyIDEA returns a successful
        authentication
    'update_attributes': if set to True, the user attributes in the django DB will be updated, if privacyidea samlcheck
        returns user attributes
    'realm': if set, the realm of the user, who tries to authenticate. If the realm is None, the user is looked up in
        the default realm
    'enforce_realm': if set, login name must contains '@' too separates realm from the username
    """
    def __init__(self):
        self.url = 'https://localhost/validate/samlcheck'
        self.timeout = 5
        self.ssl_verify = False
        self.create_user = False
        self.update_attributes = True
        self.realm = None
        self.enforce_realm = False
        if settings.PRIVACYIDEA:
            self.url = settings.PRIVACYIDEA.get('url', self.url)
            self.timeout = settings.PRIVACYIDEA.get('timeout', self.timeout)
            self.ssl_verify = settings.PRIVACYIDEA.get('ssl_verify', self.ssl_verify)
            self.create_user = settings.PRIVACYIDEA.get('create_user', self.create_user)
            self.update_attributes = settings.PRIVACYIDEA.get('update_attributes', self.update_attributes)
            self.realm = settings.PRIVACYIDEA.get('realm', self.realm)
            self.enforce_realm = settings.PRIVACYIDEA.get('enforce_realm', self.enforce_realm)

    def authenticate(self, username=None, password=None):
        user = None
        # ensure that username does not contains or contains only one '@'
        if username.count('@') > 1:
            return user

        # enforce_realm is set and username is not valid
        if self.enforce_realm and username.count('@') != 1:
            return user

        # realm is set and realm provided in username is not equals realm
        if self.realm and self.enforce_realm and self.realm != username.split('@')[1]:
            return user

        # realm is set and username contains '@'
        if self.realm and '@' in username:
            # realm provided in username is not equals realm
            if self.realm != username.split('@')[1]:
                return user
            username = username.split('@')[0]

        try:
            r = requests.post(self.url, verify=self.ssl_verify, timeout=self.timeout, data={
                'user': username,
                'pass': password,
                'realm': self.realm
            })
            logger.debug("privacyidea %s get status_code %i" % (self.url, r.status_code))
            if r.status_code == requests.codes.ok:
                response = r.json()
                logger.debug("privacyidea %s get response %s" % (self.url, response))

                if (response.get('result', {}).get('status') == True and
                        (
                            response.get('result', {}).get('value') == True or
                            response.get('result', {}).get('value', {}).get('auth') == True
                        )):
                    if self.realm and self.enforce_realm:
                        username += '@' + self.realm

                    user = User.objects.filter(username=username)
                    if len(user) == 0:
                        # The user was authenticated by PrivacyIDEA but does not exist!
                        logger.debug("User authenticated but does not exist")
                        if self.create_user:
                            # Create a new user. There's no need to set a password
                            user = User(username=username)
                            user.is_staff = False
                            user.is_superuser = False
                            user.save()
                        else:
                            return None
                    else:
                        user = user[0]

                    if self.update_attributes:
                        attributes = response.get('result', {}).get('value', {}).get('attributes', {})
                        surname = attributes.get('surname', None)
                        givenname = attributes.get('givenname', None)
                        email = attributes.get('email', None)
                        user.first_name = givenname
                        user.last_name = surname
                        user.email = email
                        user.save()

        except Exception as e:
            logger.exception("An error occurred: %s" % e)

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
