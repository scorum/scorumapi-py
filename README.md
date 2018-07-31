How to install
===
```
pipenv --three install
pipend shell
pip install .
```
Example
===
```
# get post information
scorumapi --method get_content --args alextazy sports-media-your-media-your-money

# get statistics
scorumapi --host rpc5-mainnet-weu-v2.scorum.com:8001 --api blockchain_statistics --method get_stats_for_interval --args 2018-06-13T00:00:00 2018-06-14T00:00:00

# or even without api
scorumapi --host rpc5-mainnet-weu-v2.scorum.com:8001 --method get_stats_for_interval --args 2018-06-13T00:00:00 2018-06-14T00:00:00
```
