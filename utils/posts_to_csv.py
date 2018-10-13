from api import helpers
from metrics import timeit


def save_to_csv(data, keys, filename):
    with open(filename, "w") as f:
        for k in keys:
            f.write(k + "\t")

        f.write("\n")

        for a in data:
            for k in keys:
                f.write(str(a[k]) + "\t")

            f.write("\n")


@timeit
def posts_to_csv():
    # url = "https://prodnet.scorum.com/rpc"
    url = "http://127.0.0.1:8021"

    posts = helpers.get_all_posts(url)

    print(len(posts))

    save_to_csv(posts, [
        "author",
        "permlink"
    ], "posts.csv")

    print("done.")


def main():
    posts_to_csv()


if __name__ == "__main__":
    posts_to_csv()
