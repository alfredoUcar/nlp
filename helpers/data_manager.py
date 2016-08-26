"""Data packages manager of NLTK.

This data manager main aim is to provide a simple interface to make
the project work just with required data packages from
nltk repository.

A secondary purpose is storage control. All data is saved inside
the project structure to make it entirely context independent so it
could be freely moved.
"""

import sys
import argparse
import nltk
from nltk.downloader import Downloader
from config import NltkDataConfig

_data_config = NltkDataConfig()
_data_path = _data_config.get_root_path()
_downloader = Downloader(download_dir=_data_path)
_status_classified_packages = None #cache

def download_pending_packages(use_cache=True):
    pending_packages = get_pending_packages(use_cache)
    total_downloads = len(pending_packages)
    successfull_downloads = download(pending_packages)
    return (total_downloads - successfull_downloads)

def download(packages=[]):
    successfull_downloads = 0
    for package in packages:
        if _downloader.download(info_or_id=package, quiet=True):
            successfull_downloads += 1
    return successfull_downloads

def get_pending_packages(use_cache=True):
    return get_data_packages_by_status(use_cache)['pending']

def require_updates():
    return (len(get_pending_packages()) > 0)

def get_installed_packages(use_cache=True):
    return get_data_packages_by_status(use_cache)['installed']

def get_data_packages_by_status(use_cache=True):
    """ Get all packages classified by status.

    -installed: installed and ready to use.

    -pending: not ready to use. It could correspond either to
    'not installed' or 'stale' status of nltk downloader.

    Parameters
    ----------
    use_cache: bool
        Flag that indicates whether to use or not the cache for
        packages. When cache is not used it is updated too.
    """
    global _status_classified_packages
    if use_cache and _status_classified_packages is not None:
        return _status_classified_packages

    required_packages = _data_config.get_all_packages()
    installed = []
    pending = []

    for package in required_packages:
        if is_package_installed(package):
            installed.append(package)
        else:
            pending.append(package)

    _status_classified_packages = {
        'installed': installed,
        'pending': pending
        }
    return _status_classified_packages

def is_package_installed(package_name):
    global _status_classified_packages
    if _status_classified_packages is not None:
        installed_packages = _status_classified_packages['installed']
        return package_name in installed_packages
    else:
        return _downloader.is_installed(package_name)

def _show_state():
    pending_packages = get_pending_packages(use_cache=False)
    pending_count = len(pending_packages)
    if pending_count == 0:
        print "All packages ready."
    elif pending_count == 1:
        print "There is a missing or outdated package."
    elif pending_count > 1:
        print "The are (" + `pending_count` + ") missing or outdated packages."

def _show_installed():
    installed_packages = get_installed_packages(use_cache=False)
    installed_count = len(installed_packages)
    if installed_count == 0:
        print "Any package installed."
    elif installed_count > 0:
        print "Installed packages: " + ",".join(installed_packages)

def _show_required():
    packages = _data_config.get_all_packages()
    print "Required packages: " + ", ".join(packages)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-s", "--state", action='store_true',
                        help="Show current state of data packages")
    parser.add_argument("-i", "--installed", action='store_true',
                        help="Show current installed packages")
    parser.add_argument("-r", "--required", action='store_true',
                        help="Show project required packages")
    parser.add_argument("-u", "--update", action='store_true',
                        help="Update data packages")

    if not len(sys.argv) > 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        if args.state:
            _show_state()

        if args.installed:
            _show_installed()

        if args.required:
            _show_required()

        if args.update:
            errors = download_pending_packages()
            if errors > 0:
                print "There was errors during downloading"
            _show_state()
