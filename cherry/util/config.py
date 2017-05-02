import os
import sys
import ConfigParser

conf_dir = os.getenv('CHERRY_CONF_DIR')
if not conf_dir:
    if sys.platform.startswith('linux') and \
            os.path.exists('/etc/cherry/cherry.conf'):
        conf_dir = '/etc/cherry'
    else:
        raise IOError("CHERRY_CONF_DIR not defined")

cherry_conf_file = os.path.join(conf_dir, 'cherry.conf')

conf = ConfigParser.ConfigParser()
conf.read(cherry_conf_file)

sections = conf.sections()
conf_dict = {}
for section in sections:
    configs = {}
    for item in conf.items(section):
        k, v = item[0], item[1]
        configs[k] = v
    conf_dict[section] = configs
