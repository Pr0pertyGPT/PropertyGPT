%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.bool import FALSE
from starkware.starknet.common.syscalls import deploy
from starkware.cairo.common.uint256 import Uint256

from contracts.l2.interfaces.Istatic_a_token import Istatic_a_token

@contract_interface
namespace IBridge {
    func approve_bridge(l1_token: felt, l2_token: felt) {
    }
    func set_reward_token(token: felt) {
    }
    func set_l1_bridge(l1_bridge_address: felt) {
    }
}

@external
func delegate_execute{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() {
    
    // bridge consts
    const l2_bridge_address = 1902308026103231708399763098802936489569449978602912766430085816491897565217;
    const l1_bridge_address = 215523330021256381962255580076428681983938390349;
    const reward_token_address = 2029792542476292482162717781560870950057314618366310397915647554677269565121;//rewAAVE
    const aUSDC = 1077803441986936771120489637498156868855928333884;
    const aDAI = 14304685556238090176394662515936233272922302627;
    const aUSDT= 358678608052866257668291367909875857327283918865;
    const staticV2EthADAI=1867882240083208423799184639500919618573462941664712747609919667022414676733;
    const staticV2EthAUSDC=588102177568622932536062234131824042711704376796923341979312819023177367758;
    const staticV2EthAUSDT=1316341714119165292570263631681097098207593530730745197961203856625400552336;

    // set reward token address on bridge
    IBridge.set_reward_token(l2_bridge_address, reward_token_address);

    // set l1 bridge address
    IBridge.set_l1_bridge(l2_bridge_address, l1_bridge_address);

    
    // approve aDAI<->staticADai bridge
    IBridge.approve_bridge(l2_bridge_address, aDAI, staticV2EthADAI);

    // approve aUSDC<->staticAUsdc bridge
    IBridge.approve_bridge(l2_bridge_address, aUSDC, staticV2EthAUSDC);
    
    // approve aUSDT<->staticV2EthAUSDT bridge
    IBridge.approve_bridge(l2_bridge_address, aUSDT, staticV2EthAUSDT);

    return ();
}
