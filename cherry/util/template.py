# -*- coding: utf-8 -*-
'''
filters module
author: zhangxusheng
date:2015/11/12
email:huodahaha@gmail.com
'''
from __future__ import absolute_import

import os
import sys
import jinja2

from cherry.tasks.operators import Singleton
from cherry.util.config import conf_dict


class Template(Singleton):
    """ generate a template bat
    """

    def __init__(self):
        super(Template, self).__init__()

        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(
            conf_dict['all']['template_path']))
        self.script_file_prefix = "execute_"

    def generate_bat(self, template_file, params):
        """render template, generate bat file

        template_file: input template file, expected to be in template dir
        params: key/value dict for rendering
        """
        print("generating bat ...")
        print("template: %s" % template_file)
        print("params: %s" % params)

        params.update(conf_dict['tools'])
        rendered_str = self.env.get_template(template_file).render(params)

        # for windows: replace \n with \r\n
        if not sys.platform.startswith('linux'):
            rendered_str = "\r\n".join(rendered_str.split('\n'))

        script_file = self.script_file_prefix + template_file
        print("rendered script file: %s" % (script_file))
        with open(script_file, 'w') as f:
            f.writelines(rendered_str)

        if sys.platform.startswith('linux'):
            os.chmod(script_file, 0777)  # add executing privileage

        return script_file
