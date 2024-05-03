// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.8.0;
import "./DummyERC20Impl.sol";

contract DummyERC20A is DummyERC20Impl {
    // preserve proxy's balance
    function havocMe(address proxy) external {
        uint256 bal = proxy.balance;
        msg.sender.delegatecall("");
        require(bal == proxy.balance);
    }

    function havocMeEth() external {
        msg.sender.delegatecall("");
    }
}
