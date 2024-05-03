// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "../handlers/HandlerBase.sol";

contract Foo5Handler is HandlerBase {
    function getContractName() public pure override returns (string memory) {
        return "Foo5Handler";
    }

    function exec(address _target, bytes memory _data)
        public
        payable
        returns (bytes memory response)
    {
		(bool ok, bytes memory ret) = _target.call{ value: msg.value }(_data);
        require(ok, string(ret));
        response = ret;
    }

    function bar() public pure returns (bool) {
        return true;
    }
}
