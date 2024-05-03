// SPDX-FileCopyrightText: 2023 Lido <info@lido.fi>
// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.9;

import { IReportAsyncProcessor } from "../../oracle/HashConsensus.sol";

contract MockReportProcessor is IReportAsyncProcessor {
    uint256 internal _consensusVersion;

    struct SubmitReportLastCall {
        bytes32 report;
        uint256 refSlot;
        uint256 deadline;
        uint256 callCount;
    }

    SubmitReportLastCall internal _submitReportLastCall;
    uint256 internal _lastProcessingRefSlot;

    constructor(uint256 consensusVersion) {
        _consensusVersion = consensusVersion;
    }

    function setConsensusVersion(uint256 consensusVersion) external {
        _consensusVersion = consensusVersion;
    }

    function setLastProcessingStartedRefSlot(uint256 refSlot) external {
        _lastProcessingRefSlot = refSlot;
    }

    function getLastCall_submitReport() external view returns (SubmitReportLastCall memory) {
        return _submitReportLastCall;
    }

    function startReportProcessing() external {
        _lastProcessingRefSlot = _submitReportLastCall.refSlot;
    }

    ///
    /// IReportAsyncProcessor
    ///

    function getConsensusVersion() external view returns (uint256) {
        return _consensusVersion;
    }

    function submitConsensusReport(bytes32 report, uint256 refSlot, uint256 deadline) external {
        _submitReportLastCall.report = report;
        _submitReportLastCall.refSlot = refSlot;
        _submitReportLastCall.deadline = deadline;
        ++_submitReportLastCall.callCount;
    }

    function getLastProcessingRefSlot() external view returns (uint256) {
        return _lastProcessingRefSlot;
    }
}
