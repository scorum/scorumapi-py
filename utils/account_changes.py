from api import api
import json

import time

# from influxdb import InfluxDBClient
#
#
# def main(host='localhost', port=8086):
#     """Instantiate a connection to the InfluxDB."""
#     user = 'root'
#     password = 'root'
#     dbname = 'example'
#     dbuser = 'smly'
#     dbuser_password = 'my_secret_password'
#     query = 'select value from dev_pool_scr;'
#     json_body = [
#         {
#             "measurement": "dev_pool_scr",
#             "tags": {
#                 "host": "server01",
#                 "region": "us-west"
#             },
#             "time": "2018-08-10T23:00:00",
#             "fields": {
#                 "Float_value": 3000.000000000,
#                 "Int_value": 3000000000000,
#                 "String_value": "3000.000000000 SCR",
#                 "Bool_value": True
#             }
#         }
#     ]
#
#     client = InfluxDBClient(host, port, user, password, dbname)
#
#     print("Create database: " + dbname)
#     client.create_database(dbname)
#
#     print("Create a retention policy")
#     client.create_retention_policy('ex_policy', duration='100w', replication=3, default=True, shard_duration="100w")
#
#     print("Switch user: " + dbuser)
#     client.switch_user(dbuser, dbuser_password)
#
#     print("Write points: {0}".format(json_body))
#     client.write_points(json_body)
#
#     print("Querying data: " + query)
#     result = client.query(query)
#
#     print("Result: {0}".format(result))
#
#     print("Switch user: " + user)
#     client.switch_user(user, password)
#
#     print("Drop database: " + dbname)
#     client.drop_database(dbname)
#
#
# main()

# from prometheus_client import start_http_server
# from prometheus_client import Gauge
#
#
# def prometheus():
#     start_http_server(9000)
#
#     value = 1000
#
#     g = Gauge('dev_pool_scr', "Total amount of SCR's in development pool")
#     g.set(value)  # Set to a given value
#
#     while True:
#         time.sleep(0.5)
#
#         value += 100
#
#         g.set(value)  # Set to a given value
#
# prometheus()

prod = "https://prodnet.scorum.com"
local = "http://127.0.0.1:8021"
# local = "http://127.0.0.1:38090"

blocks = api.get_blocks_history(local, 1, 1)

print(blocks)

start = time.time()

# operations = api.get_ops_history(local, 0, 1, 3)
#
# print("took: %s s" % (time.time() - start))
#
# for op in operations:
#     print(op)
    # print(json.dumps(op[1], indent=True))


# for block in blocks:
#     id = block[0]
#     body = block[1]
#
#     transactions = block[1]["transactions"]
#
#     for t in transactions:
#         print("%d : %s" % (id, t))

# for n in range(0, 4504060):
#
#     if len(response) > 0:
#         op = response[0][1]["op"]
#         if op[0] == "account_witness_vote":
#             pass


# {
#     "block_number" : 100,
#     "block_time": "2018-01-01T00:00:00",
#     "devpool_scr": 0,
#     "devpool_sp": 0,
#     "total_users_scr": 0,
#     "total_users_sp": 0,
#     "registration_pool": 0,
#     "reward_pool_scr": 0,
#     "reward_pool_sp": 0,
# }



