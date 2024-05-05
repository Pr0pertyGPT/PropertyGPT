pragma solidity 0.8.0;

contract VulnerableMappingRegistry {bytes32 public constant DOMAIN_SEPARATOR = keccak256("EIP712Domain(string name,uint256 chainId,address verifyingContract)");


rule ValidateRegisterMappingSignatory(){
    address $token;
    uint8 $v;
    bytes32 $r;
    bytes32 $s;
    bytes32 $structHash = keccak256(abi.encode($token));
    bytes32 $digest = keccak256(abi.encodePacked("\x19\x01", DOMAIN_SEPARATOR, $structHash));
    address $signatory = ecrecover($digest, $v, $r, $s);

    __assume__(msg.sender == 0x0000000000000000000000000000000000000001);
    assert($signatory != address(0));
}}