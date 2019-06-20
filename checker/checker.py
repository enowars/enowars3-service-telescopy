import requests
import json
import random
import string
import json
import sympy
from enochecker import BaseChecker, BrokenServiceException, run

# from primes import primes

session = requests.Session()
PRIMES_COUNT = 19800

teamIndexes = {}


class TelescopyChecker(BaseChecker):
    port = 80  # default port to send requests to.
    USERNAME = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    PASSWORD = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))

    flag_count = 1
    noise_count = 0
    havoc_count = 1

    def exploit(self):
        pass

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
            self.debug("the flag is still there :)")
        else:
            raise BrokenServiceException("Incorrect flag {}".format(self.flag))

    def putnoise(self):
        pass

    def getnoise(self):
        pass

    def havoc(self):
        try:
            un = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
            pw = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
            self.register(un, pw)
            self.login(un, pw)

            name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
            declination = str(round(random.uniform(0.6, 155.5), 3))
            rightAscension = str(round(random.uniform(0.6, 155.5), 3))
            flag = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(30))
            data = {'name': name,
                    'declination': declination,
                    'rightAscension': rightAscension,
                    'flag': flag}
            self.add_planet2(data)
            self.check_planet_list(name)
            self.check_planet_details(name, declination, rightAscension)
        except:
            raise BrokenServiceException("something wrong with the service")

    def register(self, username, password):
        print("Start registration  U: " + username + "  P: " + password, flush=True)
        self.debug("Start registration  U: " + username + "  P: " + password)
        data = {'username': username, 'password': password}
        resp = self.http_post('/register', data)

        # if resp.status_code != 200:
        #     raise BrokenServiceException("Could not register in the service")

    def login(self, username, password):
        print("loging in", flush=True)
        self.debug("loging in")
        data = {'username': username, 'password': password}

        resp = self.http_post('/login', data)
        cookie = resp.cookies["session"]
        print("cookie " + cookie, flush=True)
        self.debug("cookie " + cookie)

        # if resp.status_code == 200:
        self.team_db['USERNAME'] = username
        self.team_db['PASSWORD'] = password
        # else:
        #     raise BrokenServiceException("Could not login in the service")

    def add_planet(self):
        data = {'name': ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15)),
                'declination': str(round(random.uniform(0.6, 155.5), 2)),
                'rightAscension': str(round(random.uniform(0.6, 155.5), 2)),
                'flag': self.flag}
        resp = self.http_post('/addPlanet', data)
        print("\n \n \n " + self.team + "\n \n \n \n \n " + resp.text, flush=True)
        self.debug("\n \n " + self.team + "\n \n \n " + resp.text)

        resp_dict = resp.json()

        print("planet added with id: " + resp_dict['planetId'], flush=True)
        self.debug("planet added with id: " + resp_dict['planetId'])

        self.team_db[self.flag] = resp_dict['planetId']

    def add_planet2(self, data):
        resp = self.http_post('/addPlanet', data)
        resp_dict = json.loads(resp.text)
        print("planet added with id: " + resp_dict['planetId'], flush=True)
        self.debug("planet added with id: " + resp_dict['planetId'])

    def get_planet(self):
        try:
            planet_id = self.team_db[self.flag]
        except KeyError:
            raise BrokenServiceException("can't retrieve planet")

        # try:
        #     index = self.team_db[self.team]
        #     # index = teamIndexes[self.team]
        # except KeyError:
        #     self.team_db[self.team] = 0
        #     index = self.team_db[self.team]
        #     # teamIndexes[self.team] = 0
        #     # index = 0

        # print("TEAM: {}, counter: {}, prime: {}".format(self.team,str(index), primes[index]), flush=True)
        ticket = sympy.nextprime(random.randint(100000000, 10000000000))
        data = {'ticket': "-" + str(ticket), 'id': planet_id}

        # teamIndexes[self.team] = index + 1
        resp = self.http_get('/getPlanet', data)
        print("\n \n \n \n " + self.team + " \n \n \n  index " + str(ticket) + " \n \n" + resp.text, flush=True)
        self.debug("\n \n \n \n " + self.team + " \n \n \n  index " + str(ticket) + " \n \n" + resp.text)
        try:
            resp_dict = json.loads(resp.text)
        except:
            raise BrokenServiceException("can't retrieve planet")
        print("planet retrieved with id: " + resp_dict['planetId'], flush=True)
        self.debug("planet retrieved with id: " + resp_dict['planetId'])

        return resp_dict

    def check_planet_list(self, name):
        resp = self.http_get("/")
        print("checking planets list \n " + resp.text, flush=True)
        self.debug("checking planets list \n " + resp.text)
        if name not in resp.text:
            raise BrokenServiceException("planet list not showing")
        else:
            print("planet name is displayed : " + name + "\n", flush=True)
            self.debug("planet name is displayed : " + name + "\n")

    def check_planet_details(self, name, declination, rightAscension):
        resp = self.http_get("/planet_details?name=" + name)
        print("checking planets details \n " + resp.text, flush=True)
        self.debug("checking planets details \n " + resp.text)

        if declination not in resp.text or rightAscension not in resp.text:
            raise BrokenServiceException("planet details not working")
        else:
            print("planet details displayed \n  declination: " + declination + " rightAscension" + rightAscension,
                  flush=True)
            self.debug("planet details displayed \n  declination: " + declination + " rightAscension" + rightAscension)


app = TelescopyChecker.service
if __name__ == "__main__":
    run(TelescopyChecker)
