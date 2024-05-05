// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableSubmit {
    uint256 public lastDataTimestamp = 0;

    event DataSubmitted(address indexed submitter, uint256 timestamp, string data);

    function submit(uint256 _dataTimestamp, string memory _data) public {
        // require(_dataTimestamp <= block.timestamp + 3, "oh, so you can predict the future:");

        require(_dataTimestamp > lastDataTimestamp, "Submitted data must be newer than the last submission");

        lastDataTimestamp = _dataTimestamp;

        emit DataSubmitted(msg.sender, _dataTimestamp, _data);
    }
}
