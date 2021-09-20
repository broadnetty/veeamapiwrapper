import requests
import urllib3, json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class VBA:

    def __init__(self, VBhost, VBport, user, password, token=None):
        self.user = user
        self.creds ={"pass": password,"login": user}
        self.url = 'https://{0}:{1}/api/v1'.format(VBhost, VBport)
        self.api_version = '1.1-rev0'
        self.token = token
        self.data = {"x-api-version": self.api_version}
        pass

    def getAccessToken(self):
        if self.token == None:
            data = {"grant_type": "password", "username": self.creds['login'], "password": self.creds['pass']}
            r = requests.post(self.url+'/token', data=data, verify=False)
            self.token = json.loads(r.content)['access_token']
            self.headers = {"Authorization": "Bearer {0}".format(self.token), 'Content-type': 'application/json', 'x-api-version': self.api_version}

        pass

    def getRepositories(self):
        self.getAccessToken()
        r = requests.get(self.url+'/repositories', headers=self.headers, verify=False)
        return json.loads(str(r.text))['results']

    def getAccounts(self):
        self.getAccessToken()
        r = requests.get(self.url + '/accounts/amazon', headers=self.headers, verify=False)
        return json.loads(str(r.text))['results']

    def getBuckets(self):
        self.getAccessToken()
        r = requests.get(self.url + '/cloudInfrastructure/buckets',  headers=self.headers, verify=False)
        return json.loads(str(r.text))['results']

    def getS3Folders(self, bucket_id):
        self.getAccessToken()
        r = requests.get(self.url + '/cloudInfrastructure/buckets/{0}/folders'.format(bucket_id), headers=self.headers, verify=False)
        return json.loads(str(r.text))['results']

    def getBackupPolicies(self):
        self.getAccessToken()
        r = requests.get(self.url + '/policies', headers=self.headers, verify=False)
        return json.loads(str(r.text))['results']


    def addRepository(self, account_id, name, bucket_id, path, encryption = False):
        self.getAccessToken()
        data = {"amazonAccountId": account_id,
                "name": name,
                "amazonBucketId": bucket_id,
                "amazonStorageFolder": path,
                "enableEncryption": encryption}
        r = requests.post(self.url + '/repositories', json=data, headers=self.headers, verify=False)
        return json.loads(str(r.text))

    def addBackupPolicy(self):
        self.getAccessToken()
        data = {}
        with open('json-templates/aws-automation-policy-linux.json', 'r') as fp:
            data = json.loads(fp.read())
        r = requests.post(self.url + '/policies', json=data, headers=self.headers, verify=False)
        return json.loads(str(r.text))

vb = VBA('18.116.163.28','11005','grizzly','7ujMko0admin!')
print(vb.addBackupPolicy())

def addrepo(vb):
    for bucket in vb.getBuckets():
        if 'mtop-s3-lab' in bucket['name']:
        #for folder in vb.getS3Folders(bucket['id']):
        #    if 'awx-automation2' in folder['name']:
            vb.addRepository(vb.getAccounts()[0]['id'], "main-repository-awx-automation", bucket['id'], 'awx-automation')

