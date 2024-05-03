%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.alloc import alloc
from starkware.starknet.common.syscalls import library_call

from contracts.l2.lib.version_initializable import VersionedInitializable

const REVISION = 1;

@storage_var
func _l1_governance_relay() -> (res: felt) {
}

@external
func initialize_governance_relay{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    l1_governance_relay: felt
) {
    VersionedInitializable.initializer(REVISION);
    _l1_governance_relay.write(l1_governance_relay);
    return ();
}

@l1_handler
func relay{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    from_address: felt, spell: felt
) {
    let (l1_governance_relay) = _l1_governance_relay.read();
    assert l1_governance_relay = from_address;

    // selector of delegate_execute() function on spell contracts
    const DELEGATE_EXECUTE_SELECTOR = 1715357134534920869852627606170305435965756153030215653526748248853578673782;

    library_call(
        class_hash=spell,
        function_selector=DELEGATE_EXECUTE_SELECTOR,
        calldata_size=0,
        calldata=new (),
    );

    return ();
}
