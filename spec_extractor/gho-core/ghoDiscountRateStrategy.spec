methods {
    calculateDiscountRate(uint256, uint256) returns (uint256) envfree
    MIN_DISCOUNT_TOKEN_BALANCE() returns (uint256) envfree
    MIN_DEBT_TOKEN_BALANCE() returns (uint256) envfree
    DISCOUNT_RATE() returns (uint256) envfree
    GHO_DISCOUNTED_PER_DISCOUNT_TOKEN() returns (uint256) envfree
    wadMul(uint256, uint256) returns (uint256) envfree
}


/**
* @title proves that the discount rate is caped by the maximal discount rate value
**/
rule limitOnDiscountRate() {
    uint256 debtBalance;
    uint256 discountTokenBalance;
    uint256 discountRate = calculateDiscountRate(debtBalance, discountTokenBalance);
    assert(discountRate <= DISCOUNT_RATE());
}

