// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "./MerkleRedeem.sol";

/**
 * @title The staking contract for Furucombo
 */
contract Staking is Ownable, Pausable, ReentrancyGuard {
    
    using SafeERC20 for IERC20;

    IERC20 public stakingToken;
    // The redeem contract location of claiming functions
    MerkleRedeem public redeemable;

    mapping(address => uint256) private _balances;
    mapping(address => mapping(address => bool)) private _approvals;

    event Staked(
        address indexed sender,
        address indexed onBehalfOf,
        uint256 amount
    );
    event Unstaked(
        address indexed sender,
        address indexed onBehalfOf,
        uint256 amount
    );
    event Approved(address indexed user, address indexed agent, bool approval);

    modifier onlyApproved(address owner) {
        require(
            _approvals[owner][msg.sender],
            "Furucombo staking: agent is not approved"
        );
        _;
    }

    /**
     * @notice The redeem contract owner will be transferred to the deployer.
     */
    constructor(address _stakingToken, address _rewardToken) {
        stakingToken = IERC20(_stakingToken);
        redeemable = new MerkleRedeem(_rewardToken);
        redeemable.transferOwnership(msg.sender);
    }

    /**
     * @notice Verify if the agent is approved by user. Approval is required to
     * perform `unstakeFor`.
     * @param user The user address.
     * @param agent The agent address to be verified.
     */
    function isApproved(address user, address agent)
        external
        view
        returns (bool)
    {
        return _approvals[user][agent];
    }

    /**
     * @notice Check the staked balance of user.
     * @param user The user address.
     * @return The staked balance.
     */
    function balanceOf(address user) external view returns (uint256) {
        return _balances[user];
    }

    /**
     * @notice Set the approval for agent.
     * @param agent The agent to be approved/disapproved.
     * @param approval The approval.
     */
    function setApproval(address agent, bool approval) external {
        require(agent != address(0), "Furucombo staking: agent is 0");
        require(
            _approvals[msg.sender][agent] != approval,
            "Furucombo staking: identical approval assigned"
        );
        _approvals[msg.sender][agent] = approval;
        emit Approved(msg.sender, agent, approval);
    }

    /**
     * @notice The staking function.
     * @param amount The amount to be staked.
     */
    function stake(uint256 amount) external nonReentrant whenNotPaused {
        _stakeInternal(msg.sender, amount);
    }

    /**
     * @notice The delegate staking function.
     * @param onBehalfOf The address to be staked.
     * @param amount The amount to be staked.
     */
    function stakeFor(address onBehalfOf, uint256 amount)
        external
        nonReentrant
        whenNotPaused
    {
        _stakeInternal(onBehalfOf, amount);
    }

    /**
     * @notice The unstaking function.
     * @param amount The amount to be staked.
     */
    function unstake(uint256 amount) external nonReentrant {
        _unstakeInternal(msg.sender, amount);
    }

    /**
     * @notice The delegate staking function. Approval is required. The
     * unstaked balance will be transferred to the caller.
     * @param onBehalfOf The address to be staked.
     * @param amount The amount to be staked.
     */
    function unstakeFor(address onBehalfOf, uint256 amount)
        external
        nonReentrant
        onlyApproved(onBehalfOf)
    {
        _unstakeInternal(onBehalfOf, amount);
    }

    /**
     * @notice The claiming function. The function call is forwarded to the
     * redeem contract.
     */
    function claimWeek(
        address user,
        uint256 week,
        uint256 balance,
        bytes32[] memory merkleProof
    ) public {
        redeemable.claimWeek(user, week, balance, merkleProof);
    }

    /**
     * @notice The claiming function. The function call is forwarded to the
     * redeem contract.
     */
    function claimWeeks(address user, MerkleRedeem.Claim[] memory claims)
        public
    {
        redeemable.claimWeeks(user, claims);
    }

    function _stakeInternal(address user, uint256 amount) internal {
        require(amount > 0, "Furucombo staking: staking 0");
        _balances[user] = _balances[user] + amount;
        stakingToken.safeTransferFrom(msg.sender, address(this), amount);
        emit Staked(msg.sender, user, amount);
    }

    function _unstakeInternal(address user, uint256 amount) internal {
        require(amount > 0, "Furucombo staking: unstaking 0");
        _balances[user] = _balances[user] - amount;
        stakingToken.safeTransfer(msg.sender, amount);
        emit Unstaked(msg.sender, user, amount);
    }
}
