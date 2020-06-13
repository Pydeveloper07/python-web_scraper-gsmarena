import requests
import psycopg2
from bs4 import BeautifulSoup

URL = 'https://www.gsmarena.com/samsung_galaxy_s10_lite-9917.php'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'lxml')
specs = soup.find(id='specs-list')
# tables = specs.find_all('table')
# for table in tables:
#     table_rows = table.find_all('tr')
#     for tr in table_rows:
#         ttl = tr.find('td', class_='ttl')
#         nfo = tr.find('td', class_='nfo')
#         try:
#             name = ttl.find('a')
#             content = nfo.find('a')
#         except Exception:
#             continue
#         if not content:
#             content = nfo
#         try:
#             print('{0}:\n    {1}'.format(name.text, content.text))
#         except AttributeError:
#             print(tr.prettify())
article_info = soup.find(class_='article-info')
phone = {}
name = article_info.find('h1', class_='specs-phone-name-title').text
phone['name'] = name
price = 1
phone['price'] = price
color = specs.find('td', attrs={'data-spec':'colors'}).text
phone['color'] = color
# announced_date_temp = specs.find('td', attrs={'data-spec':'year'}).text.split('.')
# announced_date = announced_date_temp[0]
# phone['announced_date'] = announced_date
announced_date = specs.find('td', attrs={'data-spec':'year'}).text
phone['announced_date'] = announced_date
status_temp = specs.find('td', attrs={'data-spec':'status'}).text.split('.')
status = status_temp[0]
phone['status'] = status
# released_date_temp = announced_date_temp[1].split(' ')
# released_date = released_date_temp[len(released_date_temp)-2] + released_date_temp[len(released_date_temp)-1]
try:
    released_date = status_temp[2]
except IndexError:
    released_date = status_temp[1]
phone['released_date'] = released_date
display_type = specs.find('td', attrs={'data-spec':'displaytype'}).text
phone['display_type'] = display_type
display_size_temp = specs.find('td', attrs={'data-spec':'displaysize'}).text
display_size = display_size_temp.split(' ')[0]
phone['display_size'] = display_size
display_resolution_temp = specs.find('td', attrs={'data-spec':'displayresolution'}).text.split(' ')
display_resolution = display_resolution_temp[0] + display_resolution_temp[1] + display_resolution_temp[2]
phone['display_resolution'] = display_resolution
dimensions = specs.find('td', attrs={'data-spec':'dimensions'}).text
phone['dimensions'] = dimensions
weight = specs.find('td', attrs={'data-spec':'weight'}).text.split(' ')[0]
phone['weight'] = weight
sim = specs.find('td', attrs={'data-spec':'sim'}).text
phone['sim'] = sim
phone['ram'] = 1
phone['storage'] = 1
card_slot = specs.find('td', attrs={'data-spec':'memoryslot'}).text
phone['card_slot'] = card_slot
dimensions = specs.find('td', attrs={'data-spec':'dimensions'}).text
phone['dimensions'] = dimensions
phone['mc_type'] = 'single'
phone['mc'] = '1 MP'
mc_features = specs.find('td', attrs={'data-spec':'cam1features'}).text
phone['mc_features'] = mc_features
mc_video = specs.find('td', attrs={'data-spec':'cam1video'}).text
phone['mc_video'] = mc_video
phone['sc_type'] = 'single'
phone['sc'] = '1 MP'
if specs.find('td', attrs={'data-spec':'cam2features'}):
    sc_features = specs.find('td', attrs={'data-spec':'cam2features'}).text
else:
    sc_features = None
phone['sc_features'] = sc_features
if specs.find('td', attrs={'data-spec':'cam2video'}):
    sc_video = specs.find('td', attrs={'data-spec':'cam2video'}).text
else:
    sc_video = None
phone['sc_video'] = sc_video
os = specs.find('td', attrs={'data-spec':'os'}).text
phone['os'] = os
cpu_temp = specs.find('td', attrs={'data-spec':'cpu'}).text.split(' ')
cpu_type = cpu_temp[0].lower()
phone['cpu_type'] = cpu_type
cpu_temp = list(cpu_temp)
cpu_temp[0] = ''
cpu = ' '.join(cpu_temp)[1:]
phone['cpu'] = cpu
chipset = specs.find('td', attrs={'data-spec':'chipset'}).text
phone['chipset'] = chipset
network = specs.find('a', attrs={'data-spec':'nettech'}).text
phone['network'] = network
if specs.find('td', attrs={'data-spec':'usb'}):
    usb = specs.find('td', attrs={'data-spec':'usb'}).text
else:
    usb = None
battery_temp = specs.find('td', attrs={'data-spec':'batdescription1'}).text.split(' ')
battery_type = battery_temp[1]
phone['battery_type'] = battery_type
battery_capacity = battery_temp[2]
phone['battery_capacity'] = battery_capacity
sensors = specs.find('td', attrs={'data-spec':'sensors'}).text
phone['sensors'] = sensors
phone['photo_main'] = r'C:\Users\User\Pictures\phones\nokia 8.3 5G\nokia-8.3-5G-camera-module.jpg'
gpu = specs.find('td', attrs={'data-spec':'gpu'}).text
phone['gpu'] = gpu
phone['brand_id'] = 'Samsung'
print(phone)


try:
    connection = psycopg2.connect(
        user='postgres',
        password='black_tiger07!',
        host='localhost',
        port='5432',
        database='mobileinfo'
    )
    cursor = connection.cursor()
    insert_query = """ INSERT INTO listings_mobilephone(name, price, is_mc_exists, is_sc_exists, is_cardslot_exists, multitouch, color, announced_date, status, released_date, 
    display_type, display_size, display_resolution, dimensions, weight, sim, card_slot, mc_features, mc_video,
    sc_features, sc_video, loudspeaker, headphone_connector, os, cpu_type, cpu, chipset, network, wlan, bluetooth ,
    gps, radio, nfc, usb, is_battery_removable, battery_type, battery_capacity, sensors,
    photo_main, is_wkp, gpu, brand_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    data = (phone['name'], 100, True, True, True, True, phone['color'], phone['announced_date'], phone['status'], phone['released_date'],
            phone['display_type'], phone['display_size'], phone['display_resolution'], phone['dimensions'],
            phone['weight'], 'sim', phone['card_slot'], phone['mc_features'], phone['mc_video'],
            phone['sc_features'], phone['sc_video'], True, True, phone['os'], phone['cpu_type'], phone['cpu'], phone['chipset'],
            phone['network'], True, True, True, True, True, 'usb', False, phone['battery_type'], phone['battery_capacity'], phone['sensors'],
            phone['photo_main'], False, phone['gpu'], phone['brand_id'])
    cursor.execute(insert_query, data)
    connection.commit()
    count = cursor.rowcount()
    print('Successfully inserted to the table!')
except (Exception, psycopg2.Error) as error:
    print('Failed to insert!')
    print('Error:', error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print('PostgreSQL is now closed!')
