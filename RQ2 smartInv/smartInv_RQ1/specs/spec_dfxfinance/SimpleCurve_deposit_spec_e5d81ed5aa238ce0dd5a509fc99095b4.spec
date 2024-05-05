pragma solidity 0.8.0;

contract SimpleCurve {mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;

function deposit(uint256) public  {}

rule DepositConservesTotalLiquidity() {
    uint256 $amount;
    uint256 totalLiquidityBefore = totalLiquidity;
    address $sender = msg.sender;

    deposit($amount);

    assert(totalLiquidity == totalLiquidityBefore + $amount);
}}