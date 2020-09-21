import os
import requests

try:
    if os.uname()[0] == 'Linux':
        from pip import get_installed_distributions
except AttributeError:
    from pip._internal.utils.misc import get_installed_distributions

import subprocess


def get_installed_packages(original: str = None):
    installed_packages = get_installed_distributions()
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
    if original is None:
        installed_packages_list = format_list(installed_packages_list)
    return installed_packages_list


def format_list(my_list: list):
    for i in range(0, len(my_list)):
        my_list[i] = my_list[i][:my_list[i].index('==')] + ' ' + my_list[i][my_list[i].index('==') + 2:]
    return my_list


def remove(string: str, s):
    string = string.replace(s, '')
    return string


def read_log_file(s: subprocess.Popen, is_uninstall=False):
    logfile = open('log.txt', 'w')
    result = ''
    while s.poll() is None:
        if is_uninstall:
            res = s.communicate(b'y')[0]
            # result = result + str(res, 'utf-8')
        else:
            result = result + str(s.stdout.read(), 'utf-8')
    logfile.write(result)
    return result.split('\n')


def percentage_calculator(x, y, case=1):
    if case == 1:
        # Case1: What is x% of y?
        r = x / 100 * y
        return r
    elif case == 2:
        # Case2: x is what percent of y?
        r = x / y * 100
        return r
    elif case == 3:
        # Case3: What is the percentage increase/decrease from x to y?
        r = (y - x) / x * 100
        return r
    else:
        raise Exception("Only case 1,2 and 3 are available!")


def read_requirements(dir_name: str):
    package_list = []
    with open(dir_name, 'r') as requirements:
        for package in requirements:
            package_list.append(package)
    package_list = format_list(package_list)
    return package_list


def check_installed(package: str):
    is_installed = False
    installed_packages = get_installed_packages()
    if installed_packages.count(package) == 0:
        is_installed = True
    return is_installed


def remove_packages(list1, list2):
    for package in list1:
        list2.remove(package)
    return list2


def get_package_information(package_name: str):
    response = requests.get(f'https://pypi.python.org/pypi/{package_name}/json')
    if response.status_code == 200:
        data = {'name': response.json()['info']['name'], 'version': response.json()['info']['version'],
                'description': response.json()['info']['summary']}
        return data
    else:
        print('package not found')


