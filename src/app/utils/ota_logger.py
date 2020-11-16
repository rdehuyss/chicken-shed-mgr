import os, machine, binascii, utime
from .httpclient import HttpClient

class OTALogger:
    """
    A class to log from your MicroController to a GitHub Gist.
    """

    def __init__(self, gistId, access_token, headers={}):
        self.gistId = gistId
        self.access_token = access_token
        self.headers = headers

    def logToGist(self, filePath) -> bool:
        """Function which will upload the file to the specified GitHub Gist

        Returns
        -------
            bool: true if logging to Gist succeeded, false otherzie
        """

        httpClient = HttpClient(headers={'Authorization': 'token {}'.format(self.access_token)})
        self.filePath = filePath
        rootUrl = 'https://api.github.com/gists/' + self.gistId
        print(rootUrl)
        resp = httpClient.post(rootUrl, custom=self.writeToSocket)
        if resp.status_code == 200:
            return True
        else:
            return False


    def writeToSocket(self, s):
        contentLength = self.calculateContentLength()
        s.write(b'Content-Length: %d\r\n' % contentLength)
        s.write(b'\r\n')
        s.write('{"public":true,"files":{"' + utime.strftime('%Y%m%d-%H%M%S', utime.localtime()) + '.log":{"content":"')
        with open(self.filePath, 'r') as file_object:
            for line in file_object:
                lineToWrite = line.replace('"', '\"').replace('\n', '<br/>')
                s.write(lineToWrite)
        s.write('"}}}')

    def calculateContentLength(self) -> int:
        contentLength = 58 + 4
        with open(self.filePath, 'r') as file_object:
            for line in file_object:
                contentLength += len(line.replace('"', '\"').replace('\n', '<br/>'))
        return contentLength

