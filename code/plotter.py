import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/masked_demo.html#sphx-glr-gallery-lines-bars-and-markers-masked-demo-py


def plot(sensor_db, sensors):

    _, ax = plt.subplots()

    for sensor in range(sensors):
        temperatures = [db['temperature']
                        for db in sensor_db if db['sensorId'] == sensor]
        temperatures = np.array(temperatures)
        temperatures_masked = np.ma.masked_where(
            temperatures == 999, temperatures)

        times = [db['timestamp'] for db in sensor_db if db['sensorId'] == sensor]
        for i in range(len(times)):
            times[i] = datetime.timestamp(
                datetime.strptime(times[i], '%m/%d/%Y, %I:%M:%S %p'))
        t = np.array(times)
        t = t[:] - t[0]
        ax.plot(t, temperatures_masked, '*--',
                markersize=3, label='sensor-{}'.format(sensor), linewidth=1.5)
    plt.xlabel('Runtime (seconds)')
    plt.ylabel('Temperature (Fahrenheit)')
    plt.title('Temperature Measurements for {} Sensors'.format(sensors+1))
    plt.legend()
    plt.show()
