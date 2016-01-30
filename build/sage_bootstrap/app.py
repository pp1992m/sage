# -*- coding: utf-8 -*-
"""
Controller for the commandline actions
"""


#*****************************************************************************
#       Copyright (C) 2016 Volker Braun <vbraun.name@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

import os
import sys
import logging
log = logging.getLogger()

from sage_bootstrap.env import SAGE_DISTFILES
from sage_bootstrap.package import Package
from sage_bootstrap.tarball import Tarball


class Application(object):

    def config(self):
        """
        Print the configuration

        $ sage --package config
        Configuration:
          * log = info
          * interactive = True
        """
        log.debug('Printing configuration')
        from sage_bootstrap.config import Configuration
        print(Configuration())

    def list(self):
        """
        Print a list of all available packages

        $ sage --package list | sort
        4ti2
        arb
        atlas
        autotools
        [...]
        zn_poly
        """
        log.debug('Listing packages')
        for pkg in Package.all():
            print(pkg.name)

    def name(self, tarball_filename):
        """
        Find the package name given a tarball filename
    
        $ sage --package name pari-2.8-1564-gdeac36e.tar.gz
        pari
        """
        log.debug('Looking up package name for %s', tarball_filename)
        tarball = Tarball(os.path.basename(tarball_filename))
        print(tarball.package.name)

    def tarball(self, package_name):
        """
        Find the tarball filename given a package name
    
        $ sage --package tarball pari
        pari-2.8-1564-gdeac36e.tar.gz
        """
        log.debug('Looking up tarball name for %s', package_name)
        package = Package(package_name)
        print(package.tarball.filename)

    def apropos(self, incorrect_name):
        """
        Find up to 5 package names that are close to the given name

        $ sage --package apropos python
        Did you mean: cython, ipython, python2, python3, patch?
        """
        log.debug('Apropos for %s', incorrect_name)
        from sage_bootstrap.levenshtein import Levenshtein, DistanceExceeded
        levenshtein = Levenshtein(5)
        names = []
        for pkg in Package.all():
            try:
                names.append([levenshtein(pkg.name, incorrect_name), pkg.name])
            except DistanceExceeded:
                pass
        if names:
            names = sorted(names)[:5]
            print('Did you mean: {0}?'.format(', '.join(name[1] for name in names)))
        else:
            print('There is no package similar to {0}'.format(incorrect_name))
            print('You can find further packages at http://files.sagemath.org/spkg/')

    def update(self, package_name, new_version, url=None):
        """
        Update a package. This modifies the Sage sources. 
    
        $ sage --package update pari 2015 --url=http://localhost/pari/tarball.tgz
        """
        log.debug('Updating %s to %s', package_name, new_version)
        from sage_bootstrap.updater import PackageUpdater
        update = PackageUpdater(package_name, new_version)
        if url is not None:
            log.debug('Downloading %s', url)
            update.download_upstream(url)
        update.fix_checksum()
