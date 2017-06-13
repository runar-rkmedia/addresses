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
from time import time, strftime, gmtime


def get_number_of_lines_in_file(file_name):
    """Return the number of lines in file."""
    with open(file_name) as f:
        for i, l in enumerate(f):
            pass
        return i + 1


def csv_reader(file_name, index, length, start_time, total_number_of_lines, lines_cycled, **kwargs):
    """Read a csv-file, and convert it to python-dictionary."""
    time1 = time()
    last_output = 0.01
    this_time = time()
    data_list = []
    lines_cycled_real = lines_cycled
    number_of_lines = get_number_of_lines_in_file(file_name)
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
            if time2 - time1 > last_output:
                total_time_spent = time2 - start_time
                last_lines_cycled_real = lines_cycled_real
                line_count = data.line_num
                last_time = this_time
                this_time = time2
                lines_cycled_real = lines_cycled + line_count
                print('\n{}/{} {} "{}"'.format(
                    index + 1,
                    length,
                    strftime("%H:%M:%S", gmtime(total_time_spent)),
                    file_name
                ))
                print(
                    'Read and shrinked {:0.1f}% of this county after {}'.format(
                        data.line_num / number_of_lines * 100,
                        # this_time-time1,

                        strftime("%H:%M:%S", gmtime(this_time - time1))
                    ))
                print('{:0.1f}% total, calculating this should take about {} more, with an average of {:0.0f} lines/second'.format(
                    lines_cycled_real / total_number_of_lines * 100,
                    strftime("%H:%M:%S", gmtime(
                        (total_number_of_lines - lines_cycled_real) / (
                            (lines_cycled_real - last_lines_cycled_real) / (this_time - last_time))
                        - (total_time_spent)
                    )),
                    (lines_cycled_real - last_lines_cycled_real) /
                    (this_time - last_time),
                ))
                last_output += .5
    return data_list, number_of_lines


def read_csv_from_list_of_files(list_of_files, time1=time()):
    """Read a list of csv-files."""
    adresser = []
    total_number_of_lines = 0
    lines_cycled = 0
    for file_name in list_of_files:
        total_number_of_lines += get_number_of_lines_in_file(file_name)
    for idx, county in enumerate(list_of_files):
        a, number_of_lines = csv_reader(
            county, idx, len(counties), time1, total_number_of_lines, lines_cycled, delimiter=';')
        adresser.append(a)
        lines_cycled += number_of_lines
        time3 = time()
        if idx == len(list_of_files) - 1:
            print("{:0.1f} seconds elapsed total".format((time3 - time1)))
    return adresser


if __name__ == '__main__':
    directory = 'data'
    counties = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            counties.append(os.path.join(directory, file))
    # counties = [
    #     counties[18],
    #     # counties[12],
    #     # counties[18],
    #     # counties[18],
    # ]
    # print(counties)

    print('''Converting and shrinking data from Kartverket, total {} counties.
           This should take about anything from 20 seconds to 10 minutes per county.
           '''.format(len(counties)))

    def read_and_shrink(queue_):
        """Description."""
        output_file = 'data/adresser.json'
        # open(output_file, 'w').close()
        adresser = []
        adresser.append(read_csv_from_list_of_files(
            counties))
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
