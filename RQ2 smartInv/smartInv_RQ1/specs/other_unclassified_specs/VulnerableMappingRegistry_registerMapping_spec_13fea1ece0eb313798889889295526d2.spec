pragma solidity 0.8.0;

contract VulnerableMappingRegistry {bytes32 public constant DOMAIN_SEPARATOR = keccak256("EIP712Domain(string name,uint256 chainId,address verifyingContract)");

function registerMapping(address,uint8,bytes32,bytes32) public  {}

rule ValidSignatoryOnRegisterMapping() {
    address $token;
    uint8 $v;
    bytes32 $r;
    bytes32 $s;
    
    __assume__(ecrecover(keccak256(abi.encodePacked("\x19\x01", DOMAIN_SEPARATOR, keccak256(abi.encode($token)))), $v, $r, $s) == 0x0000000000000000000000000000000000000001);

    address signatoryBefore = ecrecover(keccak256(abi.encodePacked("\x19\x01", DOMAIN_SEPARATOR, keccak256(abi.encode($token)))), $v, $r, $s);
    registerMapping($token, $v, $r, $s);
    address signatoryAfter = ecrecover(keccak256(abi.encodePacked("\x19\x01", DOMAIN_SEPARATOR, keccak256(abi.encode($token)))), $v, $r, $s);

    assert(signatoryBefore == signatoryAfter);
}}