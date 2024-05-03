
all result in 
[SmartInvRQ1 -3-.xlsx](assets/SmartInvRQ1%20-3-.xlsx)




26 of the 60 security events in smartInv's RQ1 were scanned
Here is the translation of the summary of your research results into English:

### Research Results Summary

1. **Undetected Attacks:**
   - There were 9 events where corresponding attacks were not found. This includes projects like sherlockYields, moneyReserve, and pancakeswap, where vulnerabilities may not have been disclosed publicly or detailed attack information could not be obtained due to other reasons.

2. **Reentrancy Attacks:**
   - The table indicates that 11 events were identified as having reentrancy vulnerabilities. These can be preliminarily identified through static analysis engines and require specific attack contracts to support, thus no specific specifications were generated to handle them.

3. **Price Manipulation:**
   - A total of 8 events involve price manipulation. Vulnerabilities in these projects may involve strategies to manipulate market prices, which are generally difficult to identify using standard security tools in DeFi projects.

4. **Other Special Types of Attacks:**
   - Cross-chain selector collision attacks (e.g., polynetwork) are difficult to identify with regular scanning tools due to their complexity.
   - Vulnerabilities in projects like LIFI and Qubit are also difficult to simulate and analyze with automation tools due to their complexity.

5. **Code Not Provided:**
   - Two projects (beanStalk and Meter) could not provide code, which poses obstacles for in-depth security analysis.
   - The contracts for two projects were too complex to provide complete code.

### Scannable Projects
In the security scanning of smart contracts, a total of 26 projects' contracts were scannable. To improve compilation compatibility and scanning efficiency:

1. The contract versions of 2 projects were upgraded to Solidity 0.6.12.
2. The attacked contract code for 14 projects was simplified.
3. 8 projects used the original versions of the attacked contract codes for scanning.

After these preparations, we tested these contracts using the verification tool, prover, to confirm whether the scan could effectively identify the actual vulnerabilities.

To ensure the practicality of the results and simulate real-world application scenarios, we selected only the top two highest scoring results (top1 and top2) from each project for evaluation. This selection is based on conventional practices in actual usage scenarios, where only the top two most likely results are usually considered to optimize resource allocation and response time.

Scanning Results: TP:19 FP:7

| Detectable with CVE knowledge | 1 |
| ----------------------------- | - |
| Failure exists, but not the corresponding vulnerability | 2 |
| Failure exists, but not the corresponding vulnerability, as it requires a malicious factory contract environment | 1 |
| Failure exists, detected the vulnerability | 10 |
| Not detected, possibly due to requiring a uniswap environment | 1 |
| Not detected, possibly due to requiring multi-signature generation | 1 |
| Not detected, possibly due to needing an environment involving e-DAI | 1 |
| Not detected, possibly due to requiring an external contract environment (malicious token) | 1 |
| Detectable with added knowledge | 8 |

|Project|Loss(\$)|Property count|Generation Total Time|Generation Average Time|
| ----- | ----- | ----- | ----- | ----- |
|dfxFinance|4000000|8|235.075|29.384375|
|AnySwap|1400000|11|517.891|47.081|
|Dodo|700000|17|1182.109|69.53582353|
|Bancor|545000|19|1948.071|102.5300526|
|BeautyChain|900000000|5|104.228|20.8456|
|Melo|90000|9|252.001|28.00011111|
|BGLD|18000|9|229.278|25.47533333|
|GYMNetwork|2000000|21|273.816|13.03885714|
|elasticSwap|845000|37|1136.311|30.71110811|
|EulerFinance|200000000|23|376.019|16.34865217|
|monoSwap|31000000|5|68.855|13.771|
|nimBus|5241|32|4287.841|133.9950313|
|VTF|50000|8|357.85|44.73125|
|Nomad|152000000|14|589.542|42.11014286|
|Umbrella|700000|14|403.704|28.836|
|Fortress Loan|3000000|2|70.53|35.265|
|ShadowFinance|300000|25|551.369|22.05476|
|Revest|\-|4|74.542|18.6355|
|Cartel|\-|11|400.7|36.42727273|
|sushiSwap|3300000|10|418.994|41.8994|
|ChainSwap|8000000|9|307.161|34.129|
|Ragnarok|44000|42|1890.451|45.0107381|
|templeDao|2300000|13|302.409|23.26223077|
|BabySwap|\-|33|1841.951|55.81669697|
|DFX|4000000|8|235.075|29.384375|
|MonoX|31000000|5|68.855|13.771|

Three new pieces of knowledge:

They are applicable to init, owner-related operations and access control are applicable, and any public function access control is applicable.

Strategy: Triggered when the function name is related to init, triggered when the operation within the function is related to owner, triggered by public function

```Plain Text
def get_owner_related_function_example(): # Suitable for access control related to owner operations
    return """rule EnsureOwnershipTransferOnlyByOwner() {
        __assume__(msg.sender == 0x0000000000000000000000000000000000000001);
        address $initialOwner = owner;
        owned();
        assert(owner == msg.sender);

        __assume__(msg.sender == 0x0000000000000000000000000000000000000002);
        owned();
        assert(owner == $initialOwner);
    }
}"""

def get_owner_based_contract_example(): # Suitable for access control of any public function
    return """rule OnlyOwnerCanCallDepositFromOtherContract() {
        address $owner;
        address $nonOwner;
        uint256 $depositAmount;
        address $depositAddress;

        // Assume $owner is the contract owner
        __assume__(owner == 0x0000000000000000000000000000000000000001);
        // Assume $msgSender is a non-owner
        __assume__(msg.sender == 0x0000000000000000000000000000000000000002);
        assert(owner != msg.sender)

        // Capture the state before and after the call to depositFromOtherContract function
        uint256 balanceBefore = balances[$depositAddress];
        depositFromOtherContract($depositAmount, $depositAddress);
        uint256 balanceAfter = balances[$depositAddress];

        // Assertion: Calling from a non-owner should not change the balance
        assert(balanceBefore == balanceAfter);
    }"""

def get_init_related_example(): # Suitable for initialization
    return """rule InitializeFunctionCanBeCalledOnlyOnce() {
        address $initCaller;
        // Assume parameter values
        uint256 $initialParam1;
        uint256 $initialParam2;

        // Assume $msgSender is the initial caller
        __assume__(msg.sender, $initCaller);

        // First call to init function
        init($initialParam1, $initialParam2);

        // Attempting a second call to init function, possibly with different parameters
        uint256 $secondParam1 = $initialParam1 + 1;
        uint256 $secondParam2 = $initialParam2 + 1;

        // Capture the critical state variables before and after the second call to init
        bool initCalledBefore = isInitialized;
        init($secondParam1, $secondParam2);
        bool initCalledAfter = isInitialized;

        // Assertion: The second call to init should not change the initialization state
        assert(initCalledBefore == true);
        assert(initCalledAfter == true);
        // Assertion: None of the critical state variables should change after the second call
        assert(param1 == $initialParam1);
        assert(param2 == $initialParam2);
    }"""

```
# Time data
[SmartInvRQ1 -3- -1-.xlsx](assets/SmartInvRQ1%20-3-%20-1-.xlsx)




|Project|Property count(include compile failed)|Total Time|Generation Average Time|Verification count|Verification Total Time|Verification Average Time|
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
|dfxFinance|8|235.075|29.384375|7|7|1|
|AnySwap|11|517.891|47.081|7|7|1|
|Dodo|10|1182.109|118.2109|9|19|2.11|
|Bancor|19|1948.071|102.5300526|10|9|0.9|
|BeautyChain|5|104.228|20.8456|5|9|1.8|
|Melo|10|515.032|51.5032|10|8|0.8|
|BGLD|9|229.278|25.47533333|9|39|4.33|
|GYMNetwork|21|273.816|13.03885714|20|71|3.55|
|elasticSwap|37|1136.311|30.71110811|34|120|3.53|
|EulerFinance|23|376.019|16.34865217|21|43|2.05|
|monoSwap|29|470.132|16.21144828|6|12|2|
|nimBus|32|4287.841|133.9950313|15|30|2|
|VTF|8|357.85|44.73125|7|21|3|
|Nomad|14|589.542|42.11014286|14|70|5|
|Umbrella|14|403.704|28.836|9|25|2.78|
|Fortress Loan|2|70.53|35.265|2|5|2.5|
|ShadowFinance|25|551.369|22.05476|23|80|3.48|
|Revest|4|74.542|18.6355|4|10|2.5|
|Cartel|11|400.7|36.42727273|9|20|2.22|
|sushiSwap|10|418.994|41.8994|5|20|4|
|ChainSwap|9|307.161|34.129|9|25|2.78|
|Ragnarok|42|1890.451|45.0107381|33|88|2.67|
|templeDao|13|302.409|23.26223077|11|30|2.73|
|BabySwap|33|1841.951|55.81669697|24|50|2.08|

|dfxFinance|2|0|7|5|0|
| ----- | ----- | ----- | ----- | ----- | ----- |
|AnySwap|0|2| |0|5|
|Dodo|0|2|New knowledge can be detected|5|0|
|Bancor|2|0| |5|0|
|BeautyChain|2|0| |5|0|
|Melo|0|2|New knowledge can be detected|5|0|
|BGLD|0|2| |0|5|
|GYMNetwork|0|2|New knowledge can be detected|5|0|
|elasticSwap|1|1| |4|1|
|EulerFinance|0|2| |0|5|
|monoSwap|0|2|New knowledge can be detected|5|0|
|nimBus|2|0| |3|2|
|VFT(应为VTF)|0|2| |0|5|
|Nomad|1|1| |4|1|
|Umbrella|1|1| |4|1|
|Fortress Loan|0|2|New knowledge can be detected|5|0|
|ShadowFinance|0|2|New knowledge can be detected|5|0|
|Revest|1|1| |4|1|
|Cartel|2|0| |5|0|
|sushiSwap|0|2| |0|5|
|ChainSwap|0|2| |0|5|
|Ragnarok|0|2|Existing knowledge can be detected rule EnsureTransferOwnershipSecurity() {<br> address \$newOwner;  <br> // Test with assumed owner<br> \_\_assume\_\_(msg.sender == 0x0000000000000000000000000000000000000001);<br> address \$initialOwner = \_owner;<br> transferOwnership(\$newOwner);<br> // Check if the ownership actually transferred to new owner<br> assert(\_owner == \$newOwner);  <br> // Reset owner to initial for next test<br> \_owner = \$initialOwner;  <br> // Test with non-owner<br> \_\_assume\_\_(msg.sender == 0x0000000000000000000000000000000000000002);<br> transferOwnership(\$newOwner);<br> // Check if the ownership remains unchanged when called by non-owner<br> assert(\_owner == \$initialOwner);<br>}|5|0|
|templeDao|0|2|New knowledge can be detected|5|0|
|BabySwap|0|2| |0|5|

