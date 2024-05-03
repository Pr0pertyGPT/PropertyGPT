%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.math_cmp import is_le
from starkware.cairo.common.bool import TRUE

@storage_var
func VersionedInitializable_last_initialized_revision() -> (revision: felt) {
}

namespace VersionedInitializable {
    func initializer{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
        current_revision
    ) -> () {
        alloc_locals;
        let (last_revision) = VersionedInitializable_last_initialized_revision.read();
        let is_current_revision_gt_last = is_le(last_revision, current_revision - 1);

        with_attr error_message("Contract instance has already been initialized") {
            assert is_current_revision_gt_last = TRUE;
        }

        VersionedInitializable_last_initialized_revision.write(current_revision);
        return ();
    }
}
