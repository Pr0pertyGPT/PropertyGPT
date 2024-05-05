pragma solidity 0.8.0;

contract VulnerableBancor {mapping(address => mapping(address => uint256)) public allowance;
mapping(address => uint256) public balanceOf;

function safeTransferFrom(address,address,address,uint256) public  {}

rule VerifyUnchangedBalanceWithSafeTransferFrom() {
    address $sender;
    address $recipient;
    uint256 $tokenId;
    address $unrelatedAccount;

    // Ensure $unrelatedAccount is neither the sender nor recipient
    __assume__($unrelatedAccount != $sender);
    __assume__($unrelatedAccount != $recipient);

    // Specify the caller of this rule
    __assume__(msg.sender == 0x0000000000000000000000000000000000000001);

    // Obtain the balance of $unrelatedAccount prior to the token transfer
    uint balanceBefore = this.balanceOf($unrelatedAccount);

    // Execute the safeTransferFrom operation without additional data, as data specification was removed for compliance
    this.safeTransferFrom($sender, $recipient, $tokenId);

    // Obtain the balance of $unrelatedAccount following the token transfer
    uint balanceAfter = this.balanceOf($unrelatedAccount);

    // Assert that $unrelatedAccount's balance remains unchanged after the token transfer
    assert(balanceBefore == balanceAfter);
}}