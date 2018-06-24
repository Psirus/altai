import driver_database
import vented_box
from speaker import VentedSpeaker
import matplotlib.pyplot as plt
import numpy as np

driver_db = driver_database.DriverDB.from_file('driver_db.json')
driver = driver_db[0]
box = vented_box.VentedBox(Vab=90.0, fb=40.0, Ql=20.0)
speaker = VentedSpeaker(driver, box)
freqs, _, displacement = speaker.frequency_response()


plt.semilogx(freqs, np.abs(np.real(displacement)))
plt.semilogx(freqs, np.abs(np.imag(displacement)))
plt.show()
