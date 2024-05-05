pragma solidity 0.8.0;

contract VulnerableSubmit {uint256 public lastDataTimestamp = 0;

function submit(uint256,string memory) public  {}

rule submitDataIsNewer() {
    uint256 $previousDataTimestamp;
    string memory $data;
    uint256 $newDataTimestamp;

    // Assume previous submission timestamp is known
    lastDataTimestamp = $previousDataTimestamp;

    // Assume the new data timestamp is after the last data timestamp
    __assume__($newDataTimestamp > lastDataTimestamp);

    submit($newDataTimestamp, $data);

    // Check that lastDataTimestamp is updated to the new data timestamp
    assert(lastDataTimestamp == $newDataTimestamp);
}}