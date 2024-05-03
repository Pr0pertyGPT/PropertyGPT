// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

contract Foo3 {
    uint256 public num;

    constructor() {
        num = 10;
    }

    function bar1() public {
        num = 11;
    }

    function reset1() public {
        num = 1;
    }

    function bar2() public {
        num = 12;
    }

    function reset2() public {
        num = 2;
    }
}
