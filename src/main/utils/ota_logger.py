import os, machine, binascii, utime
from httpclient import HttpClient

class OTALogger:
    """
    A class to log from your MicroController to a GitHub Gist.
    """

    def __init__(self, gistId, username, access_token, headers={}):
        self.gistId = gistId
        self.username = username
        self.access_token = access_token
        self.headers = headers

    def log(self, filePath):
        authHeader = binascii.b2a_base64('{}:{}'.format(self.username, self.access_token))
        httpClient = HttpClient(headers={'Authorization': 'Basic {}'.format(authHeader)})


        httpClient.post('https://api.github.com/gists/' + self.gistId, file=filePath)
        with open(filePath + ".tmp") as tmpFile:
                tmpFile.write('{"public":true,"files":{"{}.log":{"content":"'.format())
                with open(filePath) as logFile:
                    print('todo')



