// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "../handlers/HandlerBase.sol";

interface IFoo2 {
    function bar() external payable returns (uint256 result);
}

interface IFoo2Factory {
    function addressOf(uint256 index) external view returns (address result);

    function createFoo() external;
}

contract Foo2Handler is HandlerBase {
    address public immutable factory;
    constructor(address factory_) {
        factory = factory_;
    }

    function getContractName() public pure override returns (string memory) {
        return "Foo2Handler";
    }

    function getFooFactory() public view returns (address target) {
        return factory;
    }

    function getFoo(uint256 index) public view returns (address target) {
        return IFoo2Factory(getFooFactory()).addressOf(index);
    }

    function bar(uint256 value, uint256 index)
        public
        payable
        returns (uint256 result)
    {
        address target = getFoo(index);
        _updateToken(target);
        return IFoo2(target).bar{value: value}();
    }
}
