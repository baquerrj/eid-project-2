import sys
import datetime
import os

import json
from time import sleep
import numpy as np

from pathlib import Path
import pymysql

codeDirectory = Path(__file__).parent.absolute()
rootDirectory = codeDirectory.parent
resultsDirectory = rootDirectory / 'results'

sys.path.append(codeDirectory)

from plotter import plot

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32.0) * 5/9

class MasterController:

    def __init__(self, numberOfSensors=4):
        self.filename = resultsDirectory / 'master.json'
        self.numberOfSensors = numberOfSensors
        self.sensor_db = [{}]    # empty list of dictionaries
        self.sensors = np.empty(shape=(numberOfSensors, 10))
        self.sensors[:] = np.nan
        self.max_temperature = 0.0
        self.min_temperature = 0.0
        self.mean_temperature = 0.0
        self.errorCount = 0

    def connect(self):
        with open(codeDirectory / 'config.json', 'r') as json_file:
            try:
                data = json.load(json_file)
                con = pymysql.connect(host=data['host'],
                            user=data['user'],
                            password=data['password'],
                            db=data['database'],
                            cursorclass=pymysql.cursors.DictCursor)
                return con
            except json.JSONDecodeError as e:
                self.errorCount += 1
                print("ERROR[{}]: invalid config.json: {}".format(self.errorCount, e))
            except pymysql.Error as e:
                self.errorCount += 1
                print("ERROR[{}]: failed to connect to db {}: {}".format(self.errorCount,
                                                                         data['database'], e))
        return None

    def get_filename(self):
        return self.filename

    def filter_db(self):
        # https://stackoverflow.com/questions/29051573/python-filter-list-of-dictionaries-based-on-key-value/29051598
        # Filter db on sensor id
        for i in range(self.numberOfSensors):
            measurements = [d for d in self.sensor_db if d['sensorId'] == i]
            n = len(measurements)
            validRecords = 0
            for j in range(10):
                try:
                    if measurements[(n-1)- j]['temperature'] != 999:
                        self.sensors[i][j] = float(measurements[(n-1)- j]['temperature'])
                        validRecords += 1
                    else:
                        self.errorCount += 1
                        print("ERROR[{}]: invalid temperature for sensor-{}".format(self.errorCount, i))
                except IndexError:
                    # Not enough elements for 10 yet
                    break

            t = np.asarray(self.sensors[i], dtype=np.float64)
            if validRecords > 0:
                self.mean_temperature = np.nanmean(t)
                self.max_temperature = np.nanmax(t)
                self.min_temperature = np.nanmin(t)
            else:
                self.errorCount += 1
                print("ERROR[{}]: no valid records for sensor-{}".format(self.errorCount, i))

            new_entry = self.update_records(measurements)

            # Format display information and print it
            string = ''
            for key in new_entry.keys():
                string = "{}{}:{}. ".format(string, key, new_entry[key])

            print(string)

    def update_records(self, measurements):
        new_entry = {'measurements': []}
        new_entry['measurements'].append({
            'Sensor Number': measurements[-1]['sensorId'],
            'Timestamp' : str(datetime.datetime.now()),
            'Max Temperature F'  : self.max_temperature,
            'Min Temperature F'  : self.min_temperature,
            'Mean Temperature F' : self.mean_temperature,
            'Max Temperature C'  : fahrenheit_to_celsius(self.max_temperature),
            'Min Temperature C'  : fahrenheit_to_celsius(self.min_temperature),
            'Mean Temperature C' : fahrenheit_to_celsius(self.mean_temperature),
            'Alarm Count' : measurements[-1]['alarm_count'],
            'Error Count' : measurements[-1]['error_count']
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
        try:
            con = self.connect()
            with con.cursor() as cur:
                cur.execute('SELECT * FROM sensor_db.sensors')
                self.sensor_db = cur.fetchall()
        except Exception as e:
            self.errorCount += 1
            print("ERROR[{}]: {}".format(self.errorCount, e))
        finally:
            con.close()


    def run(self):
        while True:
            print("Checking database...")
            self.poll_sensors()
            if len(self.sensor_db) > 0:
                self.filter_db()
            else:
                print("No data yet...")
            sleep(30)

def main():
    master = MasterController()

    try:
        master.run()
    except KeyboardInterrupt:
        print("Log file saved to: {}".format(master.get_filename()))
        print("Plotting temperature measurements")
        plot(master.sensor_db, master.numberOfSensors)

    print("Exiting... Total error count: {}".format(master.errorCount))

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Error while running: {}".format(e))
