import machine, os, utime
from .httpclient import HttpClient

class OTALogger:
    """
    A class to log from your MicroController to a GitHub Gist.
    """

    def __init__(self, gist_id, access_token, headers={}):
        self.gist_id = gist_id
        self.access_token = access_token
        self.headers = headers
        self.http_client = HttpClient(headers={'Authorization': 'token {}'.format(self.access_token)})

    def __del__(self):
        self.http_client = None

    def log_to_gist(self, file_path) -> bool:
        """Function which will upload the file to the specified GitHub Gist

        Returns
        -------
            bool: true if logging to Gist succeeded, false otherwise
        """
        self.file_path = file_path
        rootUrl = 'https://api.github.com/gists/' + self.gist_id
        resp = self.http_client.post(rootUrl, custom=self._write_to_socket)
        if resp.status_code == 200:
            return True
        else:
            return False

    def _write_to_socket(self, s):
        contentLength = self.calculate_content_length()
        s.write(b'Content-Length: %d\r\n' % contentLength)
        s.write(b'\r\n')
        s.write('{"public":true,"files":{"' + utime.strftime('%Y%m%d-%H%M%S', utime.localtime()) + '.log":{"content":"')
        with open(self.file_path, 'rb') as file_object:
            for line in file_object:
                s.write(line.replace(b'"', b'\"').replace(b'\n', b'<br/>'))
        s.write('"}}}')

    def calculate_content_length(self) -> int:
        contentLength = 58 + 4
        with open(self.file_path, 'rb') as file_object:
            for line in file_object:
                contentLength += len(line.replace(b'"', b'\"').replace(b'\n', b'<br/>'))
        return contentLength

