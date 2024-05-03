// SPDX-License-Identifier: MIT
/// This is inspired by and based on CompoundBasicProxy.sol by DeFi Saver
/// reference: https://etherscan.io/address/0x336b3919a10ced553c75db18cd285335b8e8ed38#code

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

import "./IComptroller.sol";
import "./ICToken.sol";
import "./ICEther.sol";

contract FCompoundActions {
    // prettier-ignore
    address public constant ETH_ADDR = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;
    // prettier-ignore
    address public constant CETH_ADDR = 0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5;
    // prettier-ignore
    address public constant COMPTROLLER_ADDR = 0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B;

    using SafeERC20 for IERC20;

    /// @notice User deposits tokens to the DSProxy
    /// @dev User needs to approve the DSProxy to pull the _tokenAddr tokens
    /// @param _tokenAddr The address of the token to be deposited
    /// @param _amount Amount of tokens to be deposited
    function deposit(address _tokenAddr, uint256 _amount) public {
        IERC20(_tokenAddr).safeTransferFrom(msg.sender, address(this), _amount);
    }

    /// @notice User withdraws tokens from the DSProxy
    /// @param _tokenAddr The address of the token to be withdrawn
    /// @param _amount Amount of tokens to be withdrawn
    function withdraw(address _tokenAddr, uint256 _amount) public {
        if (_tokenAddr == ETH_ADDR) {
            payable(msg.sender).transfer(_amount);
        } else {
            IERC20(_tokenAddr).safeTransfer(msg.sender, _amount);
        }
    }

    /// @notice DSProxy borrows tokens from the Compound protocol
    /// @param _cTokenAddr CTokens to be borrowed
    /// @param _amount Amount of tokens to be borrowed
    function borrow(address _cTokenAddr, uint256 _amount) public {
        require(
            ICToken(_cTokenAddr).borrow(_amount) == 0,
            "FCompoundActions: borrow failed"
        );
    }

    /// @dev User needs to approve the DSProxy to pull the _tokenAddr tokens
    /// @notice User paybacks tokens to the Compound protocol
    /// @param _cTokenAddr CTokens to be paybacked
    /// @param _amount Amount of tokens to be payedback
    function repayBorrow(address _cTokenAddr, uint256 _amount) public payable {
        uint256 debt = ICToken(_cTokenAddr).borrowBalanceCurrent(address(this));
        // If given `_amount` is greater than current debt, set `_amount` to current debt otherwise repay will fail
        if (_amount > debt) {
            _amount = debt;
        }

        if (_cTokenAddr == CETH_ADDR) {
            uint256 ethReceived = msg.value;
            ICEther(_cTokenAddr).repayBorrow{value: _amount}();
            // send back the extra eth
            if (ethReceived > _amount) {
                payable(msg.sender).transfer(ethReceived - _amount);
            }
        } else {
            IERC20 token = IERC20(ICToken(_cTokenAddr).underlying());
            token.safeTransferFrom(msg.sender, address(this), _amount);
            if (token.allowance(address(this), _cTokenAddr) < _amount) {
                token.approve(_cTokenAddr, _amount);
            }
            require(
                ICToken(_cTokenAddr).repayBorrow(_amount) == 0,
                "FCompoundActions: repay token failed"
            );
            if (msg.value > 0) payable(msg.sender).transfer(msg.value);
        }
    }

    /// @notice Enters the Compound market so it can be used as collateral
    /// @param _cTokenAddr CToken address of the token
    function enterMarket(address _cTokenAddr) public {
        address[] memory markets = new address[](1);
        markets[0] = _cTokenAddr;
        enterMarkets(markets);
    }

    /// @notice Enters the Compound market so these token can be used as collateral
    /// @param _cTokenAddrs CToken address array to enter market
    function enterMarkets(address[] memory _cTokenAddrs) public {
        uint256[] memory errors = IComptroller(COMPTROLLER_ADDR).enterMarkets(
            _cTokenAddrs
        );
        for (uint256 i = 0; i < errors.length; i++) {
            require(errors[i] == 0, "FCompoundActions: enter markets failed");
        }
    }

    /// @notice Exits the Compound market so it can't be deposited/borrowed
    /// @param _cTokenAddr CToken address of the token
    function exitMarket(address _cTokenAddr) public {
        require(
            IComptroller(COMPTROLLER_ADDR).exitMarket(_cTokenAddr) == 0,
            "FCompoundActions: exit market failed"
        );
    }
}
