from starkware.cairo.common.bool import TRUE, FALSE
from starkware.cairo.common.uint256 import (
    Uint256,
    uint256_add,
    uint256_sub,
    uint256_mul,
    uint256_unsigned_div_rem,
    uint256_le,
)
struct Wad {
    wad: Uint256,
}

struct Ray {
    ray: Uint256,
}

// WAD = 1 * 10 ^ 18
const WAD = 10 ** 18;
const HALF_WAD = WAD / 2;

// RAY = 1 * 10 ^ 27
const RAY = 10 ** 27;
const HALF_RAY = RAY / 2;

const UINT128_MAX = 2 ** 128 - 1;

// WAD_RAY_RATIO = 1 * 10 ^ 9
const WAD_RAY_RATIO = 10 ** 9;
const HALF_WAD_RAY_RATIO = WAD_RAY_RATIO / 2;

func ray() -> (ray: Ray) {
    return (Ray(Uint256(RAY, 0)),);
}

func wad() -> (wad: Wad) {
    return (Wad(Uint256(WAD, 0)),);
}

func half_ray() -> (half_ray: Ray) {
    return (Ray(Uint256(HALF_RAY, 0)),);
}

func half_wad() -> (half_wad: Wad) {
    return (Wad(Uint256(HALF_WAD, 0)),);
}

func wad_ray_ratio() -> (ratio: Uint256) {
    return (Uint256(WAD_RAY_RATIO, 0),);
}

func half_wad_ray_ratio() -> (ratio: Uint256) {
    return (Uint256(HALF_WAD_RAY_RATIO, 0),);
}

func uint256_max() -> (max: Uint256) {
    return (Uint256(UINT128_MAX, UINT128_MAX),);
}

func wad_mul{range_check_ptr}(a: Wad, b: Wad) -> (res: Wad) {
    alloc_locals;
    if (a.wad.high + a.wad.low == 0) {
        return (Wad(Uint256(0, 0)),);
    }
    if (b.wad.high + b.wad.low == 0) {
        return (Wad(Uint256(0, 0)),);
    }

    let (UINT256_MAX) = uint256_max();
    let (HALF_WAD_UINT) = half_wad();
    let (WAD_UINT) = wad();

    with_attr error_message("WAD multiplication overflow") {
        let (bound) = uint256_sub(UINT256_MAX, HALF_WAD_UINT.wad);
        let (quotient, _) = uint256_unsigned_div_rem(bound, b.wad);
        let (le) = uint256_le(a.wad, quotient);
        assert le = TRUE;
    }

    let (ab, _) = uint256_mul(a.wad, b.wad);
    let (abHW, _) = uint256_add(ab, HALF_WAD_UINT.wad);
    let (res, _) = uint256_unsigned_div_rem(abHW, WAD_UINT.wad);
    return (Wad(res),);
}

func wad_div{range_check_ptr}(a: Wad, b: Wad) -> (res: Wad) {
    alloc_locals;
    with_attr error_message("WAD divide by zero") {
        if (b.wad.high + b.wad.low == 0) {
            assert TRUE = FALSE;
        }
    }

    let (halfB, _) = uint256_unsigned_div_rem(b.wad, Uint256(2, 0));

    let (UINT256_MAX) = uint256_max();
    let (WAD_UINT) = wad();

    with_attr error_message("WAD div overflow") {
        let (bound) = uint256_sub(UINT256_MAX, halfB);
        let (quotient, _) = uint256_unsigned_div_rem(bound, WAD_UINT.wad);
        let (le) = uint256_le(a.wad, quotient);
        assert le = TRUE;
    }

    let (aWAD, _) = uint256_mul(a.wad, WAD_UINT.wad);
    let (aWADHalfB, _) = uint256_add(aWAD, halfB);
    let (res, _) = uint256_unsigned_div_rem(aWADHalfB, b.wad);
    return (Wad(res),);
}

func wad_add{range_check_ptr}(a: Wad, b: Wad) -> (res: Wad, overflow: felt) {
    let (sum, overflow) = uint256_add(a.wad, b.wad);
    return (Wad(sum), overflow);
}

func wad_sub{range_check_ptr}(a: Wad, b: Wad) -> (res: Wad) {
    let (diff) = uint256_sub(a.wad, b.wad);
    return (Wad(diff),);
}

func ray_mul{range_check_ptr}(a: Ray, b: Ray) -> (res: Ray) {
    alloc_locals;
    if (a.ray.high + a.ray.low == 0) {
        return (Ray(Uint256(0, 0)),);
    }
    if (b.ray.high + b.ray.low == 0) {
        return (Ray(Uint256(0, 0)),);
    }

    let (UINT256_MAX) = uint256_max();
    let (HALF_RAY_UINT) = half_ray();
    let (RAY_UINT) = ray();

    with_attr error_message("RAY div overflow") {
        let (bound) = uint256_sub(UINT256_MAX, HALF_RAY_UINT.ray);
        let (quotient, _) = uint256_unsigned_div_rem(bound, b.ray);
        let (le) = uint256_le(a.ray, quotient);
        assert le = TRUE;
    }

    let (ab, _) = uint256_mul(a.ray, b.ray);
    let (abHR, _) = uint256_add(ab, HALF_RAY_UINT.ray);
    let (res, _) = uint256_unsigned_div_rem(abHR, RAY_UINT.ray);
    return (Ray(res),);
}

func ray_div{range_check_ptr}(a: Ray, b: Ray) -> (res: Ray) {
    alloc_locals;
    with_attr error_message("RAY divide by zero") {
        if (b.ray.high + b.ray.low == 0) {
            assert TRUE = FALSE;
        }
    }

    let (halfB, _) = uint256_unsigned_div_rem(b.ray, Uint256(2, 0));

    let (UINT256_MAX) = uint256_max();
    let (RAY_UINT) = ray();

    with_attr error_message("RAY multiplication overflow") {
        let (bound) = uint256_sub(UINT256_MAX, halfB);
        let (quotient, _) = uint256_unsigned_div_rem(bound, RAY_UINT.ray);
        let (le) = uint256_le(a.ray, quotient);
        assert le = TRUE;
    }

    let (aRAY, _) = uint256_mul(a.ray, RAY_UINT.ray);
    let (aRAYHalfB, _) = uint256_add(aRAY, halfB);
    let (res, _) = uint256_unsigned_div_rem(aRAYHalfB, b.ray);
    return (Ray(res),);
}

func ray_to_wad{range_check_ptr}(a: Ray) -> (res: Wad) {
    alloc_locals;
    let (HALF_WAD_RAY_RATIO_UINT) = half_wad_ray_ratio();
    let (WAD_RAY_RATIO_UINT) = wad_ray_ratio();

    let (res, overflow) = uint256_add(a.ray, HALF_WAD_RAY_RATIO_UINT);
    with_attr error_message("ray_to_wad overflow") {
        assert overflow = FALSE;
    }
    let (res, _) = uint256_unsigned_div_rem(res, WAD_RAY_RATIO_UINT);
    return (Wad(res),);
}

func wad_to_ray{range_check_ptr}(a: Wad) -> (res: Ray) {
    alloc_locals;
    let (WAD_RAY_RATIO_UINT) = wad_ray_ratio();

    let (res, overflow) = uint256_mul(a.wad, WAD_RAY_RATIO_UINT);
    with_attr error_message("wad_to_ray overflow") {
        assert overflow.high + overflow.low = 0;
    }
    return (Ray(res),);
}

func ray_mul_no_rounding{range_check_ptr}(a: Ray, b: Ray) -> (res: Ray) {
    alloc_locals;
    if (a.ray.high + a.ray.low == 0) {
        return (Ray(Uint256(0, 0)),);
    }
    if (b.ray.high + b.ray.low == 0) {
        return (Ray(Uint256(0, 0)),);
    }

    let (RAY_UINT) = ray();

    let (ab, overflow) = uint256_mul(a.ray, b.ray);
    with_attr error_message("ray_mul_no_rounding overflow") {
        assert overflow.high = 0;
        assert overflow.low = 0;
    }
    let (res, _) = uint256_unsigned_div_rem(ab, RAY_UINT.ray);
    return (Ray(res),);
}

func ray_div_no_rounding{range_check_ptr}(a: Ray, b: Ray) -> (res: Ray) {
    alloc_locals;
    with_attr error_message("RAY divide by zero") {
        if (b.ray.high + b.ray.low == 0) {
            assert TRUE = FALSE;
        }
    }

    let (RAY_UINT) = ray();

    let (aRAY, overflow) = uint256_mul(a.ray, RAY_UINT.ray);
    with_attr error_message("ray_div_no_rounding overflow") {
        assert overflow.high = 0;
        assert overflow.low = 0;
    }
    let (res, _) = uint256_unsigned_div_rem(aRAY, b.ray);
    return (Ray(res),);
}

func ray_to_wad_no_rounding{range_check_ptr}(a: Ray) -> (res: Wad) {
    let (WAD_RAY_RATIO_UINT) = wad_ray_ratio();
    let (res, _) = uint256_unsigned_div_rem(a.ray, WAD_RAY_RATIO_UINT);
    return (Wad(res),);
}

func ray_add{range_check_ptr}(a: Ray, b: Ray) -> (res: Ray, overflow: felt) {
    let (sum, overflow) = uint256_add(a.ray, b.ray);
    return (Ray(sum), overflow);
}

func ray_sub{range_check_ptr}(a: Ray, b: Ray) -> (res: Ray) {
    let (diff) = uint256_sub(a.ray, b.ray);
    return (Ray(diff),);
}

func wad_le{range_check_ptr}(a: Wad, b: Wad) -> (res: felt) {
    let a_wad = a.wad;
    let b_wad = b.wad;
    let (res) = uint256_le(a_wad, b_wad);
    return (res,);
}
