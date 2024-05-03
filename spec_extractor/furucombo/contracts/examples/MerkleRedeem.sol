// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract MerkleRedeem is Ownable {
    IERC20 public token;

    event Claimed(address _claimant, uint256 _balance);

    // Recorded weeks
    mapping(uint256 => bytes32) public weekMerkleRoots;
    mapping(uint256 => mapping(address => bool)) public claimed;

    constructor(address _token) {
        token = IERC20(_token);
    }

    function disburse(address _liquidityProvider, uint256 _balance) private {
        if (_balance > 0) {
            emit Claimed(_liquidityProvider, _balance);
            require(
                token.transfer(_liquidityProvider, _balance),
                "ERR_TRANSFER_FAILED"
            );
        }
    }

    function claimWeek(
        address _liquidityProvider,
        uint256 _week,
        uint256 _claimedBalance,
        bytes32[] memory _merkleProof
    ) public {
        require(!claimed[_week][_liquidityProvider]);
        require(
            verifyClaim(
                _liquidityProvider,
                _week,
                _claimedBalance,
                _merkleProof
            ),
            "Incorrect merkle proof"
        );

        claimed[_week][_liquidityProvider] = true;
        disburse(_liquidityProvider, _claimedBalance);
    }

    struct Claim {
        uint256 week;
        uint256 balance;
        bytes32[] merkleProof;
    }

    function claimWeeks(address _liquidityProvider, Claim[] memory claims)
        public
    {
        uint256 totalBalance = 0;
        Claim memory claim;
        for (uint256 i = 0; i < claims.length; i++) {
            claim = claims[i];

            require(!claimed[claim.week][_liquidityProvider]);
            require(
                verifyClaim(
                    _liquidityProvider,
                    claim.week,
                    claim.balance,
                    claim.merkleProof
                ),
                "Incorrect merkle proof"
            );

            totalBalance += claim.balance;
            claimed[claim.week][_liquidityProvider] = true;
        }
        disburse(_liquidityProvider, totalBalance);
    }

    function claimStatus(
        address _liquidityProvider,
        uint256 _begin,
        uint256 _end
    ) external view returns (bool[] memory) {
        uint256 size = 1 + _end - _begin;
        bool[] memory arr = new bool[](size);
        for (uint256 i = 0; i < size; i++) {
            arr[i] = claimed[_begin + i][_liquidityProvider];
        }
        return arr;
    }

    function merkleRoots(uint256 _begin, uint256 _end)
        external
        view
        returns (bytes32[] memory)
    {
        uint256 size = 1 + _end - _begin;
        bytes32[] memory arr = new bytes32[](size);
        for (uint256 i = 0; i < size; i++) {
            arr[i] = weekMerkleRoots[_begin + i];
        }
        return arr;
    }

    function verifyClaim(
        address _liquidityProvider,
        uint256 _week,
        uint256 _claimedBalance,
        bytes32[] memory _merkleProof
    ) public view returns (bool valid) {
        bytes32 leaf =
            keccak256(abi.encodePacked(_liquidityProvider, _claimedBalance));
        return MerkleProof.verify(_merkleProof, weekMerkleRoots[_week], leaf);
    }

    function seedAllocations(
        uint256 _week,
        bytes32 _merkleRoot,
        uint256 _totalAllocation
    ) external onlyOwner {
        require(
            weekMerkleRoots[_week] == bytes32(0),
            "cannot rewrite merkle root"
        );
        weekMerkleRoots[_week] = _merkleRoot;

        require(
            token.transferFrom(msg.sender, address(this), _totalAllocation),
            "ERR_TRANSFER_FAILED"
        );
    }
}
