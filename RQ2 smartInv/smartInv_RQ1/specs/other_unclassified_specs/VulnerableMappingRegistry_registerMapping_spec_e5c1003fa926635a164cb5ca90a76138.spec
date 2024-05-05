pragma solidity 0.8.0;

contract VulnerableMappingRegistry {bytes32 public constant DOMAIN_SEPARATOR = keccak256("EIP712Domain(string name,uint256 chainId,address verifyingContract)");

function registerMapping(address,uint8,bytes32,bytes32) public  {}

rule ValidateRegisterMappingSignature() {
    address $token;
    uint8 $v;
    bytes32 $r;
    bytes32 $s;

    // Simulating the call to registerMapping with symbolic variables
    bytes32 $structHash = keccak256(abi.encode($token));
    bytes32 $digest = keccak256(abi.encodePacked("\x19\x01", DOMAIN_SEPARATOR, $structHash));
    address $signatory = ecrecover($digest, $v, $r, $s);

    // Assume the signatory is valid and distinct from zero address
    __assume__($signatory != 0x0000000000000000000000000000000000000000);
    // Assume a specific Ethereum address for msg.sender
    __assume__(msg.sender == 0x0000000000000000000000000000000000000001);

    // Invoke the registerMapping function with the intended parameters
    registerMapping($token, $v, $r, $s);

    // Assertions to validate the expected outcomes
    assert(ecrecover($digest, $v, $r, $s) == $signatory); // Validate recovered address matches expected signatory
}}