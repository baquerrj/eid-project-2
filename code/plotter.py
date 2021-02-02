import matplotlib.pyplot as plt
import numpy as np

# https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/masked_demo.html#sphx-glr-gallery-lines-bars-and-markers-masked-demo-py


def plot(sensor_db, sensors):

    _, ax = plt.subplots()

    for sensor in range(sensors):
        temperatures = [db['temperature']
                        for db in sensor_db if db['sensorId'] == sensor]
        temperatures = np.array(temperatures)
        temperatures_masked = np.ma.masked_where(
            temperatures == 999, temperatures)

        ax.plot(range(len(temperatures)), temperatures_masked, '*--',
                markersize=3, label='sensor-{}'.format(sensor), linewidth=1.5)
    plt.xlabel('Measurements')
    plt.ylabel('Temperature (Fahrenheit)')
    plt.legend()
    plt.show()
