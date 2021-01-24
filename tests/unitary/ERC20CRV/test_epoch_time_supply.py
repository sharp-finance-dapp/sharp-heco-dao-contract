import brownie

WEEK = 86400 * 7
YEAR = 365 * 86400
BOOST_RATE = 300_000_000 * 52 * 10 ** 18 // YEAR

def test_start_epoch_time_write(token, chain, accounts):
    creation_time = token.start_epoch_time() # one year ago + 8 days
    chain.sleep(YEAR)
    chain.sleep(86400) # one day later
    token.update_boost_mining_parameters() # 
    chain.mine() 
    chain.sleep(WEEK - 86400)
    
    chain.mine()

    # the constant function should not report a changed value
    assert token.start_epoch_time() == creation_time

    # the state-changing function should show the changed value
    assert token.start_epoch_time_write().return_value == creation_time + YEAR

    # after calling the state-changing function, the view function is changed
    assert token.start_epoch_time() == creation_time + YEAR


def test_start_epoch_time_write_same_epoch(token, chain, accounts):
    # calling `start_epoch_token_write` within the same epoch should not raise
    token.start_epoch_time_write()
    token.start_epoch_time_write()


def test_update_mining_parameters(token, chain, accounts):
    creation_time = token.start_epoch_time()
    new_epoch = creation_time + YEAR - chain.time()
    chain.sleep(new_epoch)
    token.update_boost_mining_parameters({'from': accounts[0]})
    chain.mine()
    chain.sleep(WEEK)
    token.update_mining_parameters({'from': accounts[0]})

def test_update_mining_parameters_same_epoch(token, chain, accounts):
    creation_time = token.start_epoch_time()
    chain.sleep(86400)
    token.update_boost_mining_parameters()
    chain.mine()
    new_epoch = creation_time + YEAR - 86400 - chain.time()
    chain.sleep(new_epoch - 3)
    with brownie.reverts("dev: too soon!"):
        token.update_mining_parameters({'from': accounts[0]})


def test_mintable_in_timeframe_end_before_start(token, accounts):
    creation_time = token.start_epoch_time()
    with brownie.reverts("dev: start > end"):
        token.mintable_in_timeframe(creation_time + 1, creation_time)


def test_mintable_in_timeframe_multiple_epochs(token, accounts):
    creation_time = token.start_epoch_time()

    # two epochs should not raise
    token.mintable_in_timeframe(creation_time, int(creation_time + YEAR * 1.9))

    with brownie.reverts("dev: too far in future"):
        # three epochs should raise
        token.mintable_in_timeframe(creation_time, int(creation_time + YEAR * 2.1))


def test_available_supply(chain, web3, token):
    creation_time = token.start_epoch_time()
    initial_supply = token.totalSupply()
    rate = token.rate()
    chain.sleep(WEEK)
    chain.mine()

    expected = initial_supply + (chain[-1].timestamp - creation_time) * rate
    assert token.available_supply() == expected


def test_accurate_available_supply(chain, web3, token):
    creation_time = token.start_epoch_time()
    boost_start_time = creation_time + YEAR - WEEK
    initial_supply = token.totalSupply()
    rate = token.rate()
    assert rate == 0, "rate should be 0 at the begainning"
    chain.sleep(86401)
    token.update_boost_mining_parameters()
    chain.mine()
    print('just at the starts the boost period starts available_supply: ',
          token.available_supply())
    print('just at the starts the boost period starts rate: ',
          token.rate())

    new_rate = token.rate()
    assert new_rate == BOOST_RATE
    assert token.mining_epoch() == -1, "Boost Period should be -1"
    assert token.is_boosted() == True, 'Should has been boosted'
    
    # At the end of boost period
    chain.sleep(WEEK)
    chain.mine()
    print('just at the end of the boost period starts available_supply: ',
          token.available_supply() )
    print('just at the end of the boost period starts rate: ',
          token.rate() )

    expected = initial_supply + (chain[-1].timestamp - boost_start_time) * new_rate
    assert token.available_supply() == expected


    # starts normal mining, year 1
    token.update_mining_parameters()
    chain.mine()
    token_rate_epoch_0 = token.rate()
    print('year 1 available_supply: ', token.available_supply() )
    print('year 1 starts rate: ', token.rate() )

    assert token_rate_epoch_0 < BOOST_RATE
    assert token.available_supply() > 340_000_000 * 10 ** 18
    # almost 35% early boost + team distribution
    assert token.mining_epoch() == 0

    # starts next epoch, year 2
    chain.sleep(YEAR)
    chain.mine()
    token.update_mining_parameters()
    token_rate_epoch_1 = token.rate()
    print('year 2 starts available_supply: ', token.available_supply() )
    print('year 2 starts rate: ', token.rate() )
    assert token_rate_epoch_1 < token_rate_epoch_0
    assert token.mining_epoch() == 1
    assert token.available_supply() >= 340_000_000 * 10 ** 18


    # starts next epoch, year 3
    chain.sleep(YEAR)
    chain.mine()
    token.update_mining_parameters()
    token_rate_epoch_2 = token.rate()
    print('year 3 available_supply: ', token.available_supply() )
    print('year 3 starts rate: ', token.rate() )


    assert token_rate_epoch_2 < token_rate_epoch_1
    assert token.mining_epoch() == 2
    assert token.available_supply() >= 340_000_000 * 10 ** 18

    # starts next epoch, year 4
    chain.sleep(YEAR)
    chain.mine()
    token.update_mining_parameters()
    token_rate_epoch_3 = token.rate()
    print('year 4 available_supply: ', token.available_supply() )
    print('year 4 starts rate: ', token.rate() )

    assert token_rate_epoch_3 < token_rate_epoch_2
    assert token.mining_epoch() == 3
