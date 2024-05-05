// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/access/Ownable.sol";

import "./StakingRewardsAdapter.sol";

contract StakingRewardsAdapterFactory is Ownable {
    // List of adapters
    mapping(address => address[]) public adapters;

    event NewAdapter(address indexed stakingContract, address indexed adapter);

    function newAdapter(
        address _stakingContract,
        address _stakingToken,
        address _rewardsToken
    ) external onlyOwner returns (address) {
        // Deploy new adapter
        StakingRewardsAdapter adapter = new StakingRewardsAdapter(
            _stakingContract,
            _stakingToken,
            _rewardsToken
        );
        // Transfer pausership to factory owner and renounce
        adapter.addPauser(owner());
        adapter.renouncePauser();
        // Add to the list
        adapters[_stakingContract].push(address(adapter));

        emit NewAdapter(_stakingContract, address(adapter));
        return address(adapter);
    }
}
