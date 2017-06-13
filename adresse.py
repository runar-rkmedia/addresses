# pylama:ignore=C0301,E501
"""
Extract data from kartverket's .csv-files
(http://data.kartverket.no/download/content/geodataprodukter?korttype=3637&aktualitet=All&datastruktur=All&dataskema=All)
and shrink it to only what is needed."""

import csv
import json
import os
import threading
from queue import Queue
from time import time


def csv_reader(file_name, data_list=None, **kwargs):
    """Read a csv-file, and convert it to python-dictionary."""
    time1 = time()
    last_output = 4.99
    data_list = data_list or []
    number_of_lines = 0
    with open(file_name) as f:
        for i, l in enumerate(f):
            pass
        number_of_lines = i+1
    with open(file_name) as csv_file:
        data = csv.reader(csv_file, **kwargs)
        for csv_row in data:
            this_data = {
                'vei': csv_row[4],
                'kort_vei': csv_row[5],
                'tettsted': csv_row[19],
                'postnummer': csv_row[26],
                'postnummeromrade': csv_row[27]
            }
            if this_data not in data_list:
                data_list.append(this_data)
            time2 = time()
            if time2-time1 > last_output:
                print(
                    'Read and shrinked {:0.1f}% of this county after {:0.1f} seconds'.format(
                        data.line_num/number_of_lines*100,
                        time2-time1
                    ))
                last_output += 5
    return data_list


def read_csv_from_list_of_files(list_of_files, verbose=False, time1=time()):
    """Read a list of csv-files."""
    adresser = []
    for idx, county in enumerate(counties):
        time2 = time()
        if verbose:
            print('Reading file {} of {} with name {}'.format(
                idx+1, len(counties), county
            ))
        adresser = csv_reader(county, data_list=adresser, delimiter=';')
        time3 = time()
        if verbose:
            print(
                "{:0.1f} seconds elapsed on this, totalling {:0.1f} seconds.\n".format(
                    time3-time2,
                    time3-time1,
                    ))
            if idx == len(counties)-1:
                print("{:0.1f} seconds elapsed total".format((time3-time1)))
    return adresser


if __name__ == '__main__':
    directory = 'data'
    counties = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            counties.append(os.path.join(directory, file))
    # counties = [
    #     counties[18],
    #     counties[18],
    #     counties[18],
    #     counties[12],
    # ]
    # print(counties)

    print('''Converting and shrinking data from Kartverket, total {} counties.
           This should take about anything from 20 seconds to 10 minutes per county.
           '''.format(len(counties)))

    def read_and_shrink(queue_):
        """Description."""
        output_file = 'adresse/adresser.json'
        # open(output_file, 'w').close()
        adresser = []
        adresser.append(read_csv_from_list_of_files(
            counties, verbose=True))
        with open(output_file, 'w') as fout:
            json.dump(adresser, fout)
        print('Data saved in "{}"'.format(output_file))
        queue.put('')

    queue = Queue()
    thread = threading.Thread(
        target=read_and_shrink,
        name='Thread1',
        args=[queue]
    )
    thread.daemon = True
    thread.start()
    queue.get()
