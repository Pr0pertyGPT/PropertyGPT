pragma solidity ^0.4.13;

contract SimplifiedDoftcoin { 
    string public name = "Doftcoin"; // Name for display purposes
    string public symbol = "DFC"; // Symbol for display purposes
    uint256 public decimals = 18; // Amount of decimals for display purposes
    uint256 public totalSupply; // Stores the total token supply
    mapping (address => uint256) public balanceOf; // Keeps track of token balances

    address public owner; // Owner of the contract

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Mint(address indexed target, uint256 mintedAmount);

    // Modifier to restrict functions to the owner
    modifier onlyOwner {
        require(msg.sender == owner, "Only the owner can call this function.");
        _;
    }

    constructor() {
        owner = msg.sender; // Sets the creator as the owner
        totalSupply = 5000000 * (10 ** decimals); // Sets the total supply
        balanceOf[msg.sender] = totalSupply; // Assigns the entire supply to the owner
        emit Transfer(0x0, msg.sender, totalSupply); // Emits a transfer event for the initial supply
    }

    // Function to mint new tokens
    function mintToken(address _target, uint256 _mintedAmount) public onlyOwner {
        require(_target != address(0), "Cannot mint to the 0x0 address.");
        totalSupply += _mintedAmount; // Increases the total supply
        balanceOf[_target] += _mintedAmount; // Adds the amount to the target's balance
        emit Mint(_target, _mintedAmount); // Emits a mint event
        emit Transfer(0x0, _target, _mintedAmount); // Emits a transfer event
    }
}
