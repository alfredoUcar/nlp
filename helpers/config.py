import ConfigParser
import os

class ConfigException(Exception):
    pass

class NltkDataConfig(ConfigParser.ConfigParser, object):
    #sections
    DATA_PACKAGES = 'DataPackages'
    DIRECTORY_NAMES = 'DirectoryNames'

    def __init__(self):
        super(NltkDataConfig, self).__init__()
        try:
            with open('nltk_data.ini') as config_file:
                self.readfp(config_file)
        except:
            raise ConfigException('Cannot open config')

    def get_all_packages(self):
        classified_packages = dict(self.items(self.DATA_PACKAGES))
        packages = []
        for package_type in self._get_package_types():
            packages += self._get_packages_by_type(package_type)
        return packages

    def _get_package_types(self):
        classified_packages = dict(self.items(self.DATA_PACKAGES))
        return classified_packages.keys()

    def _get_packages_by_type(self, package_type):
        return eval(self.get(self.DATA_PACKAGES, package_type))

    def get_corpora(self):
        """Get corpora packages"""
        return self._get_packages_by_type('corpora')

    def get_grammars(self):
        """Get grammars packages"""
        return self._get_packages_by_type('grammars')

    def get_tokenizers(self):
        """Get tokenizers packages"""
        return self._get_packages_by_type('tokenizers')

    def get_taggers(self):
        """Get taggers packages"""
        return self._get_packages_by_type('taggers')

    def _get_root_directory(self):
        return self._get_directory('root')

    def _get_directory(self, directory):
        return self.get(self.DIRECTORY_NAMES, directory)

    def get_directories(self):
        return dict(self.items(self.DIRECTORY_NAMES))

    def get_root_path(self):
        """Get path to data packages storing directory"""
        nltk_data_dir = self._get_root_directory()
        helpers_path = os.path.dirname(os.path.abspath(__file__))
        project_path = os.path.dirname(helpers_path)
        return os.path.join(project_path, nltk_data_dir)
