import requests
import urllib3, json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class VBA:

    def __init__(self, VBhost, VBport, user, password, token=None):
        self.user = user
        self.creds ={"pass": password,"login": user}
        self.url = 'https://{0}:{1}/'.format(VBhost, VBport)
        self.api_version = '1.1-rev0'
        self.token = token
        pass

    def getAccessToken(self):
        if self.token == None:
            data = {"grant_type": "password", "username": self.creds['login'], "password": self.creds['pass']}
            r = requests.post(self.url+'api/v1/token', data=data, verify=False)
            self.headers = {"Authorization": "Bearer {0}".format(json.loads(r.content)['access_token'])}
        pass

    def getRepositories(self):
        if self.token == None:
            self.getAccessToken()
        data = {"x-api-version": self.api_version}
        r = requests.get(self.url+'api/v1/repositories', data=data, headers=self.headers, verify=False)
        print(r.content)
        pass

vb = VBA('18.116.163.28','11005','grizzly','7ujMko0admin!')

vb.getRepositories()

