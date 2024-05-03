%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.uint256 import Uint256

@contract_interface
namespace IBridge {
    func set_l1_bridge(l1_bridge_address: felt) {
    }
}

@contract_interface
namespace IProxy {
    func set_implementation(implementation_hash: felt) {
    }
}

@external
func delegate_execute{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() {
    IBridge.set_l1_bridge(12345, 67890);
    IProxy.set_implementation(54321, 5);
    return ();
}
