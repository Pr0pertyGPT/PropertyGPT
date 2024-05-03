pragma solidity >=0.4.0;

import {FullMath} from '../../contracts/popsicle-v3-optimizer/libraries/FullMath.sol';

contract FullMathWrapper {
    using FullMath for uint256;

    function callMulDiv(uint256 a,
             uint256 b,
             uint256 denominator
    ) public pure returns (uint256 mulDivResult){
        mulDivResult = FullMath.mulDiv(a, b, denominator);
    }

    function callMulDivRoundingUp(uint256 a,
             uint256 b,
             uint256 denominator
    ) public pure returns (uint256 mulDivResult){
        mulDivResult = FullMath.mulDivRoundingUp(a, b, denominator);
    }
}