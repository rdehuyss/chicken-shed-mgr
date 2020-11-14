# 1000 x dank aan Evelien die mijn in deze tijden gesteund heeft
# ohja, en ook een dikke merci aan tante suker (Jana Dej.) die super voor onze Otis zorgt!

import machine, os
from .httpclient import HttpClient

class OTAUpdater:
    """
    A class to update your MicroController with the latest version from a GitHub tagged release,
    optimized for low power usage.
    """

    def __init__(self, github_repo, github_src_dir='', module='', main_dir='main', new_version_dir='next', headers={}):
        self.http_client = HttpClient(headers=headers)
        self.github_repo = github_repo.rstrip('/').replace('https://github.com', 'https://api.github.com/repos')
        self.github_src_dir = '' if len(github_src_dir) < 1 else github_src_dir.rstrip('/') + '/'
        self.module = module.rstrip('/')
        self.main_dir = main_dir
        self.new_version_dir = new_version_dir

    def check_for_update_to_install_during_next_reboot(self) -> bool:
        """Function which will check the GitHub repo if there is a newer version available.
        
        This method expects an active internet connection and will compare the current 
        version with the latest version available on GitHub.
        If a newer version is available, the file 'next/.version' will be created 
        and you need to call machine.reset(). A reset is needed as the installation process 
        takes up a lot of memory (mostly due to the http stack)

        Returns
        -------
            bool: true if a new version is available, false otherwise
        """

        (current_version, latest_version) = self._check_for_new_version()
        if latest_version > current_version:
            print('New version available, will download and install on next reboot')
            self._create_new_version_file(latest_version)
            return True

        return False

    def download_and_install_update_if_available(self, ssid, password):
        """This method will install the latest version if out-of-date after boot.
        
        This method, which should be called first thing after booting, will check if the 
        next/.version' file exists. 

        - If yes, it initializes the WIFI connection, downloads the latest version and installs it
        - If no, the WIFI connection is not initialized as no new known version is available
        """

        if self.new_version_dir in os.listdir(self.module):
            if '.version' in os.listdir(self.modulepath(self.new_version_dir)):
                latest_version = self.get_version(self.modulepath(self.new_version_dir), '.version')
                print('New update found: ', latest_version)
                OTAUpdater._using_network(ssid, password)
                self.download_update_if_available()
        else:
            print('No new updates found...')

    def download_update_if_available(self):
        """This method will immediately install the latest version if out-of-date.
        
        This method expects an active internet connection and allows you to decide yourself
        if you want to install the latest version. It is necessary to run it directly after boot 
        (for memory reasons) and will restart the microcontroller if a new version is found.
        """

        (current_version, latest_version) = self._check_for_new_version()
        if latest_version > current_version:
            print('Updating to version {}...'.format(latest_version))
            self._create_new_version_file(latest_version)
            self._download_all_files(latest_version)
            self._rmtree(self.modulepath(self.main_dir))
            os.rename(self.modulepath(self.new_version_dir), self.modulepath(self.main_dir))
            print('Update installed (', latest_version, '), will reboot now')
            machine.reset()

    @staticmethod
    def _using_network(ssid, password):
        import network
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('connecting to network...')
            sta_if.active(True)
            sta_if.connect(ssid, password)
            while not sta_if.isconnected():
                pass
        print('network config:', sta_if.ifconfig())

    def _rmtree(self, directory):
        for entry in os.ilistdir(directory):
            is_dir = entry[1] == 0x4000
            if is_dir:
                self._rmtree(directory + '/' + entry[0])

            else:
                os.remove(directory + '/' + entry[0])
        os.rmdir(directory)

    def _check_for_new_version(self):
        current_version = self.get_version(self.modulepath(self.main_dir))
        latest_version = self.get_latest_version()

        print('Checking version... ')
        print('\tCurrent version: ', current_version)
        print('\tLatest version: ', latest_version)
        return (current_version, latest_version)

    def _create_new_version_file(self, latest_version):
        os.mkdir(self.modulepath(self.new_version_dir))
        with open(self.modulepath(self.new_version_dir + '/.version'), 'w') as versionfile:
            versionfile.write(latest_version)
            versionfile.close()

    def get_version(self, directory, version_file_name='.version'):
        if version_file_name in os.listdir(directory):
            with open(directory + '/' + version_file_name) as f:
                version = f.read()
                return version
        return '0.0'

    def get_latest_version(self):
        latest_release = self.http_client.get(self.github_repo + '/releases/latest')
        version = latest_release.json()['tag_name']
        latest_release.close()
        return version

    def _download_all_files(self, version, sub_dir = ''):
        root_url = self.github_repo + '/contents/' + self.github_src_dir + self.main_dir + sub_dir
        print('RootUrl', root_url)
        file_list = self.http_client.get(root_url + '?ref=refs/tags/' + version)
        print('FileList', file_list)
        for file in file_list.json():
            print(file)
            if file['type'] == 'file':
                download_url = file['download_url']
                download_path = self.modulepath(self.new_version_dir + '/' + file['path'].replace(self.main_dir + '/', ''))
                print('Download path', download_path)
                self._download_file(download_url.replace('refs/tags/', ''), download_path)
            elif file['type'] == 'dir':
                path = self.modulepath(self.new_version_dir + '/' + file['path'].replace(self.main_dir + '/', ''))
                os.mkdir(path)
                self._download_all_files(version, sub_dir + '/' + file['name'])

        file_list.close()

    def _download_file(self, url, path):
        print('\tDownloading: ', path)
        self.http_client.get(url, toFile=path)

    def modulepath(self, path):
        return self.module + '/' + path if self.module else path

    