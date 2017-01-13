.. vim: set fileencoding=utf-8 :
.. Fri 02 Dec 2016 11:41:17 CET

.. image:: http://img.shields.io/badge/docs-stable-yellow.png
   :target: http://pythonhosted.org/bob.db.fv3d/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: https://www.idiap.ch/software/bob/docs/latest/bob/bob.db.fv3d/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.db.fv3d/badges/master/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.fv3d/commits/master
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.fv3d
.. image:: http://img.shields.io/pypi/v/bob.db.fv3d.png
   :target: https://pypi.python.org/pypi/bob.db.fv3d
.. image:: http://img.shields.io/pypi/dm/bob.db.fv3d.png
   :target: https://pypi.python.org/pypi/bob.db.fv3d


==========================================
 3D Fingervein Database Interface for Bob
==========================================

This package is part of the signal-processing and machine learning toolbox
Bob_. It contains an interface for the evaluation protocols of the `3D
Fingervein Database`_. Notice this package does not contain the raw data files
from this dataset, which need to be obtained through the link above.


Installation
------------

Follow our `installation`_ instructions. Then, using the Python interpreter
provided by the distribution, bootstrap and buildout this package::

  $ python bootstrap-buildout.py
  $ ./bin/buildout


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://gitlab.idiap.ch/bob/bob/wikis/Installation
.. _mailing list: https://groups.google.com/forum/?fromgroups#!forum/bob-devel
.. _3d fingervein database: https://www.idiap.ch/dataset/3d-fingervein
