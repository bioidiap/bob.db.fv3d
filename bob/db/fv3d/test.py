#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""A few checks at the 3D Fingervein database.
"""

import os
import numpy

from .query import Database

import nose.tools
from nose.plugins.skip import SkipTest


def metadata_available(test):
  """Decorator for detecting if the metadata is available"""

  from bob.io.base.test_utils import datafile
  from nose.plugins.skip import SkipTest
  import functools

  @functools.wraps(test)
  def wrapper(*args, **kwargs):
    dbfile = datafile("db.sql3", __name__, None)
    if os.path.exists(dbfile):
      return test(*args, **kwargs)
    else:
      raise SkipTest("The interface SQL file (%s) is not available; did you forget to run 'bob_dbmanage.py %s create' ?" % (dbfile, 'fv3d'))

  return wrapper


def db_available(test):
  """Decorator for detecting if the database files are available"""

  from bob.io.base.test_utils import datafile
  from nose.plugins.skip import SkipTest
  import functools

  @functools.wraps(test)
  def wrapper(*args, **kwargs):
    if os.path.exists(DATABASE_PATH):
      return test(*args, **kwargs)
    else:
      raise SkipTest("The database path (%s) is not available" % (DATABASE_PATH))

  return wrapper


@metadata_available
def test_recreate():

  from bob.db.base.script.dbmanage import main
  nose.tools.eq_(main('fv3d create --recreate'.split()), None)


@metadata_available
def test_counts():

  # test whether the correct number of clients is returned
  db = Database()

  nose.tools.eq_(db.groups(), ('train', 'dev', 'eval'))

  protocols = db.protocol_names()
  nose.tools.eq_(len(protocols), 1)
  assert 'central' in protocols

  nose.tools.eq_(db.purposes(), ('train', 'enroll', 'probe'))
  nose.tools.eq_(db.genders(), ('m', 'f'))
  nose.tools.eq_(db.sides(), ('l', 'r'))
  nose.tools.eq_(db.fingers(), ('t', 'i', 'm', 'r', 'l'))

  # FDV: 89 subjects * 2 fingers * 5 snapshots * 1 attempt = 890
  # IDI: 2 subjects * 6 fingers * 2 snapshots = 48
  # Total: 938 images
  nose.tools.eq_(len(db.objects(protocol='central', groups='train')), 938)

  # IDI: 50 subjects * 6 fingers * 2 snapshots * 2 attempts = 1200 images
  nose.tools.eq_(len(db.objects(protocol='central', groups='dev',
    purposes='enroll')), 1200)

  # test model ids
  model_ids = db.model_ids()
  nose.tools.eq_(len(model_ids), 440)

  model_ids = db.model_ids(protocol='Nom')
  nose.tools.eq_(len(model_ids), 220)

  model_ids = db.model_ids(protocol='Fifty')
  nose.tools.eq_(len(model_ids), 100)

  model_ids = db.model_ids(protocol='B')
  nose.tools.eq_(len(model_ids), 216)

  model_ids = db.model_ids(protocol='Full')
  nose.tools.eq_(len(model_ids), 440)

  # test database sizes
  nose.tools.eq_(len(db.objects(protocol='Nom', groups='train')), 0)
  nose.tools.eq_(len(db.objects(protocol='Nom', groups='dev')), 440)
  nose.tools.eq_(len(db.objects(protocol='Nom', groups='dev',
    purposes='enroll')), 220)
  nose.tools.eq_(len(db.objects(protocol='Nom', groups='dev',
    purposes='probe')), 220)

  nose.tools.eq_(len(db.objects(protocol='Fifty', groups='train')), 240)
  nose.tools.eq_(len(db.objects(protocol='Fifty', groups='dev')), 200)
  nose.tools.eq_(len(db.objects(protocol='Fifty', groups='dev',
    purposes='enroll')), 100)
  nose.tools.eq_(len(db.objects(protocol='Fifty', groups='dev',
    purposes='probe')), 100)

  nose.tools.eq_(len(db.objects(protocol='B', groups='train')), 224)
  nose.tools.eq_(len(db.objects(protocol='B', groups='dev')), 216)
  nose.tools.eq_(len(db.objects(protocol='B', groups='dev',
    purposes='enroll')), 216)
  nose.tools.eq_(len(db.objects(protocol='B', groups='dev',
    purposes='probe')), 216)

  nose.tools.eq_(len(db.objects(protocol='Full', groups='train')), 0)
  nose.tools.eq_(len(db.objects(protocol='Full', groups='dev')), 440)
  nose.tools.eq_(len(db.objects(protocol='Full', groups='dev',
    purposes='enroll')), 440)
  nose.tools.eq_(len(db.objects(protocol='Full', groups='dev',
    purposes='probe')), 440)

  # make sure that we can filter by model ids
  nose.tools.eq_(len(db.objects(protocol='Full', groups='dev',
    purposes='enroll', model_ids=model_ids[:10])), 10)

  # filtering by model ids on probes, returns all
  nose.tools.eq_(len(db.objects(protocol='Full', groups='dev',
    purposes='probe', model_ids=model_ids[0])), 440)


@nose.tools.nottest
@metadata_available
def test_driver_api():

  from bob.db.base.script.dbmanage import main

  nose.tools.eq_(main('fv3d dumplist --self-test'.split()), 0)
  nose.tools.eq_(main('fv3d dumplist --protocol=Full --group=dev --purpose=enroll --model=101_L_1 --self-test'.split()), 0)
  nose.tools.eq_(main('fv3d checkfiles --self-test'.split()), 0)


@nose.tools.nottest
@metadata_available
@db_available
def test_load():

  db = Database()

  for f in db.objects():

    # loads an image from the database
    image = f.load(DATABASE_PATH)
    assert isinstance(image, numpy.ndarray)
    nose.tools.eq_(len(image.shape), 2) #it is a 2D array
    nose.tools.eq_(image.dtype, numpy.uint8)


@nose.tools.nottest
@metadata_available
def test_model_id_to_finger_name_conversion():

  db = Database()

  for f in db.objects():

    assert len(db.finger_name_from_model_id(f.model_id)) == 5
