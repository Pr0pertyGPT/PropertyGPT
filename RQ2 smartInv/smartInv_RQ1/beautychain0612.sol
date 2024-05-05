pragma solidity 0.6.12;

/**
 * @title Simplified Vulnerable Batch Transfer Contract
 * @dev Simulates an arithmetic overflow vulnerability in single token transfer
 */
contract VulnerableBatchTransfer {
    mapping(address => uint256) public balances;

    constructor() public {
        balances[msg.sender] = 10000;
    }

    // Change from handling an array of receivers to a single receiver
    function transfer(address _receiver, uint256 _value) public returns (bool) {
        require(balances[msg.sender] >= _value, "Insufficient balance");
        require(_receiver != address(0), "Cannot send to zero address");

        balances[msg.sender] -= _value;
        balances[_receiver] += _value;

        return true;
    }
    
    function balanceOf(address _owner) public view returns (uint256) {
        return balances[_owner];
    }
}
