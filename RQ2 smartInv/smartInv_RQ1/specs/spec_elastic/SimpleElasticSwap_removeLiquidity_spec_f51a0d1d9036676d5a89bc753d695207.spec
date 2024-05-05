pragma solidity 0.8.0;

contract SimpleElasticSwap{uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;
function removeLiquidity(uint256) public   
precondition{
    liquidity > 0 && liquidity <= liquidityBalance[msg.sender] && totalLiquidity > 0;
}

postcondition{
    baseTokenReserve == __old__(baseTokenReserve) - ((__old__(baseTokenReserve) * liquidity) / __old__(totalLiquidity));
    quoteTokenReserve == __old__(quoteTokenReserve) - ((__old__(quoteTokenReserve) * liquidity) / __old__(totalLiquidity));
    totalLiquidity == __old__(totalLiquidity) - liquidity;
    liquidityBalance[msg.sender] == __old__(liquidityBalance[msg.sender]) - liquidity;
}
}