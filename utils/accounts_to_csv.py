from api import helpers

from metrics import timeit


def save_to_csv(accounts, keys, filename):
    with open(filename, "w") as f:
        for k in keys:
            f.write(k + "\t")

        f.write("\n")

        for a in accounts:
            for k in keys:
                f.write(str(a[k]) + "\t")

            f.write("\n")


@timeit
def accounts_to_csv():
    # url = "https://prodnet.scorum.com/rpc"
    url = "http://127.0.0.1:8021"

    accounts = helpers.get_all_account_objects(url)

    import os
    print(os.getcwd())

    save_to_csv(accounts, ["name",
                           "balance",
                           "scorumpower",
                           "posting_rewards_sp",
                           "curation_rewards_sp",
                           "post_count",
                           "comment_count"],
                "accounts.csv")

def main():
    accounts_to_csv()

if __name__ == "__main__":
    accounts_to_csv()
