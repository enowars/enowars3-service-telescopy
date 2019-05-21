import requests
import json
import random
import string
import json
from faker import Faker
from enochecker import BaseChecker, BrokenServiceException, run
from primes import primes

session = requests.Session()
fake = Faker()
PRIMES_COUNT = 19800


class TelescopyChecker(BaseChecker):
    port = 8000  # default port to send requests to.
    USERNAME = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    PASSWORD = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    PLANET_NAME = fake.name()

    def putflag(self):
        self.register(self.USERNAME, self.PASSWORD)
        self.login(self.USERNAME, self.PASSWORD)
        self.add_planet()

    def getflag(self):
        self.http_get("/")
        self.login(self.team_db['USERNAME'], self.team_db['PASSWORD'])
        planet = self.get_planet()
        if planet['flag'] == self.flag:
            print("the flag is still there :)", flush=True)
        else:
            raise BrokenServiceException("Incorrect flag {}".format(self.flag))

    def putnoise(self):
        pass

    def getnoise(self):
        pass

    def havoc(self):
        pass

    def register(self, username, password):
        print("Start registration  U: " + username + "  P: " + password, flush=True)
        data = {'username': username, 'password': password}
        resp = self.http_post('/register', data)

        if resp.status_code != 200:
            raise BrokenServiceException("Could not register in the service")

    def login(self, username, password):
        print("loging in", flush=True)

        data = {'username': username, 'password': password}
        print("finished loging in", flush=True)

        resp = self.http_post('/login', data)
        cookie = resp.cookies["session"]
        print("cookie " + cookie, flush=True)

        if resp.status_code == 200:
            self.team_db['USERNAME'] = username
            self.team_db['PASSWORD'] = password
        else:
            raise BrokenServiceException("Could not login in the service")

    def add_planet(self):
        data = {'name': fake.name(),
                'declination': '10.1',
                'rightAscension': '10.2',
                'flag': self.flag}
        resp = self.http_post('/addPlanet', data)
        resp_dict = json.loads(resp.text)

        print("planet added with id: " + resp_dict['planetId'], flush=True)

        self.team_db[self.flag] = resp_dict['planetId']

    def get_planet(self):
        planet_id = self.team_db[self.flag]

        try:
            index = self.team_db[self.team]
        except KeyError:
            self.team_db[self.team] = 0
            index = self.team_db[self.team]

        print("TEAM: {}, counter: {}, prime: {}".format(self.team, self.team_db[self.team], primes[index]), flush=True)
        data = {'ticket': "-" + str(primes[index]), 'id': planet_id}

        self.team_db[self.team] = self.team_db[self.team] + 1

        resp = self.http_get('/getPlanet', data)
        resp_dict = json.loads(resp.text)

        print("planet retrieved with id: " + resp_dict['planetId'], flush=True)
        return resp_dict


app = TelescopyChecker.service
if __name__ == "__main__":
    run(TelescopyChecker)
