import "./SafeMath.sol";
import "./Receiver.sol";

/**
 * Dummy WETH token.
 */
contract DummyWeth {
    using SafeMath for uint256;
    uint256 supply;
    
    mapping(address => uint256) balances;
    mapping(address => mapping(address => uint256)) allowances;

    string public name;
    string public symbol;
    uint public decimals;

    function totalSupply() external view returns (uint256) {
        return supply;
    }

    function balanceOf(address account) external view returns (uint256) {
        return balances[account];
    }

    function transfer(address recipient, uint256 amount) external returns (bool) {
        balances[msg.sender] = balances[msg.sender].sub(amount);
        balances[recipient] = balances[recipient].add(amount);
        return true;
    }

    function allowance(address owner, address spender) external view returns (uint256) {
        return allowances[owner][spender];
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowances[msg.sender][spender] = amount;
        return true;
    }

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool) {
        balances[sender] = balances[sender].sub(amount);
        balances[recipient] = balances[recipient].add(amount);
        allowances[sender][msg.sender] = allowances[sender][msg.sender].sub(amount);
        return true;
    }
    
    // WETH
    function deposit() external payable {
        // assume succeeds
        supply = supply.add(msg.value);
        balances[msg.sender] = balances[msg.sender].add(msg.value);
    }

    function withdraw(uint256 amount) external {
        supply = supply.sub(amount);
        balances[msg.sender] = balances[msg.sender].sub(amount);
        require (Receiver(payable(msg.sender)).acceptEth{value:amount}());
    }
}