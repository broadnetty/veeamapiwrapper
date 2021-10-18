import requests, os
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

    def getRepositories(self, name=''):
        self.getAccessToken()
        r = requests.get(self.url+'/repositories', params={'SearchPattern': name}, headers=self.headers, verify=False)
        return json.loads(str(r.text))['results']

    def getAccounts(self, name=''):
        self.getAccessToken()
        r = requests.get(self.url + '/accounts/amazon', params={'SearchPattern': name}, headers=self.headers, verify=False)
        return json.loads(str(r.text))['results']

    def getRegions(self, name=''):
        self.getAccessToken()
        r = requests.get(self.url + '/cloudInfrastructure/regions', params={'SearchPattern': name},
                         headers=self.headers, verify=False)
        return json.loads(str(r.text))['results']

    def getTags(self, name=''):
        self.getAccessToken()
        r = requests.get(self.url + '/cloudInfrastructure/tags', params={'SearchPattern': name},
                         headers=self.headers, verify=False)
        return json.loads(str(r.text))['results']

    def getBuckets(self, name =''):
        self.getAccessToken()
        r = requests.get(self.url + '/cloudInfrastructure/buckets',  params={'SearchPattern': name}, headers=self.headers, verify=False)
        return json.loads(str(r.text))['results']

    def rescanS3(self, account_id):
        self.getAccessToken()
        r = requests.post(self.url + '/cloudInfrastructure/buckets/rescan/' + account_id, headers=self.headers, verify=False)
        return json.loads(str(r.text))

    def rescanEC2(self):
        self.getAccessToken()
        r = requests.post(self.url + '/virtualMachines/rescan', headers=self.headers, verify=False)
        return json.loads(str(r.text))

    def rescanFull(self, amazonAccountId, regionIds):
        self.getAccessToken()
        data = {'rescanType': 'All', 'regionIds': regionIds}
        r = requests.post(self.url + '/accounts/amazon/' + amazonAccountId + '/rescan', json=data ,headers=self.headers, verify=False)
        return json.loads(str(r.text))

    def getS3Folders(self, bucket_id):
        self.getAccessToken()
        r = requests.get(self.url + '/cloudInfrastructure/buckets/{0}/folders'.format(bucket_id), headers=self.headers, verify=False)
        return json.loads(str(r.text))['results']

    def getBackupPolicies(self):
        self.getAccessToken()
        r = requests.get(self.url + '/policies', headers=self.headers, verify=False)
        return json.loads(str(r.text))['results']

    def getSession(self, session_id):
        self.getAccessToken()
        r = requests.get(self.url + '/sessions/' + session_id, headers=self.headers, verify=False)
        return json.loads(str(r.text))

    def addRepository(self, account_id, name, bucket_id, path, encryption = False):
        self.getAccessToken()
        data = {"amazonAccountId": account_id,
                "name": name,
                "amazonBucketId": bucket_id,
                "amazonStorageFolder": path,
                "enableEncryption": encryption}
        r = requests.post(self.url + '/repositories', json=data, headers=self.headers, verify=False)
        return json.loads(str(r.text))

    def addBackupPolicy(self, amazonAccountId, regionIds, targetRepositoryId, tagIds ):
        self.getAccessToken()
        data = {}
        with open('json-templates/aws-automation-policy-linux.json', 'r') as fp:
            data = json.loads(fp.read())

        data['amazonAccountId'] = amazonAccountId
        data['backupSettings']['regionIds'] = regionIds
        data['targetRepositoryId'] = targetRepositoryId
        data['selectedItems']['tagIds'] = tagIds
        r = requests.post(self.url + '/policies', json=data, headers=self.headers, verify=False)
        return json.loads(str(r.text))


vb = VBA('127.0.0.1','11005', os.environ['VBAlogin'], os.environ['VBApass'])

#print(vb.rescanFull(vb.getAccounts('Default*')[0]['id'], [vb.getRegions('us-east-2')[0]['id']]))
#print(vb.getTags('mtop-mo-backup'))

#print(vb.getRegions('us-east-2'))
#print(vb.rescanEC2())
#print(vb.rescanСloudAccounts(vb.getAccounts('Default*')[0]['id'], [vb.getRegions('us-east-2')[0]['id']]))
#print(vb.rescanS3(vb.getAccounts('Default*')[0]['id']))
#print(vb.addBackupPolicy(vb.getAccounts('Default*')[0]['id'], vb.getAccounts('Default*')[0]['id'], vb.getRepositories('main-repository-awx-automation')[0]['id']), )

def addrepo(vb):
    vb.rescanS3(vb.getAccounts('Default*')[0]['id'])
    print(vb.getBuckets('mtop-s3-lab'))
    for bucket in vb.getBuckets('mtop-s3-lab'):
        print(vb.addRepository(vb.getAccounts('Default*')[0]['id'], "main-repository-awx-automation", bucket['id'], 'awx-automation'))

#addrepo(vb)
