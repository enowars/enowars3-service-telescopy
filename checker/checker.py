import requests
import json
import random
import string
import json
from faker import Faker
from enochecker import BaseChecker, BrokenServiceException, run

session = requests.Session()
fake = Faker()


class TelescopyChecker(BaseChecker):
    port = 8000  # default port to send requests to.
    USERNAME = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    PASSWORD = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    PLANET_NAME = fake.name()
    global data

    def putflag(self):

        self.register(self.USERNAME, self.PASSWORD)
        self.login(self.USERNAME, self.PASSWORD)
        self.add_planet()
    def getflag(self):
        print(self.USERNAME, flush=True)
        self.http_get("/")
        self.get_planet()
        # TODO does get all planets work?


        # try:
        # tag = self.team_db[self.flag]
        # except KeyError as ex:
        #     raise BrokenServiceException("Inconsistent Database: Couldn't get tag for team/flag ({})".format(self.flag))

        # r = self.http_get("/api/SearchAttacks", params={"needle": tag})
        # self.info("Parsing search result")
        # try:
        #     search_results = json.loads(r.text)
        #     id = search_results["matches"][0]["id"]
        # except Exception as ex:
        #     raise BrokenServiceException("Invalid JSON Response: {} ({})".format(r.text, ex))

        # self.info("Found attack (id={})".format(id))
        # self.info("Fetching attack: {}".format({"id": id, "password": self.flag}))

        # r = self.http_get("/api/GetAttack", params={"id": id, "password": self.flag}, timeout=5, verify=False)
        # self.info("Parsing GetAttack result")
        # try:
        #     attack_results = json.loads(r.text)
        # except Exception:
        #     raise BrokenServiceException("Invalid JSON: {}".format(r.text))

        # try:
        #     flag_field = "attackDate" if self.flag_idx % 2 == 0 else "location"
        #     if attack_results["attack"][flag_field] != self.flag:
        #         raise BrokenServiceException(
        #             "Incorrect flag in date field (searched for {} in {} - {})".format(self.flag, attack_results,
        #                                                                                flag_field))
        # except Exception as ex:
        #     if isinstance(ex, BrokenServiceException):
        #         raise
        #     raise BrokenServiceException(
        #         "Error parsing json: {}. {} (expected: {})".format(attack_results, ex, self.flag))

    def putnoise(self):
        pass

    def getnoise(self):
        pass

    def havoc(self):
        pass

    def register(self, username, password):
        print("Start registration  U: " + username + "  P: " + password, flush=True)
        data = {'username': username, 'password': password}
        self.http_post('/register', data)

    def login(self, username, password):
        print("loging in", flush=True)

        data = {'username': username, 'password': password}
        print("finished loging in", flush=True)

        resp = self.http_post('/login', data)
        cookie = resp.cookies["session"]
        print("cookie " + cookie, flush=True)

        # TODO login success?

    def add_planet(self):
        data = {'name': fake.name(),
                'declination': '10.1',
                'rightAscension': '10.2',
                'flag': self.flag}
        resp = self.http_post('/addPlanet', data)
        resp_dict = json.loads(resp.text)

        print("planet added with id: " + resp_dict['planetId'], flush=True)

        #todo where we store the id??



    def get_planet(self):
        #todo get the id

        data = {'ticket': '100000000901',
                'planetId' : '???'
                }
        resp = self.http_get('/getPlanet', data)
        resp_dict = json.loads(resp.text)
        self.planet_id = resp_dict['planetId']
        print("planet retrieved with id: " + resp_dict['planetId'], flush=True)

        if resp_dict['flag'] == self.flag :
            print("the flag is still there :)", flush=True)


app = TelescopyChecker.service
if __name__ == "__main__":
    run(TelescopyChecker)
