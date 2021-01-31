import sys
import datetime
import os

import json
from time import sleep
import numpy as np

USAGE_TEXT =  "Usage: {} <NUMBER OF SENSORS>".format(__file__)

def get_sensor_filename(id):
    return 'sensor-' + str(id) + '.json'

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32.0) * 5/9

class MasterController:

    def __init__(self, numberOfSensors):
        self.filename = 'master.json'
        self.numberOfSensors = numberOfSensors
        self.sensors = np.empty(shape=(numberOfSensors, 10))
        self.sensors[:] = np.nan
        self.max_temperature = 0.0
        self.min_temperature = 0.0
        self.mean_temperature = 0.0

    def get_filename(self):
        return self.filename

    def update_records(self, measurements):
        new_entry = {'measurements': []}
        new_entry['measurements'].append({
            'Sensor Number': measurements[-1]['Sensor Number'],
            'Timestamp' : str(datetime.datetime.now()),
            'Max Temperature F'  : self.max_temperature,
            'Min Temperature F'  : self.min_temperature,
            'Mean Temperature F' : self.mean_temperature,
            'Max Temperature C'  : fahrenheit_to_celsius(self.max_temperature),
            'Min Temperature C'  : fahrenheit_to_celsius(self.min_temperature),
            'Mean Temperature C' : fahrenheit_to_celsius(self.mean_temperature),
            'Alarm Count' : measurements[-1]['Alarm Count'],
            'Error Count' : measurements[-1]['Error Count']
        })

        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as json_file:
                    old_data = json.load(json_file)
                    temp = old_data['measurements']
                    temp.append(new_entry['measurements'][0])

                with open(self.filename, 'w') as json_file:
                    json.dump(old_data, json_file, indent=2)
            except json.JSONDecodeError as e:
                print('Encountered exception while reading/writing {} {}'.format(self.filename, e))
        else:
            try:
                with open(self.filename, 'w') as json_file:
                    json.dump(new_entry, json_file, indent=2)
            except json.JSONDecodeError as e:
                print('Encountered exception while reading/writing {} {}'.format(self.filename, e))

        return new_entry['measurements'][0]

    def poll_sensors(self):
        i = 0
        while i < self.numberOfSensors:
            # Read throuugh all the sensor log files starting with 0
            print("Reading from {}".format(get_sensor_filename(i)))
            try:
                with open(get_sensor_filename(i), 'r') as json_file:
                    data = json.load(json_file)
                    measurements = data['measurements']
                    n = len(measurements)
                    error_count = 0
                    for j in range(10):
                        # Try to get 10 measurements
                        try:
                            self.sensors[i][j] = float(measurements[(n-1) - j]['Temperature'])
                        except ValueError:
                            # Invalid entry, i.e. N/A
                            error_count += 1
                            pass
                        except IndexError:
                            # Not enough elements for 10 yet
                            break

                    t = np.asarray(self.sensors[i], dtype=np.float64)
                    self.mean_temperature = np.nanmean(t)
                    self.max_temperature = np.nanmax(t)
                    self.min_temperature = np.nanmin(t)

                    new_entry = self.update_records(measurements)

                # Format display information and print it
                string = ''
                for key in new_entry.keys():
                    string = "{}{}:{}. ".format(string, key, new_entry[key])

                print(string)

            except Exception as e:
                print(e)
            i += 1

    def run(self):
        while True:
            self.poll_sensors()
            sleep(30)

def main():
    num_arguments = len(sys.argv) - 1    # first argument is the file name (master_controller.py)
    if num_arguments != 1:
        print("Invalid number of arguments passed to master controller. Expected 1 and received {}".format(num_arguments))
        print(USAGE_TEXT)
        return 1

    master = MasterController(int(sys.argv[1]))

    try:
        master.run()
    except KeyboardInterrupt:
        print("Sensor data saved to {}".format(master.get_filename()))
    except Exception as e:
        print("Encountered exception: {}!".format(str(e)))


if __name__ == '__main__':
    try:
        if "-h" == sys.argv[1] or "--help" == sys.argv[1]:
            print(USAGE_TEXT)
        else:
            main()
    except IndexError:
        print(USAGE_TEXT)
