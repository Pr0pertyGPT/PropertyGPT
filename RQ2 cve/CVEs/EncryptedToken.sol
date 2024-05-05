pragma solidity ^0.4.16;

contract SimplifiedEncryptedToken {
    address public owner;
    uint256 public totalSupply;
    uint256 public buyPrice;
    mapping (address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    // 构造函数
    function SimplifiedEncryptToken(uint256 initialSupply, string tokenName, string tokenSymbol) public {
        owner = msg.sender;
        totalSupply = initialSupply * 10 ** uint256(18);  
        balanceOf[msg.sender] = totalSupply;                
        // name = tokenName;  // 未使用的变量可以移除
        // symbol = tokenSymbol;  // 未使用的变量可以移除
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function _transfer(address _from, address _to, uint _value) internal {
        require(_to != 0x0);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value >= balanceOf[_to]); // 溢出检查
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
    }

    // 设置新的购买价格
    function setPrices(uint256 newBuyPrice) onlyOwner public {
        buyPrice = newBuyPrice;
    }

    // 测试函数
    function test() payable public {
        uint amount = msg.value * buyPrice; // 计算数量
        _transfer(owner, msg.sender, amount);
        owner.transfer(msg.value); // 发送以太币到所有者
    }

    // 转移所有权
    function transferOwnership(address newOwner) onlyOwner public {
        owner = newOwner;
    }

    // 允许接收以太币
    function() payable public {}
}
