import pytest
from metrics.gatherapp import get_range_for_runners


def hosts(n):
    return [str(i + 1) for i in range(n)]


def test_expect_assert_when_start_eq_end():
    with pytest.raises(AssertionError):
        get_range_for_runners(1, 1, hosts(2))


def test_return_one_job_when_there_is_one_host():
    assert 1 == len(get_range_for_runners(1, 101, hosts(1)))
    assert 1 == len(get_range_for_runners(1, 10000, hosts(1)))
    assert 1 == len(get_range_for_runners(0, 10000, hosts(1)))


def test_return_two_jobs_when_there_is_two_hosts():
    jobs = get_range_for_runners(1, 101, hosts(2))
    assert 2 == len(jobs)

    assert [(1, 51, '1'), (51, 101, '2')] == jobs


def test_pass_three_hosts_and_return_two_jobs():
    jobs = get_range_for_runners(1, 101, hosts(3))

    assert 2 == len(jobs)
    assert [(1, 51, '1'), (51, 101, '3')] == jobs

def test_xx():
    assert [(0, 1, '2')] == get_range_for_runners(0, 1, hosts(2))

    assert [(0, 50, '1'), (50, 100, '2')] == get_range_for_runners(0, 100, hosts(2))

    assert [(1, 100, '2')] == get_range_for_runners(1, 100, hosts(2))


    # assert 2 == len(get_range_for_runners(1, 101, hosts(1)))


def test_one_worker_could_grab_100_blocks_with_api_limit_100():
    jobs = get_range_for_runners(start_block=1, end_block=100, limit=100, hosts=hosts(2))
    assert 1 == len(jobs)


def test_four_workers_could_grab_100_blocks_with_api_limit_100():
    jobs = get_range_for_runners(start_block=1, end_block=400, limit=100, hosts=hosts(4))
    assert 4 == len(jobs)

    assert [(1, 101, '1'), (101, 201, '2'), (201, 301, '3'), (301, 400, '4')] == jobs


def test_get_range():
    jobs = get_range_for_runners(100000, 200000, hosts(4))
    assert [(100000, 125000, '1'), (125000, 150000, '2'), (150000, 175000, '3'), (175000, 200000, '4')] ==  jobs


import math


def create_schedule(start, end, hosts=[], limit=100):
    assert start > 0
    assert end > start
    assert limit > 0
    assert len(hosts) > 0

    total = end - start

    number_of_queries = int(math.ceil(total / limit))
    number_of_workers = min(number_of_queries, len(hosts))

    schedule = dict()

    worker = 0
    s = start

    while s < end:

        url = hosts[worker]

        if url not in schedule:
            schedule[url] = []

        schedule[url].append((s, s + limit))

        s += limit

        worker += 1

        if worker == number_of_workers:
            worker = 0

    return schedule


def test_start_should_be_greater_than_zero():
    with pytest.raises(AssertionError):
        create_schedule(0, 2)

    create_schedule(1, 2)


def test_end_should_be_greater_than_start():
    with pytest.raises(AssertionError):
        create_schedule(1, 1)

    create_schedule(1, 2)


def test_limit_should_be_greater_than_zero():
    with pytest.raises(AssertionError):
        create_schedule(1, 100, limit=0)

    # don't throw exception
    create_schedule(1, 100, limit=1)


import json


def test_x():
    assert '{"1": [[1, 2]], "2": [[2, 3]], "3": [[3, 4]], "4": [[4, 5]]}' == \
           json.dumps(create_schedule(start=1, end=5, limit=1, hosts=hosts(4)), sort_keys=True)


def test_y():
    assert '{"1": [[1, 2]]}' == \
           json.dumps(create_schedule(start=1, end=2, limit=1, hosts=hosts(4)), sort_keys=True)


def test_z():
    assert '{"1": [[1, 101]]}' == \
           json.dumps(create_schedule(start=1, end=101, limit=100, hosts=hosts(4)), sort_keys=True)


def test_a():
    assert '{"1": [[1, 101]], "2": [[101, 201]], "3": [[201, 301]], "4": [[301, 401]]}' == \
           json.dumps(create_schedule(start=1, end=401, limit=100, hosts=hosts(4)), sort_keys=True)


def test_b():
    assert '{"1": [[1, 101]], "2": [[101, 201]], "3": [[201, 301]], "4": [[301, 401]]}' == \
           json.dumps(create_schedule(start=1, end=801, limit=100, hosts=hosts(4)), sort_keys=True)




#def test_a():
 #   assert '{"1": [[1, 2]]}' == \
  #         json.dumps(create_shedule(start=1, end=101, limit=100, hosts=hosts(4)), sort_keys=True)
