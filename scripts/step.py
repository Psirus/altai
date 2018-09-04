import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from altai.lib import driver_database
from altai.lib import vented_box
from altai.lib import speaker
import matplotlib.pyplot as plt
import numpy as np

driver_db = driver_database.DriverDB.from_file('../altai/lib/driver_db.json')
driver = driver_db[1]
box = vented_box.VentedBox(Vab=0.09, fb=40.0, Ql=20.0)
speaker = speaker.VentedSpeaker(driver, box)
t, response = speaker.step_response()

plt.plot(t, response)
plt.show()
