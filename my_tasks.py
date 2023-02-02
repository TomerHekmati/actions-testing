import os
import sys
from urllib.request import urlopen
import re
from invoke import task
import yaml


def version_format_refactor(version):
    # received format of x.y.z (str)
    # return format of xnymz (int)
    l = [int(x, 10) for x in version.split('.')]
    l.reverse()
    version = sum(x * (100 ** i) for i, x in enumerate(l))
    return version

def set_min_redis_pack_version(module_version, module_name):
    url_folder_map = {'json': 'RedisJSON',
                        'graph': 'RedisGraph',
                        'timeseries': 'RedisTimeSeries',
                        'bloom': 'RedisBloom',
                        'Cuckoo': 'RedisBloom',
                        'TopK': 'RedisBloom',
                        'CountMinSketch': 'RedisBloom',
                        'gears': 'RedisGears',
                        'search': 'RediSearch',
                        'searchlight': 'RediSearch',
                        'ai': 'RedisAI',
                        'ailight': 'RedisAI'}
    ramp_file = 'ramp.yml'
    if 'Light' in module_name:
        ramp_file = 'ramp-light.yml'
    pack = ''
    if 'Search' in module_name:
        pack = 'coord/pack/'
    elif 'RedisearchLight' in module_name:
        pack = 'pack/'
    version = module_version
    if version != 'master':
        version = 'v'+version
    url = f'https://raw.githubusercontent.com/{url_folder_map[module_name]}/{url_folder_map[module_name]}/{version}/{pack}{ramp_file}'
    page = urlopen(url)
    html = page.read().decode("utf-8")
    line = ''.join(re.findall("min_redis_pack_version.*$", html, re.MULTILINE))
    pack_version = line.replace('min_redis_pack_version: ', '')
    pack_version = pack_version.strip('"')
    pack_version = pack_version.strip("'")
    if len(pack_version) == 3:
        pack_version += '.0'
    return pack_version

@task(
    help={
        "module_name": "Redis module name",
        "module_version": "The module version",
        "module_url": "URL to download the module",
    }
)
def set_permutations(
    c,
    module_name = None,
    module_version = None,
    module_url = None,
):
    # print(module_name)
    # print(module_version)
    min_cluster_version = set_min_redis_pack_version(module_version, module_name)
    # print(f'Minimum cluster version the module support: {min_cluster_version}')

    with open('parameters.yaml') as file:
        documents = yaml.full_load(file)
        os_s = documents['OS']
        rs_versions = documents['RS_VERSIONS']
        os_supported_by_modules = documents['OS_SUPPORTED_BY_MODULES']

    # list of OSs:
    # print(os_s)
    # list of cluster versions:
    cluster_versions = []
    for rs_ver in rs_versions:
        if version_format_refactor(rs_ver) >= version_format_refactor(min_cluster_version):
            print(rs_ver)
            cluster_versions.append(rs_ver)
    # print(f'Final cluster versions to test: {cluster_versions}')
    # return cluster_versions
    # chosen_os_list = []
    # for os in os_s:
    #     print(os)
    #     chosen_os_list.append(os)
    # print('chosen_os_list after adding it automatically:')
    # print(self.chosen_os_list)
    # self.chosen_rs_versions = []
    # for rs_version in rs_versions:
    #     self.chosen_rs_versions.append(rs_version)
    # print('chosen_rs_versions after adding it automatically:')
    # print(self.chosen_rs_versions)
