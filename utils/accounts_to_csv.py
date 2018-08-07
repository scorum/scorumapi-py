from api import helpers

def save_to_csv(accounts, keys, filename):
    with open(filename, "w") as f:
        for k in keys:
            f.write(k + "\t")

        f.write("\n")

        for a in accounts:
            for k in keys:
                f.write(str(a[k]) + "\t")

            f.write("\n")


def main():
    url = "https://prodnet.scorum.com/rpc"

    accounts = helpers.get_all_account_objects(url)

    save_to_csv(accounts, ["name",
                           "balance",
                           "scorumpower",
                           "posting_rewards_sp",
                           "curation_rewards_sp",
                           "post_count",
                           "comment_count"],
                "accounts.csv")
    print("done.")
