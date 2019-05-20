import requests
import json
import random
import string
import json
from faker import Faker
from enochecker import BaseChecker, BrokenServiceException, run

session = requests.Session()
fake = Faker()

primes = [200000033, 200000039, 200000051, 200000069, 200000081, 200000083, 200000089, 200000093, 200000107, 200000117,
          200000123, 200000131, 200000161, 200000183, 200000201, 200000209, 200000221, 200000237, 200000239, 200000243,
          200000299, 200000321, 200000329, 200000347, 200000377, 200000399, 200000417, 200000431, 200000447, 200000453,
          200000477, 200000483, 200000491, 200000513, 200000527, 200000531, 200000543, 200000551, 200000579, 200000677,
          200000719, 200000729, 200000777, 200000797, 200000803, 200000819, 200000831, 200000833, 200000863, 200000881,
          200000891, 200000917, 200000929, 200000987, 200000989, 200001001, 200001007, 200001013, 200001019, 200001047,
          200001059, 200001071, 200001103, 200001143, 200001149, 200001173, 200001187, 200001211, 200001223, 200001233,
          200001247, 200001253, 200001259, 200001271, 200001283, 200001337, 200001343, 200001349, 200001419, 200001427,
          200001437, 200001449, 200001509, 200001517, 200001551, 200001577, 200001587, 200001611, 200001673, 200001691,
          200001707, 200001743, 200001757, 200001773, 200001797, 200001827, 200001833, 200001839, 200001853, 200001869,
          200001877, 200001899, 200001929, 200001931, 200001943, 200001947, 200001953, 200001973, 200002007, 200002027,
          200002051, 200002079, 200002081, 200002091, 200002123, 200002129, 200002133, 200002171, 200002177, 200002193,
          200002213, 200002219, 200002259, 200002277, 200002301, 200002333, 200002351, 200002393, 200002409, 200002441,
          200002471, 200002487, 200002489, 200002511, 200002541, 200002559, 200002567, 200002577, 200002613, 200002643,
          200002657, 200002667, 200002703, 200002709, 200002717, 200002727, 200002753, 200002769, 200002783, 200002801,
          200002823, 200002853, 200002877, 200002883, 200002903, 200002921, 200002939, 200002951, 200002967, 200002981,
          200002993, 200003003, 200003017, 200003057, 200003059, 200003077, 200003081, 200003099, 200003123, 200003173,
          200003179, 200003197, 200003213, 200003231, 200003257, 200003261, 200003269, 200003281, 200003299, 200003303,
          200003327, 200003339, 200003341, 200003359, 200003369, 200003387, 200003393, 200003497, 200003501, 200003539,
          200003563, 200003579, 200003591, 200003593, 200003603, 200003627, 200003647, 200003669, 200003693, 200003729]

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
        if planet['flag'] != self.flag:
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
        data = {'ticket': "-" + str(primes.pop()), 'id': planet_id}

        resp = self.http_get('/getPlanet', data)
        resp_dict = json.loads(resp.text)

        print("planet retrieved with id: " + resp_dict['planetId'], flush=True)
        return resp_dict


app = TelescopyChecker.service
if __name__ == "__main__":
    run(TelescopyChecker)
