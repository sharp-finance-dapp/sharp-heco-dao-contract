# sharp-dao-cuntracts 

Vyper contracts used in the [Sharp](https://www.sharp.finance/) Governance DAO.

## Testing and Development

### Dependencies

* [python3](https://www.python.org/downloads/release/python-368/) version 3.6 or greater, python3-dev
* [vyper](https://github.com/vyperlang/vyper) version [0.2.4](https://github.com/vyperlang/vyper/releases/tag/v0.2.4)
* [brownie](https://github.com/iamdefinitelyahuman/brownie) - tested with version [1.11.0](https://github.com/eth-brownie/brownie/releases/tag/v1.11.0)
* [ganache-cli](https://github.com/trufflesuite/ganache-cli) - tested with version [6.10.1](https://github.com/trufflesuite/ganache-cli/releases/tag/v6.10.1)

### Setup

To get started, first create and initialize a Python [virtual environment](https://docs.python.org/3/library/venv.html). Next, clone the repo and install the developer dependencies:

```bash
git clone git@github.com:sharp-finance-dapp/sharp-heco-dao-contract.git
cd sharp-heco-dao-contract
pip install -r requirements
```

### Running the Tests

The test suite is split between [unit](tests/unitary) and [integration](tests/integration) tests. To run the entire suite:

```bash
brownie test
```

To run accurate data for token distribution:

```bash
brownie test tests/unitary/ERC20CRV/test_epoch_time_supply.py
```

To run only the unit tests or integration tests:

```bash
brownie test tests/unitary
brownie test tests/integration
```
