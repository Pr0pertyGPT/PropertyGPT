// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "../maker/HMaker.sol";

contract HBProtocol is HMaker {
    using SafeERC20 for IERC20;

    function getContractName() public pure override returns (string memory) {
        return "HBProtocol";
    }

    function getProxyActions() public pure override returns (address) {
        return 0x351626387B5bb5408f97F8fD6B2EC415Efc9E6a1;
    }

    function getCdpManager() public pure override returns (address) {
        return 0x3f30c2381CD8B917Dd96EB2f1A4F96D91324BBed;
    }
}
