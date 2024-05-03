// SPDX-License-Identifier: GNU-3
// guard.sol -- simple whitelist implementation of DSAuthority

// Copyright (C) 2017  DappHub, LLC

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

pragma solidity >0.5.0;

import "./DSGuard.sol";

contract DSGuardFactory {
    mapping(address => bool) public isGuard;
    mapping(address => address) public guards;

    function newGuard(
        bool permitFurucombo,
        address furucombo,
        address dsProxy
    ) public returns (DSGuard guard) {
        guard = new DSGuard();
        if (permitFurucombo) {
            guard.permit(
                furucombo,
                dsProxy,
                bytes4(keccak256("execute(address,bytes)"))
            );
        }
        guard.setOwner(msg.sender);
        isGuard[address(guard)] = true;
        guards[msg.sender] = address(guard);
    }
}
