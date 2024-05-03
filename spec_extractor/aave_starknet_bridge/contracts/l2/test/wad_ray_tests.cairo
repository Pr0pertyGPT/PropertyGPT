%lang starknet

from starkware.cairo.common.uint256 import Uint256

from contracts.l2.lib.wad_ray_math import (
    Wad,
    Ray,
    wad_add,
    wad_sub,
    wad_mul,
    wad_div,
    ray_add,
    ray_sub,
    ray_mul,
    ray_div,
    ray_to_wad,
    wad_to_ray,
    ray_mul_no_rounding,
    ray_to_wad_no_rounding,
    ray,
    wad,
    uint256_max,
    half_wad,
    half_ray,
)

@view
func test_wad_mul{range_check_ptr}() {
    alloc_locals;

    let (wad_) = wad();

    // zero test

    let (res) = wad_mul(Wad(Uint256(0, 10000)), Wad(Uint256(0, 0)));
    assert res = Wad(Uint256(0, 0));

    let (res) = wad_mul(Wad(Uint256(0, 0)), Wad(Uint256(0, 10000)));
    assert res = Wad(Uint256(0, 0));

    // 1 test

    let (res) = wad_mul(Wad(Uint256(0, 10000)), wad_);
    assert res = Wad(Uint256(0, 10000));

    let (res) = wad_mul(wad_, Wad(Uint256(0, 10000)));
    assert res = Wad(Uint256(0, 10000));

    // random muls

    let (wad2, _) = wad_add(wad_, wad_);
    let (wad4, _) = wad_add(wad2, wad2);
    let (res) = wad_mul(wad2, wad2);

    assert res = wad4;

    // underflow test

    let (res) = wad_mul(Wad(Uint256(1000, 0)), Wad(Uint256(1, 0)));
    assert res = Wad(Uint256(0, 0));

    let (res) = wad_mul(Wad(Uint256(1, 0)), Wad(Uint256(10000, 0)));
    assert res = Wad(Uint256(0, 0));

    return ();
}

@view
func test_wad_mul_overflow{range_check_ptr}() {
    alloc_locals;
    let (uint256_max_) = uint256_max();
    let uint256_max_wad = Wad(uint256_max_);
    let (res) = wad_mul(uint256_max_wad, uint256_max_wad);  // expected to revert
    return ();
}

@view
func test_ray_mul{range_check_ptr}() {
    alloc_locals;

    let (ray_) = ray();

    // zero test

    let (res) = ray_mul(Ray(Uint256(0, 10000)), Ray(Uint256(0, 0)));
    assert res = Ray(Uint256(0, 0));

    let (res) = ray_mul(Ray(Uint256(0, 0)), Ray(Uint256(0, 10000)));
    assert res = Ray(Uint256(0, 0));

    // 1 test

    let (res) = ray_mul(Ray(Uint256(0, 10000)), ray_);
    assert res = Ray(Uint256(0, 10000));

    let (res) = ray_mul(ray_, Ray(Uint256(0, 10000)));
    assert res = Ray(Uint256(0, 10000));

    // random muls

    let (ray2, _) = ray_add(ray_, ray_);
    let (ray4, _) = ray_add(ray2, ray2);
    let (res) = ray_mul(ray2, ray2);

    assert res = ray4;

    // underflow test

    let (res) = ray_mul(Ray(Uint256(1000, 0)), Ray(Uint256(1, 0)));
    assert res = Ray(Uint256(0, 0));

    let (res) = ray_mul(Ray(Uint256(1, 0)), Ray(Uint256(10000, 0)));
    assert res = Ray(Uint256(0, 0));

    return ();
}

@view
func test_ray_mul_overflow{range_check_ptr}() {
    alloc_locals;
    let (uint256_max_) = uint256_max();
    let uint256_max_ray = Ray(uint256_max_);
    ray_mul(uint256_max_ray, uint256_max_ray);  // expected to revert
    return ();
}

@view
func test_wad_div{range_check_ptr}() {
    alloc_locals;

    let (wad_) = wad();
    let (half_wad_) = half_wad();

    // 1 div

    let (res) = wad_div(Wad(Uint256(1000, 0)), wad_);
    assert res = Wad(Uint256(1000, 0));

    // some other divs

    let (wad2, _) = wad_add(wad_, wad_);
    let (res) = wad_div(wad_, wad2);
    assert res = half_wad_;

    // Underflow

    let (res) = wad_div(Wad(Uint256(1, 0)), Wad(Uint256(0, 100000000000000000000)));
    assert res = Wad(Uint256(0, 0));

    return ();
}

@view
func test_wad_div_zero{range_check_ptr}() {
    wad_div(Wad(Uint256(1, 1)), Wad(Uint256(0, 0)));
    return ();
}

@view
func test_wad_div_overflow{range_check_ptr}() {
    let (uint256_max_) = uint256_max();
    let uint256_max_wad = Wad(uint256_max_);
    wad_div(uint256_max_wad, Wad(Uint256(1, 0)));
    return ();
}

@view
func test_ray_div{range_check_ptr}() {
    alloc_locals;

    let (ray_) = ray();
    let (half_ray_) = half_ray();

    // 1 div

    let (res) = ray_div(Ray(Uint256(1000, 0)), ray_);
    assert res = Ray(Uint256(1000, 0));

    // some other divs

    let (ray2, _) = ray_add(ray_, ray_);
    let (res) = ray_div(ray_, ray2);
    assert res = half_ray_;

    // Underflow

    let (res) = ray_div(Ray(Uint256(1, 0)), Ray(Uint256(0, 100000000000000000000)));
    assert res = Ray(Uint256(0, 0));

    return ();
}

@view
func test_ray_div_zero{range_check_ptr}() {
    ray_div(Ray(Uint256(1, 1)), Ray(Uint256(0, 0)));
    return ();
}

@view
func test_ray_div_overflow{range_check_ptr}() {
    let (uint256_max_) = uint256_max();
    let uint256_max_ray = Ray(uint256_max_);
    ray_div(uint256_max_ray, Ray(Uint256(1, 0)));
    return ();
}

@view
func test_ray_to_wad{range_check_ptr}() {
    alloc_locals;
    let (ray_) = ray();
    let (wad_) = wad();

    let (res) = ray_to_wad(ray_);
    assert res = wad_;

    return ();
}

@view
func test_wad_to_ray{range_check_ptr}() {
    alloc_locals;
    let (ray_) = ray();
    let (wad_) = wad();

    let (res) = wad_to_ray(wad_);
    assert res = ray_;

    return ();
}

@view
func test_ray_mul_no_rounding{range_check_ptr}() {
    alloc_locals;

    let (ray_) = ray();

    // zero test

    let (res) = ray_mul_no_rounding(Ray(Uint256(0, 10000)), Ray(Uint256(0, 0)));
    assert res = Ray(Uint256(0, 0));

    let (res) = ray_mul_no_rounding(Ray(Uint256(0, 0)), Ray(Uint256(0, 10000)));
    assert res = Ray(Uint256(0, 0));

    // 1 test

    let (res) = ray_mul_no_rounding(Ray(Uint256(0, 10000)), ray_);
    assert res = Ray(Uint256(0, 10000));

    let (res) = ray_mul_no_rounding(ray_, Ray(Uint256(0, 10000)));
    assert res = Ray(Uint256(0, 10000));

    // random muls

    let (ray2, _) = ray_add(ray_, ray_);
    let (ray4, _) = ray_add(ray2, ray2);
    let (res) = ray_mul_no_rounding(ray2, ray2);

    assert res = ray4;

    // underflow test

    let (res) = ray_mul_no_rounding(Ray(Uint256(1000, 0)), Ray(Uint256(1, 0)));
    assert res = Ray(Uint256(0, 0));

    let (res) = ray_mul_no_rounding(Ray(Uint256(1, 0)), Ray(Uint256(10000, 0)));
    assert res = Ray(Uint256(0, 0));

    return ();
}

@view
func test_ray_mul_no_rounding_overflow{range_check_ptr}() {
    alloc_locals;
    let (uint256_max_) = uint256_max();
    let uint256_max_ray = Ray(uint256_max_);
    ray_mul_no_rounding(uint256_max_ray, uint256_max_ray);  // expected to revert
    return ();
}

@view
func test_ray_to_wad_no_rounding{range_check_ptr}() {
    alloc_locals;

    let (ray_) = ray();
    let (wad_) = wad();

    let (res) = ray_to_wad_no_rounding(ray_);
    assert res = wad_;

    // check rounding

    let (ray_diminished) = ray_sub(ray_, Ray(Uint256(1, 0)));
    let (wad_diminished) = wad_sub(wad_, Wad(Uint256(1, 0)));

    let (res) = ray_to_wad_no_rounding(ray_diminished);
    assert res = wad_diminished;

    return ();
}
