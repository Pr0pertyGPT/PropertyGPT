// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "../Proxy.sol";
import "../Config.sol";
import "./debug/GasProfiler.sol";
import "./debug/IHandlerEvents.sol";
import "../lib/LibFeeStorage.sol";

contract ProxyMock is Proxy, GasProfiler, IHandlerEvents {
    using LibStack for bytes32[];
    using LibFeeStorage for mapping(bytes32 => bytes32);

    constructor(
        address registry,
        address feeRuleRegistry
    ) Proxy(registry, feeRuleRegistry) {}

    event RecordHandlerResult(bytes value);

    function execMock(
        address to,
        bytes memory data
    ) external payable returns (bytes memory result) {
        uint256[] memory rules = new uint256[](0);
        _preProcess(rules);
        _setBase();
        result = _exec(to, data, 0);
        _setPostProcess(to);
        _deltaGas("Gas");
        _postProcess();
        emit RecordHandlerResult(result);
        return result;
    }

    function _preProcess(uint256[] memory _rules) internal override {
        // Set the sender.
        _setSender();
        // Set the fee collector
        cache._setFeeCollector(feeRuleRegistry.feeCollector());
        // Calculate fee
        uint256 feeRate = feeRuleRegistry.calFeeRateMulti(_getSender(), _rules);
        cache._setFeeRate(feeRate);
    }

    function updateTokenMock(address token) public {
        stack.setAddress(token);
    }

    function setHandlerType(Config.HandlerType handlerType) public {
        stack.setHandlerType(handlerType);
    }

    function setPostProcess(
        address to,
        bytes4 sig,
        bytes32[] memory params
    ) public {
        for (uint256 i = params.length; i > 0; i--) {
            stack.set(params[i - 1]);
        }
        stack.set(sig);
        stack.setAddress(to);
        stack.setHandlerType(HandlerType.Custom);
    }
}
