pragma solidity 0.8.0;

contract SimpleElasticSwap{uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;
function addLiquidity(uint256,uint256) public   
precondition{
}

postcondition{
    totalLiquidity == __old__(totalLiquidity) + (__old__(totalLiquidity) == 0 ? (baseAmount + quoteAmount) : ((baseAmount + quoteAmount) * __old__(totalLiquidity) / (__old__(baseTokenReserve) + __old__(quoteTokenReserve))));
    baseTokenReserve == __old__(baseTokenReserve) + baseAmount;
    quoteTokenReserve == __old__(quoteTokenReserve) + quoteAmount;
    liquidityBalance[msg.sender] == __old__(liquidityBalance[msg.sender]) + (__old__(totalLiquidity) == 0 ? (baseAmount + quoteAmount) : ((baseAmount + quoteAmount) * __old__(totalLiquidity) / (__old__(baseTokenReserve) + __old__(quoteTokenReserve))));
}
}