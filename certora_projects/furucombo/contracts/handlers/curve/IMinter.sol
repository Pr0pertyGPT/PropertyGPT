// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface IMinter {
    function allowed_to_mint_for(address addr, address _for) external view returns (bool);

    function mint(address gauge_addr) external;
    function mint_for(address gauge_addr, address _for) external;
    function toggle_approve_mint(address minting_user) external;
}
