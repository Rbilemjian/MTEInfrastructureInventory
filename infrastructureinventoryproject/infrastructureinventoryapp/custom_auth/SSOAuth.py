from django.contrib.auth.models import User
import xml.etree.ElementTree as ET
import requests


class SSOAuth(object):
    """
    Authenticate against the guardhouse SSO and password
    Create a Django User object the first time a user authenticates,
    else retrieve user from database and return that User object
    """

    def authenticate(self, username=None, password=None):
        response = requests.post('https://guardhouse-prd.mts.inbcu.com/ldapauth',
                                 params={'username': username, 'password': password, 'domain': 'tfayd'})

        # response code of 200 means successful authentication
        # check if user SSO is in user datatable
        if response.status_code == 200 and User.objects.get(username=username):
            user = User.objects.get(username=username)
            # if the user has never logged in before, get more info
            if not user.first_name and not user.last_name:
                # returns tuple of user first name, last name, and sso
                user_info = parseXML(response.text)

                # set the new user's attributes
                user.is_staff = False
                user.is_superuser = False
                user.first_name = user_info[0]
                user.last_name = user_info[1]
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


# parse xml to get info from <user> tag
def parseXML(xmlResponse):
    # create an element tree object
    root = ET.fromstring(xmlResponse)

    # children are nested; access specific child nodes by index
    first_name = root[0].text
    last_name = root[1].text
    sso = root[2].text

    return (first_name, last_name, sso)



