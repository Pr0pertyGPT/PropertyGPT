// SPDX-License-Identifier: MIT
pragma solidity 0.8.10;

import "../rules/RuleBase.sol";

contract RuleMock2 is RuleBase {
    uint256 public constant override DISCOUNT = (BASE * 80) / 100;

    function verify(address usr) public view override returns (bool) {
        return usr.balance >= 10 ether;
    }

    function calDiscount(address usr) external view override returns (uint256) {
        return verify(usr) ? DISCOUNT : BASE;
    }
}
