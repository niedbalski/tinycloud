#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jorge Niedbalski R. <jnr@pyrosome.org>'


from jinja2 import Environment, PackageLoader

loader = Environment(PackageLoader('tinycloud', 'templates'))


def load(name):
    """
    Load a template from the tinycloud.templates package
    :param name: template name
    :type name: string
    """
    return loader.get_template(name)
