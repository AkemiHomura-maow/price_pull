from brownie import VeloOracle, chain
from scripts.get_tokens import fetch_tokens
from scripts.block import get_block
import json

if chain.id == 10:
    chain_name = 'op'
    data = json.load(open('./config.json'))['velo']
    oracle = VeloOracle.at('0x6a3af44e23395d2470f7c81331add6ede8597306')
elif chain.id == 8453:
    chain_name = 'base'
    data = json.load(open('./config.json'))['aero']
    oracle = VeloOracle.at('0xCbF5b6abF55Fb87271338097FDd03E9d82a9d63f')

src = fetch_tokens(chain_name)
connectors = data['connectors']
dst = data['dst']

def fetch(blk=None):
  results = []
  call_length = 150
  for start_i in range(0,len(src),call_length):
    in_connectors = src[start_i:start_i + call_length] + connectors + [dst]
    results.extend(oracle.getManyRatesWithConnectors(len(src[start_i:start_i + call_length]), in_connectors, block_identifier=blk))
  return results

# Fetch prices at the latest block
print('Fetching current prices')
results = fetch()
for token, price in zip(src, results):
   if price != 0:
    print(token, price/1e18)

print('----------------------------------------------------------------------------------')
# Should be set to >= 1723788000
timestamp = 1723788000
print(f'Fetching prices at timestamp {timestamp}')
# Fetch historical prices
results = fetch(get_block(timestamp, chain_name))

for token, price in zip(src, results):
   if price != 0:
    print(token, price/1e18)
