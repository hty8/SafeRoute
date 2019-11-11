import urllib.request  # Download File
import datetime  # string manipulation according to time
import os  # Getting current directory


def get_csv(date1, date2):
    start_date = datetime.datetime.strptime(date1, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(date2, '%Y-%m-%d')
    if start_date > end_date:
        print('start_date must be earlier than end_date')
    else:
        url = 'https://data.cityofchicago.org'\
              + '/api/views/ijzp-q8t2/rows.csv?accessType=DOWNLOAD&bom=true&query=select+*+where+%60date%60+%3E%3D+%27' \
              + date1 + 'T00%3A00%3A00%27+AND+%60date%60+%3C+%27' \
              + date2 + 'T00%3A00%3A00%27'  # Download URL

        # içinde bulunduğumuz python dosyası olmalı realpath ve replace içindeki py uzantılı stringler
        pt = os.path.realpath('get_csv.py').replace('get_csv.py',
                                                    'crime_data.csv')
        urllib.request.urlretrieve(url, pt)


get_csv('2018-01-01', '2019-10-09')  # Tarih arası CSV çekiş


