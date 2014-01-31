#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Jorge Niedbalski R. <jnr@pyrosome.org>'

from xml.etree import ElementTree

import logging


logger = logging.getLogger(__name__)


class InstanceNotFound(Exception):
    pass


VIR_DOMAIN_NOSTATE = 0
VIR_DOMAIN_RUNNING = 1
VIR_DOMAIN_BLOCKED = 2
VIR_DOMAIN_PAUSED = 3
VIR_DOMAIN_SHUTDOWN = 4
VIR_DOMAIN_SHUTOFF = 5
VIR_DOMAIN_CRASHED = 6
VIR_DOMAIN_PMSUSPENDED = 7


class Instance(object):
    """
    Class for represents a libvirt domain
    """

    POWER_STATE = {
        VIR_DOMAIN_NOSTATE: "pending",
        VIR_DOMAIN_RUNNING: "running",
        VIR_DOMAIN_BLOCKED: "running",
        VIR_DOMAIN_PAUSED: "paused",
        VIR_DOMAIN_SHUTDOWN: "shutdown",
        VIR_DOMAIN_SHUTOFF: "shutdown",
        VIR_DOMAIN_CRASHED: "crashed",
        VIR_DOMAIN_PMSUSPENDED: "suspended",
    }

    def __init__(self, domain):
        self.domain = domain
        self.xml = ElementTree.fromstring(self.domain.XMLDesc(0))

    def _get_xml_attr(self, attr):
        return self.xml.find(attr).text

    def _get_domain_attr(self, key):
        return self.xml.attrib[key]

    def __repr__(self):
        return "Instance <name:{0}, state:{1}>".format(self.name, self.state)

    def _state_name(self, code):
        return self.POWER_STATE[code]

    @property
    def hypervisor(self):
        return self._get_domain_attr('type')

    @property
    def name(self):
        return self.domain.name()

    @property
    def cpus(self):
        return self._get_xml_attr('vcpu')

    @property
    def memory(self):
        return self._get_xml_attr('currentMemory')

    @property
    def active(self):
        return self.state in (VIR_DOMAIN_RUNNING,
                              VIR_DOMAIN_SHUTDOWN,
                              VIR_DOMAIN_PAUSED,
                              VIR_DOMAIN_BLOCKED)

    @property
    def max_memory(self):
        return self._get_xml_attr('memory')

    @property
    def state(self):
        return self._state_name(self.domain.info()[0])

    def start(self):
        self.domain.create()

    def shutdown(self):
        self.domain.shutdown()

    def suspend(self):
        self.domain.resume()

    def destroy(self):
        self.domain.destroy()

    def is_running(self):
        return self.state == 'running'

    def to_dict(self):
        return {
            'hypervisor': self.hypervisor,
            'max_memory': self.max_memory,
            'memory': self.memory,
            'cpus': self.cpus,
            'state': self.state,
            'name': self.name
        }
