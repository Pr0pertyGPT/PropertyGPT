// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;
import "./Foo.sol";

contract FooFactory {
    mapping(uint256 => address) private _foos;
    uint256 private _nFoo;

    constructor() {
        _nFoo = 0;
        createFoo();
    }

    function addressOf(uint256 index) public view returns (address foo) {
        require(index < _nFoo);
        return _foos[index];
    }

    function createFoo() public {
        Foo f = new Foo();
        _foos[_nFoo] = address(f);
        _nFoo++;
    }
}
