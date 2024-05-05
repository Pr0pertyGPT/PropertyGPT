%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.math import assert_not_zero
from starkware.starknet.common.syscalls import library_call_l1_handler, library_call
from starkware.cairo.common.bool import TRUE, FALSE

from contracts.l2.dependencies.openzeppelin.upgrades.library import Proxy

// events

@event
func proxy_deployed(proxy_admin: felt) {
}

@event
func implementation_updated(implementation_hash: felt) {
}

@event
func admin_changed(new_admin: felt) {
}

//
// Constructor
//

@constructor
func constructor{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    proxy_admin: felt
) {
    with_attr error_message("Proxy: proxy admin address should be non zero.") {
        assert_not_zero(proxy_admin);
    }
    Proxy._set_admin(proxy_admin);
    proxy_deployed.emit(proxy_admin);
    return ();
}

@external
func set_implementation{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    implementation_hash: felt
) {
    with_attr error_message("Proxy: implementation hash should be non zero.") {
        assert_not_zero(implementation_hash);
    }
    Proxy.assert_only_admin();
    Proxy._set_implementation_hash(implementation_hash);
    implementation_updated.emit(implementation_hash);
    return ();
}

//
// Getters
//

@view
func get_admin{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (admin: felt) {
    let (admin) = Proxy.get_admin();
    return (admin,);
}

@view
func get_implementation{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (
    implementation: felt
) {
    let (implementation) = Proxy.get_implementation_hash();
    return (implementation,);
}

//
// Setters
//

@external
func change_proxy_admin{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    new_admin: felt
) {
    with_attr error_message("Proxy: new admin address should be non zero.") {
        assert_not_zero(new_admin);
    }
    Proxy.assert_only_admin();
    Proxy._set_admin(new_admin);
    admin_changed.emit(new_admin);
    return ();
}

//
// Fallback functions
//

@external
@raw_input
@raw_output
func __default__{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    selector: felt, calldata_size: felt, calldata: felt*
) -> (retdata_size: felt, retdata: felt*) {
    let (class_hash) = Proxy.get_implementation_hash();
    with_attr error_message("Proxy: does not have a class hash.") {
        assert_not_zero(class_hash);
    }

    let (retdata_size: felt, retdata: felt*) = library_call(
        class_hash=class_hash,
        function_selector=selector,
        calldata_size=calldata_size,
        calldata=calldata,
    );

    return (retdata_size=retdata_size, retdata=retdata);
}

@l1_handler
@raw_input
func __l1_default__{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    selector: felt, calldata_size: felt, calldata: felt*
) {
    let (class_hash) = Proxy.get_implementation_hash();
    with_attr error_message("Proxy: does not have a class hash.") {
        assert_not_zero(class_hash);
    }

    library_call_l1_handler(
        class_hash=class_hash,
        function_selector=selector,
        calldata_size=calldata_size,
        calldata=calldata,
    );

    return ();
}
