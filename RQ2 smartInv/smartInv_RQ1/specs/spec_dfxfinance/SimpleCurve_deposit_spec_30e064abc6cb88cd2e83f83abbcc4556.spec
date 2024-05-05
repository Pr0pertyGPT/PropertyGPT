pragma solidity 0.8.0;

contract SimpleCurve {mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;

function deposit(uint256) public  {}

rule DepositIncreasesBalancesAndTotalLiquidity() {
    uint256 $amount;
    address $depositor = msg.sender;
    uint256 initialBalanceDepositor = balances[$depositor];
    uint256 initialBalanceContract = balances[address(this)];
    uint256 initialTotalLiquidity = totalLiquidity;

    deposit($amount);

    assert(balances[$depositor] == initialBalanceDepositor + $amount);
    assert(balances[address(this)] == initialBalanceContract + $amount);
    assert(totalLiquidity == initialTotalLiquidity + $amount);
}}