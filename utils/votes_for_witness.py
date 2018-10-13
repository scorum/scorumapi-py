import api
import json

prod = "https://prodnet.scorum.com"
w = {}
hist = []

for n in range(0, 4504060):
    response = api.call("http://127.0.0.1:38090", "blockchain_history_api", "get_ops_in_block", [n, 1])

    if len(response) > 0:
        op = response[0][1]["op"]
        if op[0] == "account_witness_vote":
            print("{n}: {r}".format(n=n, r=json.dumps(op[1])))

            witness = op[1]["witness"]
            approve = op[1]["approve"]
            account = op[1]["account"]

            hist.append({"block":n, "operation":op[1]})

            if witness not in w:
                w[witness] = {}
                w[witness]["approves"] = []

            if approve:
                w[witness]["approves"].append(account)
            else:
                w[witness]["approves"].remove(account)

    if n % 100000 == 0:
        print(n)
        with open("witness_votes", "w") as file:
            file.write(json.dumps(w, indent=4, sort_keys=True))

        with open("account_witness_vote_hist", "w") as file:
            file.write(json.dumps(hist))

with open("witness_votes", "w") as file:
    file.write(json.dumps(w, indent=4, sort_keys=True))

with open("account_witness_vote_hist", "w") as file:
    file.write(json.dumps(hist))