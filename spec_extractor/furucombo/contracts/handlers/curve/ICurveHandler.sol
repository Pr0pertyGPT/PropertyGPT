// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface ICurveHandler {
    function get_dy(
        int128 i,
        int128 j,
        uint256 dx
    ) external view returns (uint256);

    function get_dy(
        uint256 i,
        uint256 j,
        uint256 dx
    ) external view returns (uint256);

    function exchange(
        int128 i,
        int128 j,
        uint256 dx,
        uint256 min_dy
    ) external payable;

    function exchange(
        uint256 i,
        uint256 j,
        uint256 dx,
        uint256 min_dy
    ) external payable;

    function exchange(
        uint256 i,
        uint256 j,
        uint256 dx,
        uint256 min_dy,
        bool boolean // use_eth
    ) external payable;

    function get_dy_underlying(
        int128 i,
        int128 j,
        uint256 dx
    ) external view returns (uint256);

    function get_dy_underlying(
        uint256 i,
        uint256 j,
        uint256 dx
    ) external view returns (uint256);

    function exchange_underlying(
        int128 i,
        int128 j,
        uint256 dx,
        uint256 min_dy
    ) external payable;

    function exchange_underlying(
        address pool,
        int128 i,
        int128 j,
        uint256 dx,
        uint256 min_dy
    ) external payable;

    function exchange_underlying(
        uint256 i,
        uint256 j,
        uint256 dx,
        uint256 min_dy
    ) external payable;

    function exchange_underlying(
        uint256 i,
        uint256 j,
        uint256 dx,
        uint256 min_dy,
        bool boolean // use_eth
    ) external payable;

    // Curve add liquidity function only support static array
    function add_liquidity(uint256[2] calldata amounts, uint256 min_mint_amount)
        external
        payable;

    function add_liquidity(uint256[3] calldata amounts, uint256 min_mint_amount)
        external
        payable;

    function add_liquidity(uint256[4] calldata amounts, uint256 min_mint_amount)
        external
        payable;

    function add_liquidity(uint256[5] calldata amounts, uint256 min_mint_amount)
        external
        payable;

    function add_liquidity(uint256[6] calldata amounts, uint256 min_mint_amount)
        external
        payable;

    // Curve add liquidity underlying
    function add_liquidity(
        uint256[2] calldata amounts,
        uint256 min_mint_amount,
        bool boolean // use_underlying
    ) external payable;

    function add_liquidity(
        uint256[3] calldata amounts,
        uint256 min_mint_amount,
        bool boolean // use_underlying
    ) external payable;

    function add_liquidity(
        uint256[4] calldata amounts,
        uint256 min_mint_amount,
        bool boolean // use_underlying
    ) external payable;

    function add_liquidity(
        uint256[5] calldata amounts,
        uint256 min_mint_amount,
        bool boolean // use_underlying
    ) external payable;

    function add_liquidity(
        uint256[6] calldata amounts,
        uint256 min_mint_amount,
        bool boolean // use_underlying
    ) external payable;

    function calc_token_amount(uint256[2] calldata amounts, bool deposit)
        external
        view
        returns (uint256);

    function calc_token_amount(uint256[3] calldata amounts, bool deposit)
        external
        view
        returns (uint256);

    function calc_token_amount(uint256[4] calldata amounts, bool deposit)
        external
        view
        returns (uint256);

    function calc_token_amount(uint256[5] calldata amounts, bool deposit)
        external
        view
        returns (uint256);

    function calc_token_amount(uint256[6] calldata amounts, bool deposit)
        external
        view
        returns (uint256);

    // Curve add liquidity factory metapool deposit zap
    function add_liquidity(
        address pool,
        uint256[3] calldata amounts,
        uint256 min_mint_amount
    ) external payable;

    function add_liquidity(
        address pool,
        uint256[4] calldata amounts,
        uint256 min_mint_amount
    ) external payable;

    function add_liquidity(
        address pool,
        uint256[5] calldata amounts,
        uint256 min_mint_amount
    ) external payable;

    function add_liquidity(
        address pool,
        uint256[6] calldata amounts,
        uint256 min_mint_amount
    ) external payable;

    function calc_token_amount(
        address pool,
        uint256[3] calldata amounts,
        bool deposit
    ) external view returns (uint256);

    function calc_token_amount(
        address pool,
        uint256[4] calldata amounts,
        bool deposit
    ) external view returns (uint256);

    function calc_token_amount(
        address pool,
        uint256[5] calldata amounts,
        bool deposit
    ) external view returns (uint256);

    function calc_token_amount(
        address pool,
        uint256[6] calldata amounts,
        bool deposit
    ) external view returns (uint256);

    // Curve remove liquidity
    function remove_liquidity_one_coin(
        uint256 _token_amount,
        int128 i,
        uint256 min_amount
    ) external;

    function remove_liquidity_one_coin(
        uint256 _token_amount,
        uint256 i,
        uint256 min_amount
    ) external;

    function remove_liquidity_one_coin(
        uint256 _token_amount,
        int128 i,
        uint256 min_uamount,
        bool boolean // donate_dust or use_underlying
    ) external;

    function remove_liquidity_one_coin(
        uint256 _token_amount,
        uint256 i,
        uint256 min_uamount,
        bool boolean
    ) external;

    // Curve remove liquidity factory metapool deposit zap
    function remove_liquidity_one_coin(
        address pool,
        uint256 _token_amount,
        int128 i,
        uint256 min_amount
    ) external;

    function calc_withdraw_one_coin(uint256 _token_amount, int128 i)
        external
        view
        returns (uint256);

    function calc_withdraw_one_coin(uint256 _token_amount, uint256 i)
        external
        view
        returns (uint256);

    // Curve factory metapool deposit zap
    function calc_withdraw_one_coin(
        address pool,
        uint256 _token_amount,
        int128 i
    ) external view returns (uint256);
}
