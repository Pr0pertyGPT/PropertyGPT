// SPDX-License-Identifier: MIT

// File: @openzeppelin/contracts/access/Roles.sol

/**
 * @title Roles
 * @dev Library for managing addresses assigned to a Role.
 */
library Roles {
    struct Role {
        mapping(address => bool) bearer;
    }

    /**
     * @dev Give an account access to this role.
     */
    function add(Role storage role, address account) internal {
        require(!has(role, account), "Roles: account already has role");
        role.bearer[account] = true;
    }

    /**
     * @dev Remove an account's access to this role.
     */
    function remove(Role storage role, address account) internal {
        require(has(role, account), "Roles: account does not have role");
        role.bearer[account] = false;
    }

    /**
     * @dev Check if an account has this role.
     * @return bool
     */
    function has(
        Role storage role,
        address account
    ) internal view returns (bool) {
        require(account != address(0), "Roles: account is the zero address");
        return role.bearer[account];
    }
}

// File: @openzeppelin/contracts/access/roles/PauserRole.sol

contract PauserRole is Context {
    using Roles for Roles.Role;

    event PauserAdded(address indexed account);
    event PauserRemoved(address indexed account);

    Roles.Role private _pausers;

    constructor() {
        _addPauser(_msgSender());
    }

    modifier onlyPauser() {
        require(
            isPauser(_msgSender()),
            "PauserRole: caller does not have the Pauser role"
        );
        _;
    }

    function isPauser(address account) public view returns (bool) {
        return _pausers.has(account);
    }

    function addPauser(address account) public onlyPauser {
        _addPauser(account);
    }

    function renouncePauser() public {
        _removePauser(_msgSender());
    }

    function _addPauser(address account) internal {
        _pausers.add(account);
        emit PauserAdded(account);
    }

    function _removePauser(address account) internal {
        _pausers.remove(account);
        emit PauserRemoved(account);
    }
}

// File: @openzeppelin/contracts/lifecycle/Pausable.sol

/**
 * @dev Contract module which allows children to implement an emergency stop
 * mechanism that can be triggered by an authorized account.
 *
 * This module is used through inheritance. It will make available the
 * modifiers `whenNotPaused` and `whenPaused`, which can be applied to
 * the functions of your contract. Note that they will not be pausable by
 * simply including this module, only once the modifiers are put in place.
 */
contract Pausable is Context, PauserRole {
    /**
     * @dev Emitted when the pause is triggered by a pauser (`account`).
     */
    event Paused(address account);

    /**
     * @dev Emitted when the pause is lifted by a pauser (`account`).
     */
    event Unpaused(address account);

    bool private _paused;

    /**
     * @dev Initializes the contract in unpaused state. Assigns the Pauser role
     * to the deployer.
     */
    constructor() {
        _paused = false;
    }

    /**
     * @dev Returns true if the contract is paused, and false otherwise.
     */
    function paused() public view returns (bool) {
        return _paused;
    }

    /**
     * @dev Modifier to make a function callable only when the contract is not paused.
     */
    modifier whenNotPaused() {
        require(!_paused, "Pausable: paused");
        _;
    }

    /**
     * @dev Modifier to make a function callable only when the contract is paused.
     */
    modifier whenPaused() {
        require(_paused, "Pausable: not paused");
        _;
    }

    /**
     * @dev Called by a pauser to pause, triggers stopped state.
     */
    function pause() public onlyPauser whenNotPaused {
        _paused = true;
        emit Paused(_msgSender());
    }

    /**
     * @dev Called by a pauser to unpause, returns to normal state.
     */
    function unpause() public onlyPauser whenPaused {
        _paused = false;
        emit Unpaused(_msgSender());
    }
}

// File: contracts/staking/StakingRewardsAdapter.sol

pragma solidity 0.8.10;

import "@openzeppelin/contracts/utils/Context.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

import "./IStakingRewards.sol";
import "./IStakingRewardsAdapter.sol";

contract StakingRewardsAdapter is
    IStakingRewardsAdapter,
    ReentrancyGuard,
    Pausable
{
    using SafeERC20 for IERC20;

    /* ========== STATE VARIABLES ========== */

    IStakingRewards public stakingContract;
    IERC20 public override rewardsToken;
    IERC20 public override stakingToken;
    uint256 public lastUpdateTime;
    uint256 public rewardPerTokenStored;

    mapping(address => uint256) public userRewardPerTokenPaid;
    mapping(address => uint256) public rewards;

    uint256 private _totalSupply;
    mapping(address => uint256) private _balances;
    mapping(address => mapping(address => bool)) private _approvals;

    /* ========== CONSTRUCTOR ========== */

    constructor(
        address _stakingContract,
        address _stakingToken,
        address _rewardsToken
    ) {
        stakingContract = IStakingRewards(_stakingContract);
        if (_stakingToken == address(0) && _rewardsToken == address(0)) {
            stakingToken = stakingContract.stakingToken();
            rewardsToken = stakingContract.rewardsToken();
        } else {
            stakingToken = IERC20(_stakingToken);
            rewardsToken = IERC20(_rewardsToken);
        }
    }

    /* ========== VIEWS ========== */

    function totalSupply() external view override returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(
        address account
    ) external view override returns (uint256) {
        return _balances[account];
    }

    function lastTimeRewardApplicable() public view override returns (uint256) {
        return stakingContract.lastTimeRewardApplicable();
    }

    function rewardPerToken() public view override returns (uint256) {
        return stakingContract.rewardPerToken();
    }

    function earned(address account) public view override returns (uint256) {
        return
            ((_balances[account] *
                (rewardPerToken() - userRewardPerTokenPaid[account])) / 1e18) +
            rewards[account];
    }

    function getRewardForDuration() external view override returns (uint256) {
        return stakingContract.getRewardForDuration();
    }

    function rewardRate() external view override returns (uint256) {
        return stakingContract.rewardRate();
    }

    function isApproved(
        address owner,
        address agent
    ) public view override returns (bool) {
        return _approvals[owner][agent];
    }

    /* ========== MODIFIERS ========== */

    modifier updateReward(address account) {
        rewardPerTokenStored = rewardPerToken();
        lastUpdateTime = lastTimeRewardApplicable();
        if (account != address(0)) {
            rewards[account] = earned(account);
            userRewardPerTokenPaid[account] = rewardPerTokenStored;
        }
        _;
    }

    modifier onlyApproved(address owner) {
        require(
            isApproved(owner, msg.sender),
            "StakingRewardsAdapter: agent not been approved"
        );
        _;
    }

    /* ========== APPROVAL ========== */

    function setApproval(address agent, bool approval) external override {
        require(
            agent != address(0),
            "StakingRewardsAdapter: approve to the zero address"
        );
        require(
            _approvals[msg.sender][agent] != approval,
            "StakingRewardsAdapter: approval should be different to current"
        );

        _approvals[msg.sender][agent] = approval;
        emit Approval(msg.sender, agent, approval);
    }

    /* ========== SELF_OPERATE FUNCTIONS ========== */

    function stake(
        uint256 amount
    ) external override nonReentrant whenNotPaused updateReward(msg.sender) {
        _stakeInternal(msg.sender, amount);
    }

    function withdraw(
        uint256 amount
    ) public override nonReentrant updateReward(msg.sender) {
        _withdrawInternal(msg.sender, amount);
    }

    function getReward() public override nonReentrant updateReward(msg.sender) {
        _getRewardInternal(msg.sender);
    }

    function exit() external override {
        withdraw(_balances[msg.sender]);
        getReward();
    }

    /* ========== RESTRICTED OPERATE_FOR FUNCTIONS ========== */

    function stakeFor(
        address account,
        uint256 amount
    ) external override nonReentrant whenNotPaused updateReward(account) {
        _stakeInternal(account, amount);
    }

    function withdrawFor(
        address account,
        uint256 amount
    ) public override nonReentrant onlyApproved(account) updateReward(account) {
        _withdrawInternal(account, amount);
    }

    function getRewardFor(
        address account
    ) public override nonReentrant onlyApproved(account) updateReward(account) {
        _getRewardInternal(account);
    }

    function exitFor(address account) external override onlyApproved(account) {
        withdrawFor(account, _balances[account]);
        getRewardFor(account);
    }

    /* ========== INTERNAL FUNCTIONS ========== */

    function _stakeInternal(address account, uint256 amount) internal {
        require(amount > 0, "StakingRewardsAdapter: cannot stake 0");
        _totalSupply = _totalSupply + amount;
        _balances[account] = _balances[account] + amount;
        stakingToken.safeTransferFrom(msg.sender, address(this), amount);
        stakingToken.safeApprove(address(stakingContract), amount);
        stakingContract.stake(amount);
        stakingToken.safeApprove(address(stakingContract), 0);
        emit Staked(msg.sender, account, amount);
    }

    function _withdrawInternal(address account, uint256 amount) internal {
        require(amount > 0, "StakingRewardsAdapter: cannot withdraw 0");
        _totalSupply = _totalSupply - amount;
        _balances[account] = _balances[account] - amount;
        stakingContract.withdraw(amount);
        stakingToken.safeTransfer(msg.sender, amount);
        emit Withdrawn(msg.sender, account, amount);
    }

    function _getRewardInternal(address account) internal {
        uint256 reward = rewards[account];
        if (reward > 0) {
            rewards[account] = 0;
            uint256 rewardBalance = rewardsToken.balanceOf(address(this));
            if (reward > rewardBalance) {
                stakingContract.getReward();
            }
            rewardsToken.safeTransfer(msg.sender, reward);
            emit ClaimedReward(msg.sender, account, reward);
        }
    }

    /* ========== EVENTS ========== */

    event Staked(
        address indexed sender,
        address indexed onBehalfOf,
        uint256 amount
    );
    event Withdrawn(
        address indexed sender,
        address indexed onBehalfOf,
        uint256 amount
    );
    event ClaimedReward(
        address indexed sender,
        address indexed onBehalfOf,
        uint256 amount
    );
    event Approval(address indexed owner, address indexed agent, bool approval);
}
