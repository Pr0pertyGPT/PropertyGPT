// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import { AaveGovernanceV2, IExecutorWithTimelock, IGovernanceStrategy } from "aave-address-book/AaveGovernanceV2.sol";
import { AutonomousProposal } from "aave-autonomous-proposal/contracts/AutonomousProposal.sol";
import { IAutonomousProposal } from "aave-autonomous-proposal/contracts/interfaces/IAutonomousProposal.sol";

contract RescueAutonomousProposal is AutonomousProposal {
    address public immutable PAYLOAD_SHORT;
    address public immutable PAYLOAD_LONG;

    bytes32 public immutable SHORT_PAYLOAD_IPFS;
    bytes32 public immutable LONG_PAYLOAD_IPFS;

    uint256 public longExecutorProposalId;
    uint256 public shortExecutorProposalId;

    event ProposalsCreated(
        address executor,
        uint256 longExecutorProposalId,
        uint256 shortExecutorProposalId,
        address longExecutorPayload,
        bytes32 longIpfsHash,
        address shortExecutorPayload,
        bytes32 shortIpfsHash
    );

    constructor(
        address payloadShort,
        address payloadLong,
        bytes32 payloadShortIpfs,
        bytes32 payloadLongIpfs,
        uint256 creationTimestamp
    ) AutonomousProposal(creationTimestamp) {
        require(payloadShort != address(0), "SHORT_PAYLOAD_ADDRESS_0");
        require(
            payloadShortIpfs != bytes32(0),
            "SHORT_PAYLOAD_IPFS_HASH_BYTES32_0"
        );
        require(payloadLong != address(0), "LONG_PAYLOAD_ADDRESS_0");
        require(
            payloadLongIpfs != bytes32(0),
            "LONG_PAYLOAD_IPFS_HASH_BYTES32_0"
        );

        PAYLOAD_LONG = payloadLong;
        PAYLOAD_SHORT = payloadShort;
        SHORT_PAYLOAD_IPFS = payloadShortIpfs;
        LONG_PAYLOAD_IPFS = payloadLongIpfs;
    }

    function create() external override inCreationWindow {
        require(
            longExecutorProposalId == 0 && shortExecutorProposalId == 0,
            "PROPOSALS_ALREADY_CREATED"
        );

        IAutonomousProposal.ProposalParams[]
            memory longParams = new IAutonomousProposal.ProposalParams[](1);
        IAutonomousProposal.ProposalParams[]
            memory shortParams = new IAutonomousProposal.ProposalParams[](1);
        longParams[0] = IAutonomousProposal.ProposalParams({
            target: PAYLOAD_LONG,
            withDelegateCall: true,
            value: 0,
            callData: "",
            signature: "execute()"
        });
        shortParams[0] = IAutonomousProposal.ProposalParams({
            target: PAYLOAD_SHORT,
            withDelegateCall: true,
            value: 0,
            callData: "",
            signature: "execute()"
        });

        longExecutorProposalId = _createProposal(
            AaveGovernanceV2.LONG_EXECUTOR,
            LONG_PAYLOAD_IPFS,
            longParams
        );

        shortExecutorProposalId = _createProposal(
            AaveGovernanceV2.SHORT_EXECUTOR,
            SHORT_PAYLOAD_IPFS,
            shortParams
        );

        emit ProposalsCreated(
            msg.sender,
            longExecutorProposalId,
            shortExecutorProposalId,
            PAYLOAD_LONG,
            LONG_PAYLOAD_IPFS,
            PAYLOAD_SHORT,
            SHORT_PAYLOAD_IPFS
        );
    }

    /// @dev method to vote on the governance proposals, in case there is some
    /// voting power delegation by error
    function vote() external override {
        require(
            longExecutorProposalId != 0 && shortExecutorProposalId != 0,
            "PROPOSALS_NOT_CREATED"
        );
        AaveGovernanceV2.GOV.submitVote(longExecutorProposalId, true);
        AaveGovernanceV2.GOV.submitVote(shortExecutorProposalId, true);
    }
}
