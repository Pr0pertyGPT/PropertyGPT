// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./interface/IRegistry.sol";

/// @notice The registry database for Furucombo
contract Registry is IRegistry, Ownable {
    mapping(address => bytes32) public override handlers;
    mapping(address => bytes32) public override callers;
    mapping(address => uint256) public override bannedAgents;
    bool public override fHalt;

    bytes32 public constant DEPRECATED = bytes10(0x64657072656361746564);

    event Registered(address indexed registration, bytes32 info);
    event Unregistered(address indexed registration);
    event CallerRegistered(address indexed registration, bytes32 info);
    event CallerUnregistered(address indexed registration);
    event Banned(address indexed agent);
    event Unbanned(address indexed agent);
    event Halted();
    event Unhalted();

    modifier isNotHalted() {
        require(fHalt == false, "Halted");
        _;
    }

    modifier isHalted() {
        require(fHalt, "Not halted");
        _;
    }

    modifier isNotBanned(address agent) {
        require(bannedAgents[agent] == 0, "Banned");
        _;
    }

    modifier isBanned(address agent) {
        require(bannedAgents[agent] != 0, "Not banned");
        _;
    }

    /**
     * @notice Register a handler with a bytes32 information.
     * @param registration Handler address.
     * @param info Info string.
     */
    function register(address registration, bytes32 info) external onlyOwner {
        require(registration != address(0), "zero address");
        require(info != DEPRECATED, "unregistered info");
        require(handlers[registration] != DEPRECATED, "unregistered");
        handlers[registration] = info;
        emit Registered(registration, info);
    }

    /**
     * @notice Unregister a handler. The handler will be deprecated.
     * @param registration The handler to be unregistered.
     */
    function unregister(address registration) external onlyOwner {
        require(registration != address(0), "zero address");
        require(handlers[registration] != bytes32(0), "no registration");
        require(handlers[registration] != DEPRECATED, "unregistered");
        handlers[registration] = DEPRECATED;
        emit Unregistered(registration);
    }

    /**
     * @notice Register a caller with a bytes32 information.
     * @param registration Caller address.
     * @param info Info string.
     * @dev Dapps that triggers callback function should be registered.
     * In this case, registration is the Dapp address and the leading 20 bytes
     * of info is the handler address.
     */
    function registerCaller(
        address registration,
        bytes32 info
    ) external onlyOwner {
        require(registration != address(0), "zero address");
        require(info != DEPRECATED, "unregistered info");
        require(callers[registration] != DEPRECATED, "unregistered");
        callers[registration] = info;
        emit CallerRegistered(registration, info);
    }

    /**
     * @notice Unregister a caller. The caller will be deprecated.
     * @param registration The caller to be unregistered.
     */
    function unregisterCaller(address registration) external onlyOwner {
        require(registration != address(0), "zero address");
        require(callers[registration] != bytes32(0), "no registration");
        require(callers[registration] != DEPRECATED, "unregistered");
        callers[registration] = DEPRECATED;
        emit CallerUnregistered(registration);
    }

    /**
     * @notice Ban agent from query
     *
     */
    function ban(address agent) external isNotBanned(agent) onlyOwner {
        bannedAgents[agent] = 1;
        emit Banned(agent);
    }

    /**
     * @notice Unban agent from query
     */
    function unban(address agent) external isBanned(agent) onlyOwner {
        bannedAgents[agent] = 0;
        emit Unbanned(agent);
    }

    /**
     * @notice Check if the handler is valid.
     * @param handler The handler to be verified.
     */
    function isValidHandler(
        address handler
    ) external view override returns (bool) {
        return handlers[handler] != 0 && handlers[handler] != DEPRECATED;
    }

    /**
     * @notice Check if the caller is valid.
     * @param caller The caller to be verified.
     */
    function isValidCaller(
        address caller
    ) external view override returns (bool) {
        return callers[caller] != 0 && callers[caller] != DEPRECATED;
    }

    function halt() external isNotHalted onlyOwner {
        fHalt = true;
        emit Halted();
    }

    function unhalt() external isHalted onlyOwner {
        fHalt = false;
        emit Unhalted();
    }
}
