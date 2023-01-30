import os
import sys
from urllib.request import urlopen
import re
from invoke import task


def set_min_redis_pack_version(module_version, module_name):
    url_folder_map = {'ReJSON': 'RedisJSON',
                        'RedisGraph': 'RedisGraph',
                        'RedisTS': 'RedisTimeSeries',
                        'ReBloom': 'RedisBloom',
                        'Cuckoo': 'RedisBloom',
                        'TopK': 'RedisBloom',
                        'CountMinSketch': 'RedisBloom',
                        'RedisGears': 'RedisGears',
                        'RediSearchEnterprise': 'RediSearch',
                        'RedisearchLight': 'RediSearch',
                        'RedisAI': 'RedisAI',
                        'RedisAILight': 'RedisAI'}
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
        "module_options": "The .env parameters, should be include something like: REDISEARCH_VERSION = '2.4.16' ",
        "pytest_options": "The markers to choose the module we are testing",
    }
)
def set_permutations(
    c,
    module_options = None,
    pytest_options = None,
):
    print(module_options)
    print(pytest_options)
    # mini_cluster_version = set_min_redis_pack_version()

