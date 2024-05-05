if (($# > 0))
then
    certoraRun certora/harness/StakedAaveV3Harness.sol \
        certora/harness/DummyERC20Impl.sol \
        --link StakedAaveV3Harness:STAKED_TOKEN=DummyERC20Impl \
        --link StakedAaveV3Harness:REWARD_TOKEN=DummyERC20Impl \
        --verify StakedAaveV3Harness:certora/specs/invariants.spec \
        --solc solc8.17 \
        --cloud \
        --optimistic_loop \
        --loop_iter 3 \
        --rules "${@}" \
        --msg "Invariants"
else
    certoraRun certora/harness/StakedAaveV3Harness.sol \
        certora/harness/DummyERC20Impl.sol \
        --link StakedAaveV3Harness:STAKED_TOKEN=DummyERC20Impl \
        --link StakedAaveV3Harness:REWARD_TOKEN=DummyERC20Impl \
        --verify StakedAaveV3Harness:certora/specs/invariants.spec \
        --solc solc8.17 \
        --cloud \
        --optimistic_loop \
        --loop_iter 3 \
        --msg "All invariants"
fi
