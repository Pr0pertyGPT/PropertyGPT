## BGD properties

### slashing

Implemented

- transfer amount of staked underlying to _destination_
  - check balances
  - determine that amount doesn't violate _maxSlashingPercentage_
- after slashing:
  exchangeRate_t1 = (totalStaked_t0 - amount) / totalSupply_t0
- after slashing inPostSlashingPeriod = true:
  - accounts can exit immediately without cooldown
  - no account can enter
  - no other slashing can occur

### staking

Implemented

- stkAmount_t1 = amount \* exchangeRate_t0 / 1e18

### redeeming

Implemented

- amount_t1 = amount \* 1e18 / exchangeRate_t0

### returnFunds

Implemented

- returned funds injected into the exchangeRate
- entering not possible until slashing is settled by slashingAdmin

### Governance

Not implemented

- sum of power of all accounts is eqlt to sum of all balances

- power_t0 = stkAmount_t0 \* 1e18 / exchangeRate_t0

### Airdrops

Implemented

- airdropped tokens (not through _stake_ or _returnFunds_) are not considered
  for the exchange rate, i.e. not mutualized

### Governance

Not implemented

- Sum of voting/proposition power is less or equal than sum of all balances
- delegatee of 0 is 0 (with preserve maybe)
- if count of snapshots is 0 then for all addresses their delegatee is not you
  (with ghost delegatees)
- prove t using the previous 2

### Exchange rate

Not implemented

- exchange rate is totalStaked / totalSupply

## Other properties

#### cooldown

- [v] `cooldown()` correctness: updated with block timestamp

M:

- [v] rewards getter returns the same amount of max rewards the user deserve (if the user was to withdraw max) - add actual change of balance - `rewardsGetterEquivalentClaim`
- [v] User index <= Global index - `PersonalIndexLessOrEqualGlobalIndex`
- [v] Global Index monotonically increasing - `indexesMonotonicallyIncrease`
- [v] Personal Index monotonically increasing - `indexesMonotonicallyIncrease`
- [v] previewStake returns the same share amount as actual stake - `previewStakeEquivalentStake`
- [v] previewRedeem returns the same underlying amount as actual redeem - `previewRedeemEquivalentRedeem`
- [v] totalSupply of shares GE balance of any user - `totalSupplyGreaterThanUserBalance`

- [x] Rewards monotonically increasing (except for claim methods) - `rewardsMonotonicallyIncrease` - configure changes deserved rewards retroactively
- [x] Slashing monotonically increase EXCHANGE_RATE - `slashingIncreaseExchangeRate` - fails due to down cast. assuming the ratio is not greater than 10^20
- [x] Returning funds monotonically decrease EXCHANGE_RATE - `returnFundsDecreaseExchangeRate` -
- [x] ExchangeRate never zero - see confluence + inv1, 2 and 3 - `exchangeRateNeverZero`
- [x] slashing 0 and returningFunds of 0 should be the same and same as the beginning - `slashAndReturnFundsOfZeroDoesntChangeExchangeRate`
- [x] Who decreased deserved rewards? (claim rew) - `whoDecreasedDeservedRewards` - configure decreases deserved rewards
- [x] previewRedeem of all shares <= balance of staked-token - `allSharesAreBacked` - init changes ER, slash fails because ER overflow, returnFunds fails because of ER overflow
- [x] AAVE.bal(this) >= stkAAVE.totalSupply/EXCHANGE_RATE - `allStakedAaveBacked` - init changes ER, slash fails because ER overflow, returnFunds fails because of ER overflow
