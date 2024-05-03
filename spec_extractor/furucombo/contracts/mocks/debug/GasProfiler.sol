// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

contract GasProfiler {
    // keccak256 hash of "gas.profiler.base"
    // prettier-ignore
    bytes32 private constant GAS_BASE = 0x37698e52cd5639897dae03c485a7870bceb6876f0e950fc063664398d5580c0c;

    event DeltaGas(bytes32 tag, int256 gas);
    event GetGas(bytes32 tag, uint256 gas);

    constructor() {
        _setBase();
    }

    function _setBase() internal {
        bytes32 slot = GAS_BASE;
        assembly {
            sstore(slot, sub(gas(), 5005))
        }
    }

    function _getBase() internal view returns (uint256 base) {
        bytes32 slot = GAS_BASE;
        assembly {
            base := sub(sload(slot), 203)
        }
    }

    function _deltaGas(bytes32 tag) internal {
        emit DeltaGas(tag, int256(_getBase()) - int256(gasleft()));
        _setBase();
    }

    function _getGas(bytes32 tag) internal {
        emit GetGas(tag, _getBase());
        _setBase();
    }
}
