// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "../handlers/HandlerBase.sol";

interface IFoo3 {
    function bar1() external;

    function bar2() external;

    function reset1() external;

    function reset2() external;
}

contract Foo3Handler is HandlerBase {
    using LibStack for bytes32[];
    
    function getContractName() public pure override returns (string memory) {
        return "Foo3Handler";
    }

    function bar1(address foo) public payable {
        IFoo3 target = IFoo3(foo);
        target.bar1();

        // Update post process
        bytes32[] memory params = new bytes32[](1);
        params[0] = bytes32(uint256(uint160(foo)));
        _updatePostProcess(params);
    }

    function bar2(address foo) public payable {
        IFoo3 target = IFoo3(foo);
        target.bar2();

        // Update post process
        bytes32[] memory params = new bytes32[](1);
        params[0] = bytes32(uint256(uint160(foo)));
        _updatePostProcess(params);
    }

    function postProcess() external payable override {
        bytes4 sig = stack.getSig();
        if (sig == bytes4(keccak256(bytes("bar1(address)")))) {
            address foo = stack.getAddress();
            IFoo3 target = IFoo3(foo);
            target.reset1();
        } else if (sig == bytes4(keccak256(bytes("bar2(address)")))) {
            address foo = stack.getAddress();
            IFoo3 target = IFoo3(foo);
            target.reset2();
        } else revert("Invalid post process");
    }
}
