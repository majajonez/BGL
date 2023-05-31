from datetime import date
from faker import *
import random


cities = ['Tokio', 'Delhi', 'Szanghaj', 'São Paulo', 'Meksyk', 'Kair', 'Mumbai', 'Pekin', 'Dhaka', 'Osaka',
          'Nowy Jork', 'Karaczi', 'Calcutta', 'Istanbul', 'Buenos Aires', 'Lagos', 'Kinshasa', 'Rio de Janeiro',
          'Manila', 'Moskwa', 'Dżakarta', 'Londyn', 'Lima', 'Bangkok', 'Nairobi', 'Los Angeles', 'Chennai',
          'Bogota', 'Riad', 'Hongkong', 'Santiago', 'Ahmedabad', 'Bagdad', 'Singapur', 'Ankarra', 'Madryt',
          'Berlin', 'Tajpej', 'Kairuan', 'Lakhnau', 'Johannesburg', 'Maracaibo', 'Hangzhou', 'Durban', 'Algier',
          'Addis Abeba', 'Shijiazhuang', 'Mediolan', 'Harbin', 'Suzhou', 'Chongqing', 'Alexandria', 'Kanton',
          'Jinan', 'Hyderbad', 'Surat', 'Pune', 'Dalian', 'Dar es Salaam', 'Shenzhen', 'Nanjing', 'Wuhan',
          'Kuala Lumpur', 'Chengdu', 'Luanda', 'Daka', 'Kampala', 'Caracas', 'Taegu', 'Al-Kuwejt', 'Jaipur',
          'Aleppo', 'Indore', 'Omsk', 'Kandahar', 'Lucknow', 'Baku', 'Surabaja', 'Al-Madinah', 'Dammam',
          'Patna', 'Houston', 'Warszawa']

date_ = date.today()


class Random_user():
    def __init__(self):
        fake = Faker()
        person = fake.name()
        self.name = person.split(' ')[0]
        self.email = self.name + '@gmail.com'
        self.password = self.name + str(len(person))
        self.city = random.choice(cities)



class Random_event():
    def __init__(self):
        self.title = f'test_event {random.choice(cities)} {date_}'
        self.description = 'testy gry w dniu' + str(date_)
        self.when = str(date_)
        self.where = random.choice(cities)
        self.seats = 4

