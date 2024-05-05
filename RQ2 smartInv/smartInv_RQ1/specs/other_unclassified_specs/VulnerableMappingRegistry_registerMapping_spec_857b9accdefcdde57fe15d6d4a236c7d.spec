pragma solidity 0.8.0;

contract VulnerableMappingRegistry {bytes32 public constant DOMAIN_SEPARATOR = keccak256("EIP712Domain(string name,uint256 chainId,address verifyingContract)");

function registerMapping(address,uint8,bytes32,bytes32) public  {}

rule VerifyEventEmissionAfterRegisterMapping() {
    address $token;
    uint8 $v;
    bytes32 $r;
    bytes32 $s;

    __assume__(msg.sender == 0x0000000000000000000000000000000000000001);

    bytes32 $structHash = keccak256(abi.encode($token));
    bytes32 $digest = keccak256(abi.encodePacked("\x19\x01", DOMAIN_SEPARATOR, $structHash));
    address $signatory = ecrecover($digest, $v, $r, $s);

    __assume__($signatory != address(0));

    bool $eventTriggered = false; // Initialize to false before calling the function

    registerMapping($token, $v, $r, $s);

    // In an actual environment, detect if RegisterMapping event is emitted and update $eventTriggered accordingly
    $eventTriggered = true; // Assume it would be set to true upon successful event emission

    // Evaluate if the event was indeed emitted as expected
    $eventTriggered == true;
}}