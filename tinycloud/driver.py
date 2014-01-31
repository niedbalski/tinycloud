#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jorge Niedbalski R. <jnr@pyrosome.org>'

import libvirt
import logging

from tinycloud.template import load as load_template
from tinycloud.instance import Instance, InstanceNotFound

logger = logging.getLogger(__name__)


class Driver(object):
    """
    Class for manage the creation, list, update and removal of virtual machines
    """
    def __init__(self, uri="qemu:///system", *args, **kwargs):
        self.conn = libvirt.open(uri)

    def __fini__(self):
        self.close()

    @property
    def memory(self):
        return self.conn.getFreeMemory()

    @property
    def vcpus(self):
        return self.conn.getVCPUs()

    @property
    def count(self):
        return len(self)

    def __len__(self):
        return self.conn.numOfDefinedDomains() + self.conn.numOfDomains()

    def __delitem__(self, item):
        self[item].delete()

    def __iter__(self):
        domains = self.conn.listDomainsID()
        for domain in domains:
            yield self[domain]

    def __getitem__(self, item):
        try:
            if isinstance(item, int):
                domain = self.conn.lookupByID(item)
            else:
                domain = self.conn.lookupByName(item)
        except libvirt.libvirtError, e:
            if e.get_error_code() == libvirt.VIR_ERR_NO_DOMAIN:
                raise InstanceNotFound(item)
            else:
                raise
        return Instance(domain)

    def close(self):
        self.conn.close()

    def _hydrate_disk(self, disks):
        if not isinstance(disks, list):
            disks = [disks]

        r = []
        for disk in disk:
            r.append(Disk(**disk))
        return r

    def create(self, *args, **params):
        disks = self._hydrate_disk(params.get('disks'))
        nets = self._hydrate_net(params.get('nets'))

        template = load_template(template, {
            'disks': disks,
            'nets': self._generate_nets(nets),
            'memory':  memory,
            'cpus': cpus,
            'max_memory': max_memory,
            'hypervisor': hypervisor,
            'arch': arch
        })

        try:
            self.conn.createXML(template, 0)
        except Exception as ex:
            print ex

        return self[name]
