certoraRun certora/harness/StakedAaveV3Harness.sol \
    certora/harness/DummyERC20Impl.sol \
    certora/harness/RewardVault.sol \
    --link StakedAaveV3Harness:STAKED_TOKEN=DummyERC20Impl \
    --link StakedAaveV3Harness:REWARD_TOKEN=DummyERC20Impl \
    --link StakedAaveV3Harness:REWARDS_VAULT=RewardVault \
    --verify StakedAaveV3Harness:certora/specs/allProps.spec \
    --solc solc8.17 \
    --cloud \
    --optimistic_loop \
    --loop_iter 3 \
    --rules "${@}" \
    --settings -t=600 \
    --msg "Props"
