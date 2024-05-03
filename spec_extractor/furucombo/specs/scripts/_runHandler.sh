#!/bin/bash
function usage {
    echo "_runHandler.sh HANDLER_NAME CONTAINING_DIR SPEC_FILE_PATH [UNROLL_FACTOR]"
    exit 1
}

if [ -z "$1" ] 
then
    echo "Missing handler name"
    usage
fi

if [ -z "$2" ] 
then
    echo "Missing containing directory name"
    usage
fi

if [ -z "$3" ] 
then
    echo "Missing spec file path"
    usage
fi

if [ -z "$4" ]
then
    B=2
else
    B=$4
fi

handler=$1
dir=$2
spec=$3

handler_file=contracts/handlers/${dir}/${handler}.sol

perl -0777 -i -pe 's/function _revertMsg\(string memory functionName, string memory reason\)\s*internal/function _revertMsg\(string memory functionName, string memory reason\) virtual internal/g' contracts/handlers/HandlerBase.sol
perl -0777 -i -pe 's/is HandlerBase(, [a-zA-Z0-9]+)* \{/is   HandlerBase\1 {
    function getSlot\(uint s\) external view returns \(uint x\) {
        assembly { x := sload\(s\) }
    }

    function getStackLengthSlot\(\) external view returns \(uint x\) {
        assembly { x := stack_slot }
    }

    function getStackLength\(\) external view returns \(uint\) { return stack.length; }

    function getSender\(\) public view returns \(address\) { return \_getSender\(\); }
    function getCubeCounter\(\) public view returns \(uint256\) { return \_getCubeCounter\(\); }

    function ethBalance\(address who\) external view returns \(uint\) {
        return who.balance;
    }

    \/\/ to distinguish handlers from proxy
    function isHandler\(\) public view returns \(bool\) { return true; }

    function _revertMsg(string memory functionName, string memory reason)
        internal override
        view {
            revert();
        }

/g' ${handler_file}
perl -0777 -i -pe 's/SafeERC20.sol/ERC20.sol/g' ${handler_file}
perl -0777 -i -pe 's/safeA/a/g' ${handler_file}
perl -0777 -i -pe 's/safeT/t/g' ${handler_file}
perl -0777 -i -pe 's/address public constant /address public /g' ${handler_file}
perl -0777 -i -pe 's/address private constant /address public /g' ${handler_file}
perl -0777 -i -pe 's/public constant /public /g' ${handler_file}
perl -0777 -i -pe 's/private constant /public /g' ${handler_file}
perl -0777 -i -pe 's/address payable public constant / address payable public /g' ${handler_file}
perl -0777 -i -pe 's/dsProxyPayable.transfer\(amount\)/Nothing\(dsProxyPayable\).nop{value:amount}\(\)/g' ${handler_file}

# It is so nice when ETH_ADDRESS is uniformly defined
perl -0777 -i -pe 's/address constant ETHADDRESS/address public ETHADDRESS/g' contracts/handlers/aave/FlashLoanReceiverBase.sol
perl -0777 -i -pe 's/ETHADDRESS/ETH_ADDRESS/g' contracts/handlers/aave/FlashLoanReceiverBase.sol
perl -0777 -i -pe 's/ETHADDRESS/ETH_ADDRESS/g' contracts/handlers/aave/HAaveProtocol.sol
perl -0777 -i -pe 's/ETHADDRESS/ETH_ADDRESS/g' contracts/handlers/aavev2/HAaveProtocolV2.sol
perl -0777 -i -pe 's/_ETH_ADDRESS/ETH_ADDRESS/g' contracts/handlers/oneinchV5/HOneInchV5.sol
# Add ETH_ADDRESS getter for HGelatoV2LimitOrder
perl -0777 -i -pe 's/immutable GELATO_LIMIT_ORDER_MODULE;/immutable  GELATO_LIMIT_ORDER_MODULE;\n    address public ETH_ADDRESS = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;/g' contracts/handlers/gelatov2/HGelatoV2LimitOrder.sol

# handler specific
perl -0777 -i -pe 's/function repay\(/function unique_repay\(/g' contracts/handlers/aavev2/HAaveProtocolV2.sol
perl -0777 -i -pe 's/function claimComp\(/function unique_claimComp\(/g' contracts/handlers/compound/HSCompound.sol
perl -0777 -i -pe 's/function claimComp\(/function unique_claimComp\(/g' contracts/handlers/compound/HComptroller.sol
perl -0777 -i -pe 's/function swap\(/function unique_swap\(/g' contracts/handlers/oneinchV5/HOneInchV5.sol
perl -0777 -i -pe 's/function unoswap\(/function unique_unoswap\(/g' contracts/handlers/oneinchV5/HOneInchV5.sol
perl -0777 -i -pe 's/function withdraw\(/function unique_withdraw\(/g' contracts/handlers/wrappednativetoken/HWrappedNativeToken.sol
perl -0777 -i -pe 's/function deposit\(/function unique_deposit\(/g' contracts/handlers/wrappednativetoken/HWrappedNativeToken.sol
perl -0777 -i -pe 's/function redeemUnderlying/function unique_redeemUnderlying/g' contracts/handlers/compound/HCEther.sol
perl -0777 -i -pe 's/receiver.transfer\(amount\)/Nothing\(receiver\).nop{value:amount}\(\)/g' contracts/handlers/funds/HFunds.sol
# perl -0777 -i -pe 's/function swap\(/function unique_swap\(/g' contracts/handlers/oneinchV2/HOneInchExchange.sol
# perl -0777 -i -pe 's/function swap/function unique_swap/g' contracts/handlers/kybernetwork/HKyberNetwork.sol
# constant keyword being remove above so change pure to view
perl -0777 -i -pe 's/function _isNotNativeToken\(address token\) internal pure/function _isNotNativeToken\(address token\) internal view/g' contracts/handlers/oneinchV5/HOneInchV5.sol

# add ABIEncoderV2 to HMooniswap
# perl -0777 -i -pe 's/pragma solidity/pragma experimental ABIEncoderV2; pragma  solidity/g' contracts/handlers/mooniswap/HMooniswap.sol

# Distinguish redeem of compound and of aave
perl -0777 -i -pe 's/compound.redeem\(/compound.compoundredeem\(/g' contracts/handlers/compound/HCToken.sol
perl -0777 -i -pe 's/compound.redeem\(/compound.compoundredeem\(/g' contracts/handlers/compound/HCEther.sol
perl -0777 -i -pe 's/function redeem\(/function compoundredeem\(/g' contracts/handlers/compound/ICToken.sol
perl -0777 -i -pe 's/function redeem\(/function compoundredeem\(/g' contracts/handlers/compound/ICEther.sol

# Distinguish between withdraw of WETH and of YVault
perl -0777 -i -pe 's/yVault.withdraw\(/yVault.yvault_withdraw\(/g' contracts/handlers/yearn/HYVault.sol
perl -0777 -i -pe 's/function withdraw\(/function yvault_withdraw\(/g' contracts/handlers/yearn/IYVault.sol

certoraRun ${handler_file} contracts/Registry.sol specs/harnesses/DummyERC20A.sol specs/harnesses/DummyERC20B.sol specs/harnesses/ProxyHarness.sol specs/harnesses/Summary.sol \
    --verify ${handler}:${spec} \
    --settings -assumeUnwindCond,-b=${B},-ciMode=true \
    --cache "handler${handler}" \
    --msg "Handler ${handler}" 
