
rule integrityOfMulDivNoOverflow(uint256 a,
             uint256 b,
             uint256 denominator){
    require(denominator > 0x0 && a*b <= max_uint256);
    env e;

    uint256 mul = a * b;
    uint256 remainder = mul % denominator;
    uint256 truncated = (a * b) - remainder;
    uint256 result = callMulDiv(e , a,
             b,
             denominator);
    /*
    assert ((denominator > 0 &&
    (denominator < 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)) => (result == truncated/denominator));
    */
    assert (result == a*b/denominator);
}


rule integrityOfMulDiv(uint256 a,
             uint256 b,
             uint256 denominator){
    /* require(denominator > 0 && a*(b/denominator) >= 0 && b*(a/denominator) >= 0 &&
            a*(b/denominator) <= 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff &&
            b*(a/denominator) <= 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff); */
    env e;

    uint256 mul = a * b;
    /* uint256 remainder = mul % denominator; 
    uint256 truncated = (a * b) - remainder; */
    uint256 result = callMulDiv(e , a,
             b,
             denominator);
    
    assert (result == a*b/denominator || a==0 || b==0);
}

/*
rule integrityOfSafeMulDiv(uint256 a,
             uint256 b,
             uint256 denominator){
    require(denominator > 0 && 
            mul(a , div(b , denominator)) <= max_uint256 &&
            mul(b , div(a , denominator)) <= max_uint256);
    env e;

    uint256 mul = a * b;
    uint256 remainder = mul % denominator;
    uint256 truncated = (a * b) - remainder;
    uint256 result = callMulDiv(e , a,
             b,
             denominator);
    
    assert (result == a*b/denominator);
}
*/

rule checkMulDivRoundingUp(uint256 a,
             uint256 b,
             uint256 denominator){
    require(denominator > 0x0 && 
             a*(b/denominator) <= 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff &&
             b*(a/denominator) <= 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff);
    env e;
    uint256 result = callMulDivRoundingUp(e , a,
             b,
             denominator);
     assert ((a *b % denominator == 0) && result == (a*b)/denominator ||
              (a *b % denominator> 0) && result == (a*b)/denominator + 1);
}

