import time
import datetime


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            # print(str(datetime.timedelta(te - ts)))
            print('%r  %s' % (method.__name__, str(datetime.timedelta(seconds=(te - ts)))))

        return result

    return timed


def started(method):
    def xxx(*args, **kw):

        print("started %s" % method.__name__)
        result = method(*args, **kw)
        print("finished %s" % method.__name__)

        return result

    return xxx
