# -*- coding: utf-8 -*-
"""Storing the runtime configuration of Altai."""
import os
import sys
import shutil
import PySide2.QtCore as QtCore
from ..lib import driver_database

# generate altai config dir if if does not exist;
# under Unix '~/.local/share/data/altai'
data_dir = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.ConfigLocation)
altai_config_dir = os.path.join(data_dir, 'altai')
try:
    os.makedirs(altai_config_dir)
except OSError:
    if not os.path.isdir(altai_config_dir):
        raise

# check if local driver database exists; if not copy it from altai
# source dir
local_db_fname = os.path.join(altai_config_dir, 'driver_db.json')
if not os.path.isfile(local_db_fname):
    altai_bin_dir = os.path.dirname(sys.argv[0])
    included_db_fname = os.path.join(altai_bin_dir, 'altai/lib/driver_db.json')
    shutil.copy(included_db_fname, local_db_fname)

# load driver database
driver_db = driver_database.DriverDB.from_file(local_db_fname)
