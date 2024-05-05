// SPDX-License-Identifier: MIT
pragma solidity 0.8.0;

contract VulnerableContract {
    address public owner;
    mapping(address => uint256) public deposits;
    uint256 public ownerOnlyValue;

    // 事件记录存款和所有者操作
    event DepositMade(address indexed depositor, uint256 amount);
    event OwnerOnlyValueChanged(uint256 newValue);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Caller is not the owner");
        _;
    }

    // 模拟存款函数，外部可直接调用
    function depositFromOtherContract(uint256 _depositAmount, address _from) external {
        require(_from != address(0), "Invalid address");
        // 存款增加到指定地址
        deposits[_from] += _depositAmount;
        emit DepositMade(_from, _depositAmount);
    }

    // 只有所有者可调用的函数
    function setOwnerOnlyValue(uint256 _value) external onlyOwner {
        ownerOnlyValue = _value;
        emit OwnerOnlyValueChanged(_value);
    }

    // 辅助函数，返回合约余额
    function getContractBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
