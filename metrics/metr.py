from metrics import timeit
from metrics.app import App


@timeit
def main():
    app = App()
    app.run()


main()
