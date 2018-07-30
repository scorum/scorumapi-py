from api import helpers


def save_to_csv(data, keys, filename):
    with open(filename, "w") as f:
        for k in keys:
            f.write(k + "\t")

        f.write("\n")

        for a in data:
            for k in keys:
                f.write(str(a[k]) + "\t")

            f.write("\n")


def main():
    url = "https://prodnet.scorum.com/rpc"

    posts = helpers.get_all_posts(url)

    save_to_csv(posts, [
        "author",
        "permlink"
    ], "posts.csv")

    print("done.")
