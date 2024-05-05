

# Overall Summary
| Project | Number of Findings | Confirmed | Fixed | Hits | Bounty |
| ------- | ------------------ | --------- | ----- | ---- | ------ |
| Loxodrome | 10 | 4 | 4 | 1 Medium Solo Finding | $750 |
| ZKLink Nova | 2 | 2 | 2 | 1 Critical Solo Finding<br>1 Medium Solo Finding | $4788 |
| ZKLink Bridge | 7 | 3 | 3 | 1 Medium Finding | $1500 |
| Aki Protocol | 3 | 1 | 1 | 1 Critical Finding | $1218 |

Let me know if you need further assistance!

# Loxodrome
original result

The data here is in excel, please check excel

Check fail res

|Function Name|Failure Description|
| ----- | ----- |
|DepositTokenNotOwnedBySenderFails|Assertion for deposited token ownership fails|
|DepositTokenNotAlreadyStaked|Assertion for token already being staked fails|
|testDepositFunctionOwnerAndStakeStatus|Assertion for token ownership and staking status fails|
|ValidateTokenStakingConditions|Assertion checks for token staking conditions fail|
|CheckNFTOwnershipBeforeStake|Assertion for token ownership before staking fails|
|depositTokenNotAlreadyStaked|Assertion checks for token staking status fail|
|EnsureTokenStakeConditions|Assertion checks for token staking conditions fail|
|DepositTokenOwnershipAndStakingStatus|Assertion checks for token ownership and staking status fail|
|ValidateDepositTokenOwnershipAndStakingStatus|Assertion checks for validating token ownership and staking status fail|
|validateDepositFunctionality|Assertion checks for validating deposit functionality fail|

## report
https://github.com/Secure3Audit/Secure3Academy/tree/main/audit\_reports//Loxodrome

## vul
In the deposit function, the return value of nft.transferfrom is not checked.

## Overall results
Medium 1/3

No low risk

The remaining two items in medium are centralized issue and intent design issue.

## propertyGPT check results
The data here is in excel, please check excel

1. The assertion of DepositTokenOwnershipAndStakedStatus rule `assert(userInfo[$msgSender].amount == $userAmountBefore + 1);` failed, indicating that after staking, the amount of the staker (\$msgSender) did not increase correctly by 1.
2. The assertion `assert(nftToken.ownerOf($tokenId) == $user);` of the DepositTokenOwnershipAndStakingStatus rule fails, indicating that the owner of the NFT is not the user (\$user) after staking.
3. Assertion of validateDepositFunctionality rule

```Plain Text
assert(balanceAfter == 
    balanceBefore + 1); 
    // User's amount should increase by 1
```
```Plain Text
assert(tokenStakedBefore == false && 
    tokenStakedAfter == true); 
    // Token's staked status should be updated from false to true
```
```Plain Text
assert(tokenOwnerBefore != $depositor && 
    tokenOwnerAfter == $depositor); 
    // Token's ownership should be updated to depositor
```
Failure indicates that the NFT ownership was not correctly transferred to the staker (msg.sender) after staking. And it shows that after staking, the amount of the pledger (\$msgSender) did not increase correctly by 1.

4. The assertion `assert(tokenOwnerBefore != msg.sender && tokenOwnerAfter == msg.sender);` of the ValidateTokenStakingConditions rule failed, indicating that the NFT ownership was not correctly transferred to the pledger (msg.sender) after staking.

## analysis
In summary, it shows that vulnerability 1: During the deposit process, after pledging, that is, the result after NFT.transferfrom is not checked correctly, that is, there is an unused return value vulnerability.

# ZKLink Nova
rank 1/5

The bounty is US$4,788, and the only critical one has been found

## report
https://github.com/Secure3Audit/Secure3Academy/tree/main/audit\_reports//zklink\_L3


## Result analysis
The only critical vulnerability was discovered using propertyGPT

### Specific details of the vulnerability
https://github.com/Secure3Audit/code\_zklink\_L3/blob/main/code/contracts/ZkLink.sol#L408-L419

### Vulnerability description
The `withdrawForwardFee` function in the smart contract contains a critical vulnerability that allows validators to withdraw more than their allocated share of forwarding fees, potentially leading to unfair distributions and loss of funds. This function lacks a crucial check to ensure that each validator can only withdraw their rightful share based on the total amount of fees collected and their contribution.

The vulnerability arises from the function’s failure to track and limit individual validators’ withdrawals according to their proportionate share. The function calculates the new total withdrawn fee by simply adding the requested withdrawal amount (`_amount`) to `totalValidatorForwardFeeWithdrawn`, without considering the requesting validator’s entitled share. The only check performed is against the total collected forwarding fees (`totalValidatorForwardFee`), ensuring that the new total withdrawn does not exceed this amount. However, this does not prevent individual validators from withdrawing more than their share.

### Vulnerability code
```Plain Text
function withdrawForwardFee(uint256 _amount) external nonReentrant onlyValidator {
 require(_amount > 0, "Invalid amount");
 uint256 newWithdrawnFee = 
    totalValidatorForwardFeeWithdrawn + 
    _amount;
 require(totalValidatorForwardFee >= 
    newWithdrawnFee, "Withdraw exceed");

 totalValidatorForwardFeeWithdrawn = 
    newWithdrawnFee;
 (bool success, ) = msg.sender.call{value: _amount}("");
 require(success, "Withdraw failed");
 emit WithdrawForwardFee(_amount);
}
```
### Generated spec
```Plain Text
pragma solidity 0.8.0;

contract SimplifiedStandaloneZkLink {address private _owner;
mapping(address => bool) private _validators;
uint256 public totalValidatorForwardFee;
uint256 public totalValidatorForwardFeeWithdrawn;

function withdrawForwardFee(uint256) public  {}
rule EnsureValidatorWithdrawConstraintsValid() {
    address $validatorAddr;
    uint256 $withdrawAmount;
    uint256 $validatorInitialWithdrawn;
    uint256 $initialTotalValidatorForwardFee;
    require(_validators[$validatorAddr], "Not validator");
    require($withdrawAmount > 0, "Invalid amount");
    uint256 newWithdrawnFee = 
        $validatorInitialWithdrawn + $withdrawAmount;
    require($initialTotalValidatorForwardFee >=
        newWithdrawnFee, "Withdraw exceed");

    if (msg.sender == $validatorAddr) {
        withdrawForwardFee($withdrawAmount);
        assert(totalValidatorForwardFeeWithdrawn + 
            $withdrawAmount == 
            newWithdrawnFee);        
        // Assuming successful withdraw updates the totalValidatorForwardFeeWithdrawn
        assert(totalValidatorForwardFee - 
            totalValidatorForwardFeeWithdrawn == 
            $initialTotalValidatorForwardFee - 
            newWithdrawnFee);
    }
}}
```
### spec analysis
spec mainly verifies and asserts the part where failure occurs:

```Plain Text
assert(totalValidatorForwardFeeWithdrawn + 
    $withdrawAmount == 
    newWithdrawnFee);
```
```Plain Text
assert(totalValidatorForwardFee - 
    totalValidatorForwardFeeWithdrawn == 
    $initialTotalValidatorForwardFee - 
    newWithdrawnFee);
    }
```
In the context of the `rule EnsureValidatorWithdrawConstraintsValid()` function mentioned in the smart contract `SimplifiedStandaloneZkLink`, there are two `assert` statements used to verify the correctness of the withdrawal logic. If these two `assert` statements trigger errors during symbolic execution, this indicates that in some cases the contract's logic may not behave as expected, potentially revealing a potential vulnerability. Let's analyze these two assertions and their possible violations.

#### First assertion
```Plain Text
assert(totalValidatorForwardFeeWithdrawn + 
    $withdrawAmount == 
    newWithdrawnFee);
```
The purpose of this assertion is to confirm that after performing a withdrawal operation, the recorded `totalValidatorForwardFeeWithdrawn` (the total amount that all validators have withdrawn so far) plus the current withdrawal amount `$withdrawAmount` is indeed equal to the calculated new total amount withdrawn` newWithdrawnFee`. If this assertion fails, possible reasons include:

1. **Update**`**totalValidatorForwardFeeWithdrawn**`\*\*Previous errors\*\*: If an error occurs before the `totalValidatorForwardFeeWithdrawn` variable is actually updated, or the update logic itself is wrong, then the new There may be problems with the calculation of the total withdrawal amount.
2. **Variable initialization error**: `$validatorInitialWithdrawn` (the validator’s initial withdrawal amount) or `$withdrawAmount` (this withdrawal amount) may not be initialized or updated correctly, resulting in inaccurate calculation of `newWithdrawnFee`.

#### The second assertion
```Plain Text
assert(totalValidatorForwardFee - 
    totalValidatorForwardFeeWithdrawn == 
    $initialTotalValidatorForwardFee - 
    newWithdrawnFee);
```
This assertion checks that the total forward fees remaining after the withdrawal is as expected. Specifically, it verifies that the total forward fee before the withdrawal minus the total amount withdrawn before the withdrawal equals the corresponding value after the withdrawal. If this assertion fails, it may be because:

1. **Withdrawal logic affects other state variables**: For example, if `totalValidatorForwardFee` or `totalValidatorForwardFeeWithdrawn` is modified in an unexpected way during the withdrawal process, this assertion may fail.
2. **Variable synchronization issue**: The values of `$initialTotalValidatorForwardFee` and `newWithdrawnFee` need to accurately reflect the status before and after the withdrawal operation. If the values of these variables are incorrect, the assertion may fail.

#### Is there any vulnerability?
These assertion failures point to potential logic errors or state inconsistencies that could lead to unfair withdrawal operations or fund security issues. Specifically, if a contract allows validators to withdraw more than their fair share, or if the updated state incorrectly reflects the contract's funds flow, this can be considered a vulnerability.

Taken together, these assertion failures suggest the following potential vulnerabilities:

* Second assertion: **Inconsistent status update**: causing `totalValidatorForwardFeeWithdrawn` or `totalValidatorForwardFee` to be out of sync with the actual withdrawal operation.
* First assertion: **Incorrect amount calculation**: Possibly due to a calculation error in the withdrawal logic, a validator is allowed to withdraw more than its fair share.

### Vulnerability analysis process
Based on judgment:

* **Incorrect amount calculation**: Possibly due to a calculation error in the withdrawal logic, a validator is allowed to withdraw more than its fair share.

Specific explanation:

"Incorrect amount calculation: Possibly due to a calculation error in the withdrawal logic, a validator is allowed to withdraw more than its fair share" This issue is mainly related to the first assertion:

```Plain Text
assert(totalValidatorForwardFeeWithdrawn + 
    $withdrawAmount == 
    newWithdrawnFee);
```
The purpose of this assertion is to ensure that the total amount recorded in `totalValidatorForwardFeeWithdrawn` plus the amount of the current withdrawal request `$withdrawAmount` is equal to the expected new total amount `newWithdrawnFee`. If this assertion fails, a possible explanation is that the withdrawal logic does not correctly calculate or limit the amount each validator can withdraw based on their share.

In a sound withdrawal logic, one needs to ensure that each validator can only withdraw their fair share. If the calculation of `newWithdrawnFee` simply adds the current withdrawal amount to the previous total withdrawal amount, without taking into account each validator's proportional share, then it may be possible to allow validators to withdraw more than their share. . In this case, although the assertion of `totalValidatorForwardFeeWithdrawn + $withdrawAmount == newWithdrawnFee` is mathematically true, in essence it does not ensure that the withdrawal operation follows the constraints of each validator's share, resulting in the "wrong amount" calculate".

In other words, this assertion failure may not directly indicate that the validator withdrew more than its fair share, but it does expose that the contract was not designed to implement additional checks to prevent this from happening. If there is no corresponding logic in other parts of the contract to restrict each validator from withdrawing according to his or her share, then this will be a design flaw that may allow validators to withdraw more than their share.

### Original spec knowledge used
Reference spec does not seem to have much to do with the generated spec, but gpt analyzed the scenario considerations related to the generated spec.

```Plain Text
rule getCLMFees_LEQ_ATokenBAL_RW(method f) filtered {f ->
        !harnessOnlyMethods(f) &&
        !f.isView &&
        (is_withdraw_method(f) || is_redeem_method(f) ||
         f.selector == 
            withdrawFees(address,uint256).selector
        )
}
```
analysis of gpt

```Plain Text
This specification code (or rule) is part of a smart contract that is used to verify security or correctness, especially when performing automated analysis using formal verification tools such as symbolic execution tools or static analysis tools. This particular rule is intended to be filtered and applied to a specific set of functions to verify that they meet certain conditions or properties during execution. Let’s break down this rule step by step:

- **Rule name**: `getCLMFees_LEQ_ATokenBAL_RW`. The name usually gives some hint as to the purpose of the rule or what is being checked. A possible meaning here is to verify some logic related to fees (`CLMFees`) and token balances (`ATokenBAL`), specifically verifying that fees are less than or equal to a certain token balance, where `LEQ` may stand for "less than or equal to (Less or Equal)", `RW` may indicate that this is a rule involving a function that reads and writes state.

- **Rule target** (`method f`): This defines the target to which the rule will be applied, i.e. the function (`f`) in the contract.

- **Filter conditions** (`filtered {f -> ...}`): This part is a filter that defines which functions will be checked by this rule. The conditions are as follows:
   - `!harnessOnlyMethods(f)`: Exclude methods used only in the test framework or validation framework.
   - `!f.isView`: Exclude functions marked as `view`. The `view` function does not modify the contract status, it is only used to read the status.
   - `is_withdraw_method(f) || is_redeem_method(f) || f.selector == withdrawFees(address,uint256).selector`: Select the target function, either a withdrawal method, a redemption method, or a specific function signature` withdrawFees(address,uint256)` function. `selector` is the unique identifier of the function and is used for EVM calls.

**Verification Purpose of the Rule**: Combined with the rule name and filter, this rule appears to be designed to verify that functions involving the movement of funds (such as withdrawals, exchanges, or specific fee withdrawal functions) adhere to certain token balance-related financial constraints. Although the specific logic of the rules (i.e. the conditions or properties that should be met) is not directly shown in this code, from the context and name, a possible validation goal is to ensure that when performing these operations, the associated fees do not exceed the account's Token balance, or ensuring that the post-operation state meets certain financial health metrics.
```
### spec other data
spec ranks second in code natural language similarity among generated results, and ranks first in result prediction scores.

The data here is in excel, please check excel

### v platform prover execution results
https://v.meta001.net/groundtruth/a85f73eb-8db9-4b2f-a96b-4bafb2569978/task/abc32290-0001-469b-bc4e-845d0c5875d0



### ~~Medium risk~~
Detection ratio: 1/2

#### Unverified length
The data here is in excel, please check excel

#### Generated rule

```Plain Text
rule ValidateMessageAndCorrectAccessFor_parseL2WithdrawalMessage() {
    // Assume the caller is the authorized one
    __assume__(msg.sender == 0x0000000000000000000000000000000000000001);

    // Testing with invalid message length
    uint256 invalidLength = 60; // Not the expected 56 or 108 lengths
    bytes memory messageInvalidLength = new bytes(invalidLength);
    for(uint i = 0; i < invalidLength; i++) {
        messageInvalidLength[i] = 
            bytes1(uint8(i % 256));
    }   greate spec！
    // This should fail due to incorrect message length
    _parseL2WithdrawalMessage(messageInvalidLength);

    // Testing with a valid message length of 108
    uint256 validLength108 = 108;
    bytes memory messageValidLength = new bytes(validLength108);
    for(uint i = 0; i < validLength108; i++) {
        messageValidLength[i] = 
            bytes1(uint8(i % 256));
    }
    // This is expected to pass as it satisfies the length requirement
    _parseL2WithdrawalMessage(messageValidLength);

    // Assume the caller is not the authorized one and should fail due to access control
    __assume__(msg.sender != 
        0x0000000000000000000000000000000000000001);
    _parseL2WithdrawalMessage(messageValidLength); // This should fail due to access control

    // Setup and test for return values with a valid message expecting to succeed
    uint256 expectedLength = 108;
    bytes memory messageExpectedLength = new bytes(expectedLength);
    for(uint i = 0; i < expectedLength; i++) {
        messageExpectedLength[i] = 
            bytes1(uint8(i % 256));
    }
    address l1Gateway;
    uint256 amount;
    address l1Receiver;
    // Assuming the caller is authorized again for positive test case
    __assume__(msg.sender == 
        0x0000000000000000000000000000000000000001);
    (l1Gateway, amount, l1Receiver) = 
        _parseL2WithdrawalMessage(messageExpectedLength);
    // Here, you would compare the returned values with expected ones if specific values were expected
}
```
#### The actual running spec is used for testing
Take the key part

The key is **\_parseL2WithdrawalMessage(messageInvalidLength); the rule is executed successfully after annotation, but the rule execution fails after recovery**

```Plain Text
rule ValidateMessageAndCorrectAccessFor_parseL2WithdrawalMessage() {
 // Assume the caller is the authorized one
 __assume__(msg.sender == 
    0x0000000000000000000000000000000000000001);

 // Testing with invalid message length
 uint256 invalidLength = 60; // Not the expected 56 or 108 lengths
 bytes memory messageInvalidLength = 
    new bytes(invalidLength);
 for(uint i = 0; i < invalidLength; i++) {
 messageInvalidLength[i] = 
    bytes1(uint8(i % 256));
 }
 // This should fail due to incorrect message length
 _parseL2WithdrawalMessage(messageInvalidLength);
 }


```
# ZKLink Bridge
## Audit Report
### Original results
The data here is in excel, please check excel

https://github.com/Secure3Audit/Secure3Academy/blob/main/audit\_reports/zkLinkNova/zkLink%20Nova%20Bridge%20Update\_Secure3\_Audit\_Report.pdf

1/1 medium

The data here is in excel, please check excel

Assertion failure

|assert(IERC20Upgradeable(\$\_l2Token).allowance(address(this), address(MERGE\_TOKEN\_PORTAL)) == allowBeforeApprove + \$\_amount);|
| ----- |
|assert(\$postApproval >= \$preApproval + \$amount);|
|assert(IERC20Upgradeable(\$l2Token).allowance(address(this), address(MERGE\_TOKEN\_PORTAL)) == allowanceBefore + \$amount);|

## Original contract
```Plain Text
contract SimplifiedL2ERC20Bridge {
    IMergeTokenPortal public immutable MERGE_TOKEN_PORTAL;

    constructor(IMergeTokenPortal _mergeTokenPortal) {
        MERGE_TOKEN_PORTAL = _mergeTokenPortal;
    }

    function depositToMerge(address _l2Token, uint256 _amount, address _l2Receiver) external {
        require(msg.sender == address(this), "Only bridge can call this function");
        IL2StandardToken(_l2Token).bridgeMint(address(this), _amount);
        IERC20Upgradeable(_l2Token).safeApprove(address(MERGE_TOKEN_PORTAL), _amount);
        MERGE_TOKEN_PORTAL.deposit(_l2Token, _amount, _l2Receiver);
    }
}
```
## Three Assertion failure explanations
1. Assert: `assert(IERC20Upgradeable($_l2Token).allowance(address(this), address(MERGE_TOKEN_PORTAL)) == allowBeforeApprove + $_amount);`
2. Meaning: This assertion checks whether the authorization amount of the contract address for `MERGE_TOKEN_PORTAL` is correctly increased by `$_amount` after calling `depositToMerge`. A failed assertion indicates that the authorization increase did not perform as expected.
3. Assert: `assert($postApproval >= $preApproval + $amount);`
4. Meaning: Similar to the first assertion, this also verifies whether the authorization amount increases as expected. This assertion uses an inequality sign, which means that in some implementations the entitlement may increase more than expected (if there were previously unused entitlements). A failed assertion indicates that the authorization operation did not proceed as expected.
5. Assert: `assert(IERC20Upgradeable($l2Token).allowance(address(this), address(MERGE_TOKEN_PORTAL)) == allowanceBefore + $amount);`
6. Meaning: This assertion directly checks whether the authorization of `$l2Token` to `MERGE_TOKEN_PORTAL` is accurately increased by `$amount` after the `depositToMerge` operation. A failed assertion means that the authorization operation did not modify the authorization amount as expected.

## Key details
**The safeApprove operation in the depositToMerge function does not increase the allowance correctly**

## Vulnerability description
This vulnerability is due to the design of the SafeERC20.safeApprove() function. The safeApprove() function reverts the transaction when trying to change a non-zero approval amount to another non-zero approval amount.

In the context of the MERGE\_TOKEN\_PORTAL contract, if the user already has any non-zero approval amounts, then any attempt to change these approval amounts will cause the transaction to rollback. This situation may cause a form of denial of service (DoS), preventing users from successfully modifying their approval limits.

Similar issues have been reported in the Sherlock Audit Contest, indicating the seriousness and importance of solving this problem.

The recommended solution is to use the safeIncreaseAllowance and safeDecreaseAllowance functions instead of safeApprove(). This prevents potential denial of service issues by avoiding rollbacks when changing approval limits.

#AkiProtocol
Reports: https://github.com/Secure3Audit/Secure3Academy/tree/main/audit\_reports/Aki

1/1 Critical

## Vulnerability content
The addEnvelop function does not impose unique restrictions on envelopeID. An attacker can overwrite all previous envelopes by entering the same envelopeID.

1. Function: `addEnvelope` The purpose of the function is to add a new envelope to the smart contract. Each envelope contains a hashed Merkle root (`hashedMerkleRoot`), a bit array size (`bitarraySize`), an ERC721 contract address (`erc721ContractAddress`) and a set of token IDs (`tokenIDs`).
2. Vulnerability description: When adding a new envelope, this function uses the envelope ID (`envelopeID`) as the key to store the envelope data in the map (`idToEnvelopes`). This mapping associates envelope IDs with envelope data. However, the function does not check whether the newly provided envelope ID already exists in the map. Therefore, if an attacker calls this function again with an already existing envelope ID, they can overwrite the already stored envelope data.
3. Risk consequences: Overwriting existing envelope data may cause the following problems:
4. Data loss: The data in the original envelope will be overwritten by the data in the new envelope, resulting in loss of the original data.
5. Security risk: If an attacker controls the envelope ID, they can manipulate or block the envelope's normal use by overwriting its contents.
6. Asset risk: Tokens (such as NFT) associated with the envelope may be transferred or locked incorrectly, affecting the correct ownership of the assets.
```Plain Text
function addEnvelope(
    string calldata envelopeID,
    bytes32 hashedMerkleRoot,
    uint32 bitarraySize,
    address erc721ContractAddress,
    uint256[] calldata tokenIDs
) public {
    require(tokenIDs.length > 0, "Trying to create an empty envelope!");

    MerkleEnvelopeERC721 storage envelope = 
        idToEnvelopes[envelopeID]; 未做unique限制，出现了覆写
    envelope.creator = msg.sender;
    envelope.unclaimedPasswords = 
        hashedMerkleRoot;
    envelope.isPasswordClaimed = 
        new uint8[](bitarraySize / 8 + 1);
    envelope.tokenAddress = 
        erc721ContractAddress;
    envelope.tokenIDs = tokenIDs;

    for (uint8 tokenIdx = 0; tokenIdx < tokenIDs.length; tokenIdx++) {
        _transfer(msg.sender, address(this), tokenIDs[tokenIdx]);
    }
}
```
## result
The data here is in excel, please check excel

## spec analysis
### spec3
There is no assertion failure in this spec. The reason is that the scene settings before the attack are insufficient, but it is the closest to the vulnerability:

```Plain Text
This rule verifies that the sender and creator are set correctly when the add envelope function is called, and that the envelope does not exist before adding it.
```
```Plain Text
rule checkAddEnvelopeCorrectSenderAndCreator() {
  __assume__(msg.sender == 
    0x0000000000000000000000000000000000000001);
  string memory envelopeID = 
    "uniqueID";
  bytes32 hashedMerkleRoot = 
    0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef;
  uint32 bitarraySize = 128;
  address erc721ContractAddress = 
    0x0000000000000000000000000000000000000002;
  uint256[] memory tokenIDs = 
    new uint256[](1);
  tokenIDs[0] = 12345;

  MerkleEnvelopeERC721 storage envelopeBefore = 
    idToEnvelopes[envelopeID];
  bool existsBefore = 
    (envelopeBefore.creator != 
        address(0));

  addEnvelope(envelopeID, hashedMerkleRoot, bitarraySize, erc721ContractAddress, tokenIDs);

  MerkleEnvelopeERC721 storage envelopeAfter = 
    idToEnvelopes[envelopeID];
  bool correctlyAdded = 
    (envelopeAfter.creator == 
    msg.sender);
  bool notExistsBefore = 
    !existsBefore;

  assert(correctlyAdded && notExistsBefore);
}
```
1. Set the caller address: Assume that the caller's address is fixed to a specific value (such as `0x0000000000000000000000000000000000000001`).
2. Initialize test data: set envelope ID, hash root, bit array size, ERC721 contract address and token ID.
3. Check the pre-creation state: confirm that the envelope ID was not used before calling `addEnvelope`.

\*\*

```Plain Text
(The logic of setting another envlope was missing before this step, causing envelopeBefore.creator to be address (0), which should not actually be address (0))
```
\*\*

4. Execute the function: call the `addEnvelope` function to add a new envelope.
5. Verify the result: Confirm that the envelope was created correctly and that the creator is the default caller.

