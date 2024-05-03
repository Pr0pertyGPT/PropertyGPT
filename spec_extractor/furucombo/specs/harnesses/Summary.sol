pragma experimental ABIEncoderV2;

import "./DummyERC20A.sol";

interface IERC20WithDummyFunctionality {
    function transfer(address to, uint amt) external;
    function transferFrom(address from, address to, uint amt) external;
    function balanceOf(address who) external returns (uint);
    function allowance(address a, address b) external returns (uint);
    function havocMe(address proxy) external;
    function havocMeEth() external;
}

interface Nothing {
    function nop() external payable;
}

interface WithEthAddress {
    function ETH_ADDRESS() external returns (address);
    function WETH() external returns (address);
}

interface IMakerGemJoin {
    function gem() external returns(address);
}

// used to summarize different functions
contract Summary {

    function getEthAddress(address handler) external returns (address) {
        // either the handler defines a ETH_ADDRESS function or it does not. If it does not then just return address(0)
        address eth = address(0);
        try WithEthAddress(handler).ETH_ADDRESS() returns (address x) {
            eth = x;
        } catch {
            eth = address(0);
        }
        return eth;
    }

    address nondetWeth;
    function getWethAddress(address handler) public returns (address) {
        // either the handler defines a ETH_ADDRESS function or it does not. If it does not then just return address(0)
        address eth = nondetWeth;
        try WithEthAddress(handler).WETH() returns (address x) {
            eth = x;
        } catch {
            eth = nondetWeth;
        }
        return eth;
    }


    IERC20WithDummyFunctionality public erc20A;
    IERC20WithDummyFunctionality public erc20B;
    bytes32 executeRet;
    uint256 executeRetUint256;

    address faucet;
    uint someAmount;
    uint someAmount2;

    function havocDummyToken() private {
        if (erc20A.allowance(msg.sender, address(this)) > 0) {
            // preserves proxy eth balance if no eth passed
            if (msg.value == 0) {
                erc20A.havocMe(msg.sender);
            } else {
                erc20A.havocMeEth();
            }
        } else {
            // simulate receiving tokens
            erc20A.transferFrom(faucet, msg.sender, someAmount);
        }
    }

    // for HMaker, HSCompound
    address[] delegated;
    function lenDelegated() external returns (uint256) { return delegated.length; }
    function checkDelegated(address allowed) external returns (bool) {
        for (uint i = 0 ; i < delegated.length; i++) {
            if (delegated[i] != allowed) {
                return false;
            }
        }

        return true;
    }

    function execute(address a, bytes calldata b) external payable returns (bytes32) {
        delegated.push(a);
        havocDummyToken();
        return executeRet;
    }

    /* Desired proxy.execute() */
    /*function execute(address a, bytes calldata b) external payable returns (bytes32) {
        delegated.push(a);
        (bool success, bytes memory data) = address(this).call(b);
        require(success);
        return executeRet;
    }*/

    function freeETH(address cdpManager,address ethJoin,uint256 cdp,uint256 wad) external payable {
        Nothing(msg.sender).nop{value:wad}();
    }
    function freeGem(address cdpManager,address gemJoin,uint256 cdp,uint256 wad) external payable {
        generatedToken = IMakerGemJoin(gemJoin).gem();
        IERC20WithDummyFunctionality(generatedToken).transfer(msg.sender, wad);
    }


    address _owner;
    function owner() external returns (address) {
        return _owner;
    }

    function claimComp(address a) external {
        // ERC20B will be in the role of "COMP"
        generatedToken = address(erc20B);
        erc20B.transfer(a, someAmount);
    }

    // for HAaveProtocol
    // erc20A is the underlying and erc20B is the AToken
    function deposit(address r, uint a, uint16 c) external payable {
        consumedToken = r;
        shouldBeConsumedAmount = a;
        IERC20WithDummyFunctionality(r).transferFrom(msg.sender, address(this), a);
        require (r == address(erc20A));
        // here erc20B is the "aToken"
        generatedToken = address(erc20B);
        require (a == 0 || someAmount > 0); // this may actually not hold in reality, but depends on Aave code
        erc20B.transferFrom(address(0), msg.sender, someAmount); // "minting"
    }

    function redeem(uint amount) external {
        consumedToken = address(erc20B);
        shouldBeConsumedAmount = amount;
        generatedToken = address(erc20A);
        erc20B.transferFrom(msg.sender, address(0), amount); // "burning"
        require (amount == 0 || someAmount > 0); // this may actually not hold in reality, but depends on Aave code
        erc20A.transferFrom(address(this), msg.sender, someAmount);
    }

    function flashLoan(address receiver, address reserve, uint256 amount, bytes calldata params) external {
        havocDummyToken();
    }

    // for HAaveProtocol2
    // erc20A is the underlying and erc20B is the AToken
    function borrow(
        address asset,
        uint256 amount,
        uint256 interestRateMode,
        uint16 referralCode,
        address onBehalfOf
    ) external {
        generatedToken = asset;
        IERC20WithDummyFunctionality(asset).transfer(onBehalfOf, amount);
    }

    function deposit(
        address asset,
        uint256 amount,
        address onBehalfOf,
        uint16 referralCode
    ) external {
        // if asset is WETH then don't track consumed tokens (will be incremented by WETH deposit and decremented here)
        if (getWethAddress(msg.sender) != asset) {
            consumedToken = asset;
            shouldBeConsumedAmount = amount;
        }
        require (asset == address(erc20A));
        generatedToken = address(erc20B);
        IERC20WithDummyFunctionality(asset).transferFrom(onBehalfOf, address(this), amount);
        erc20B.transferFrom(address(0), msg.sender, amount); // "minting"
    }

    function flashLoan(
        address receiverAddress,
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata modes,
        address onBehalfOf,
        bytes calldata params,
        uint16 referralCode
    ) external {
        havocDummyToken();
    }

    function repay(
        address asset,
        uint256 amount,
        uint256 rateMode,
        address onBehalfOf
    ) external returns (uint256) {
        consumedToken = address(erc20A);
        shouldBeConsumedAmount = executeRetUint256; // could be less
        require (executeRetUint256 <= amount);
        erc20A.transferFrom(onBehalfOf,address(this),executeRetUint256);
        return executeRetUint256;
    }

    function withdraw(
        address asset,
        uint256 amount,
        address to
    ) external returns (uint256) {
        require (asset == address(erc20A));
        consumedToken = address(erc20B);
        shouldBeConsumedAmount = amount;
        generatedToken = address(erc20A);
        erc20B.transferFrom(msg.sender, address(0), amount);
        erc20A.transfer(msg.sender, amount);
        return executeRetUint256;
    }

    // IWETH9
    function deposit() external payable {
        // erc20A will be the "weth" token here
        erc20A.transferFrom(address(0), msg.sender, msg.value);
    }
    function withdraw(uint256 amt) external {
        Nothing(msg.sender).nop{value:amt}();
    }

    // HOneInchV3
    struct SwapDescriptionV3 {
        address srcToken;
        address dstToken;
        address srcReceiver;
        address dstReceiver;
        uint256 amount;
        uint256 minReturnAmount;
        uint256 flags;
        bytes permit;
    }
    function swap(address a, SwapDescriptionV3 calldata desc, bytes calldata data) external payable returns (uint256) {
        consumedToken = desc.srcToken;
        generatedToken = desc.dstToken;
        shouldBeConsumedAmount = desc.amount;
        IERC20WithDummyFunctionality(desc.srcToken).transferFrom(msg.sender, address(this), desc.amount);
        IERC20WithDummyFunctionality(desc.dstToken).transfer(msg.sender, someAmount);
        return executeRetUint256;
    }
    function unoswap(address srcToken, uint256 amount, uint256 minReturn, bytes32[] calldata) external payable returns (uint256) {
        consumedToken = srcToken;
        // generatedToken = dstToken;
        shouldBeConsumedAmount = amount;
        IERC20WithDummyFunctionality(srcToken).transferFrom(msg.sender, address(this), amount);
        // IERC20WithDummyFunctionality(dstToken).transfer(msg.sender, someAmount);
        return executeRetUint256;
    }

    // HUniswap
    // the exchange is also the LP token. Applicable to HUniswapV2 and HSushiswap
    function add(uint a, uint b) internal pure returns (uint256) {
        uint c = a +b;
        require (c >= a);
        return c;
    }
    function sub(uint a, uint b) internal pure returns (uint256) {
        require (a>=b);
        return a-b;
    }

    mapping (address => uint) public balanceOf;
    mapping (address => mapping (address => uint)) public allowance;
    uint public totalSupply;
    function approve(address spender, uint amount) public returns (bool) { allowance[msg.sender][spender] = amount; return true; }
    function transfer(address recipient, uint256 amount) public returns (bool) {
        balanceOf[msg.sender] = sub(balanceOf[msg.sender], amount);
        balanceOf[recipient] = add(balanceOf[recipient], amount);
        return true;
    }
    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) public returns (bool) {
        balanceOf[sender] = sub(balanceOf[sender], amount);
        balanceOf[recipient] = add(balanceOf[recipient], amount);
        allowance[sender][msg.sender] = sub(allowance[sender][msg.sender], amount);
        return true;
    }

    // we assume the pair is erc20A <> "eth"
    // function ethToTokenSwapInput(uint256 min_tokens, uint256 deadline) external payable returns (uint256  tokens_bought) {
    //     generatedToken = address(erc20A);
    //     erc20A.transfer(msg.sender, someAmount);
    //     tokens_bought = someAmount;
    // }
    // function ethToTokenSwapOutput(uint256 tokens_bought, uint256 deadline) external payable returns (uint256  eth_sold) {
    //     generatedToken = address(erc20A);
    //     erc20A.transfer(msg.sender, tokens_bought);
    //     eth_sold = msg.value;
    // }
    // function addLiquidity(uint256 min_liquidity, uint256 max_tokens, uint256 deadline) external payable returns (uint256) {
    //     // this will be the LP token
    //     consumedToken = address(erc20A);
    //     require (address(erc20A) != address(this)); // LP token is not exchanged token
    //     shouldBeConsumedAmount = someAmount2;
    //     // someAmount is how much we get
    //     // someAmount2 is how much we give in tokens (msg.value is how much we give in ETH)
    //     require (someAmount >= min_liquidity && min_liquidity > 0);
    //     generatedToken = address(this);
    //     erc20A.transferFrom(msg.sender, address(this), someAmount2);
    //     transferFrom(address(0), msg.sender, someAmount);
    //     return someAmount;
    // }
    // function tokenToEthSwapInput(uint256 tokens_sold, uint256 min_eth, uint256 deadline) external returns (uint256  eth_bought) {
    //     shouldBeConsumedAmount = tokens_sold;
    //     consumedToken = address(erc20A);
    //     erc20A.transferFrom(msg.sender, address(this), tokens_sold);
    //     //require (someAmount > min_eth);
    //     eth_bought = someAmount;
    //     Nothing(msg.sender).nop{value:someAmount}();
    // }
    // function tokenToEthSwapOutput(uint256 eth_bought, uint256 max_tokens, uint256 deadline) external returns (uint256  tokens_sold) {
    //     consumedToken = address(erc20A);
    //     shouldBeConsumedAmount = someAmount;
    //     require (someAmount <= max_tokens);
    //     erc20A.transferFrom(msg.sender, address(this), someAmount);
    //     tokens_sold = someAmount;
    //     Nothing(msg.sender).nop{value:eth_bought}();
    // }
    // function removeLiquidity(uint256 amount, uint256 min_eth, uint256 min_tokens, uint256 deadline) external returns (uint256, uint256) {
    //     // this will be the LP token
    //     consumedToken = address(this);
    //     shouldBeConsumedAmount = amount;
    //     transferFrom(msg.sender, address(0), amount);
    //     // transfer someAmount of eth and someAmount2 of tokens
    //     erc20A.transfer(msg.sender, someAmount2);
    //     Nothing(msg.sender).nop{value:someAmount}();
    //     return (someAmount, someAmount2); // ordering is eth, token
    // }
    // function tokenToTokenSwapOutput(uint256 tokens_bought, uint256 max_tokens_sold, uint256 max_eth_sold, uint256 deadline, address token_addr) external returns (uint256  tokens_sold) {
    //     require(tokens_bought > 0); // https://github.com/Uniswap/uniswap-v1/blob/c10c08d81d6114f694baa8bd32f555a40f6264da/contracts/uniswap_exchange.vy#L313
    //     shouldBeConsumedAmount = someAmount;
    //     consumedToken = address(erc20A);
    //     require (address(erc20A) != address(this)); // LP token is not the exchanged token
    //     generatedToken = token_addr; // can token_addr be the LP token? probably not https://github.com/Uniswap/uniswap-v1/blob/c10c08d81d6114f694baa8bd32f555a40f6264da/contracts/uniswap_exchange.vy#L314
    //     require (token_addr != address(this));
    //     tokens_sold = someAmount;
    //     erc20A.transferFrom(msg.sender, address(this), someAmount);
    //     require(token_addr == address(erc20B)); // It doesn't make sense to have a pair token<>token
    //     erc20B.transfer(msg.sender, tokens_bought);
    // }
    // function tokenToTokenSwapInput(uint256 tokens_sold, uint256 min_tokens_bought, uint256 min_eth_bought, uint256 deadline, address token_addr) external returns (uint256  tokens_bought) {
    //     shouldBeConsumedAmount = tokens_sold;
    //     consumedToken = address(erc20A);
    //     require (address(erc20A) != address(this)); // LP token is not the exchanged token
    //     generatedToken = token_addr;
    //     // token_addr is not the LP token https://github.com/Uniswap/uniswap-v1/blob/c10c08d81d6114f694baa8bd32f555a40f6264da/contracts/uniswap_exchange.vy#L273
    //     require (token_addr != address(this));
    //     erc20A.transferFrom(msg.sender, address(this), tokens_sold);
    //     require(token_addr == address(erc20B)); // It doesn't make sense to have a pair token<>token
    //     tokens_bought = someAmount;
    //     require (tokens_bought > min_tokens_bought && min_tokens_bought > 0); // based on https://github.com/Uniswap/uniswap-v1/blob/c10c08d81d6114f694baa8bd32f555a40f6264da/contracts/uniswap_exchange.vy#L272
    //     erc20B.transfer(msg.sender, someAmount);
    // }

    // HUniswapV2, HSushiSwap
    function addLiquidity(
        address tokenA,
        address tokenB,
        uint256 amountADesired,
        uint256 amountBDesired,
        uint256 amountAMin,
        uint256 amountBMin,
        address to,
        uint256 deadline
    )
        external
        returns (
            uint256 amountA,
            uint256 amountB,
            uint256 liquidity
        ) {
            require (tokenA != tokenB && tokenA != address(this) && tokenB != address(this));
            require (amountAMin > 0 && amountBMin > 0);
            uint amountA = amountAMin;
            uint amountB = amountBMin;
            IERC20WithDummyFunctionality(tokenA).transferFrom(msg.sender, address(this), amountA);
            IERC20WithDummyFunctionality(tokenB).transferFrom(msg.sender, address(this), amountB);
            transferFrom(address(0), to, someAmount);
            consumedToken = tokenA;
            shouldBeConsumedAmount = amountA;
            generatedToken = address(this);
            require(someAmount > 0);
            liquidity = someAmount;
        }

    function addLiquidityETH(
        address token,
        uint256 amountTokenDesired,
        uint256 amountTokenMin,
        uint256 amountETHMin,
        address to,
        uint256 deadline
    )
        external
        payable
        returns (
            uint256 amountToken,
            uint256 amountETH,
            uint256 liquidity
        ) {
            require (token != address(this));
            consumedToken = token;
            require (amountTokenMin > 0);
            amountToken = amountTokenMin;
            shouldBeConsumedAmount = amountTokenMin;
            generatedToken = address(this);
            IERC20WithDummyFunctionality(token).transferFrom(msg.sender, address(this), amountToken);
            amountETH = msg.value;
            transferFrom(address(0), to, someAmount);
            require(someAmount > 0);
            liquidity = someAmount;
        }

    function removeLiquidity(
        address tokenA,
        address tokenB,
        uint256 liquidity,
        uint256 amountAMin,
        uint256 amountBMin,
        address to,
        uint256 deadline
    ) external returns (uint256 amountA, uint256 amountB) {
        require (tokenA != tokenB && tokenA != address(this) && tokenB != address(this));
        require(amountAMin > 0 && amountBMin > 0);
        consumedToken = address(this);
        shouldBeConsumedAmount = liquidity;
        generatedToken = tokenA;
        transferFrom(msg.sender, address(0), liquidity);
        IERC20WithDummyFunctionality(tokenA).transfer(to, amountAMin);
        IERC20WithDummyFunctionality(tokenB).transfer(to, amountBMin);
        return (amountAMin, amountBMin);
    }

    function removeLiquidityETH(
        address token,
        uint256 liquidity,
        uint256 amountTokenMin,
        uint256 amountETHMin,
        address to,
        uint256 deadline
    ) external returns (uint256 amountToken, uint256 amountETH) {
        require (token != address(this));
        require(amountTokenMin > 0);
        consumedToken = address(this);
        shouldBeConsumedAmount = liquidity;
        generatedToken = token;
        transferFrom(msg.sender, address(0), liquidity);
        IERC20WithDummyFunctionality(token).transfer(to, amountTokenMin);
        Nothing(to).nop{value:amountETHMin}();
        return (amountTokenMin,amountETHMin);
    }

    uint[] someArr;
    function swapExactTokensForTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts) {
        require (amountIn > 0 && amountOutMin > 0);
        require (path.length == 2);
        require (path[0] != address(this) && path[1] != address(this));
        consumedToken = path[0];
        generatedToken = path[1];
        require (consumedToken != generatedToken);
        shouldBeConsumedAmount = amountIn;
        IERC20WithDummyFunctionality(consumedToken).transferFrom(msg.sender, address(this), amountIn);
        IERC20WithDummyFunctionality(generatedToken).transfer(to, amountOutMin);
        return someArr;
    }

    function swapTokensForExactTokens(
        uint256 amountOut,
        uint256 amountInMax,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts) {
        require (amountInMax > 0 && amountOut > 0);
        require (path.length == 2);
        require (path[0] != address(this) && path[1] != address(this));
        consumedToken = path[0];
        generatedToken = path[1];
        require (consumedToken != generatedToken);
        shouldBeConsumedAmount = amountInMax;
        IERC20WithDummyFunctionality(consumedToken).transferFrom(msg.sender, address(this), amountInMax);
        IERC20WithDummyFunctionality(generatedToken).transfer(to, amountOut);
        return someArr;
    }

    function swapExactETHForTokens(
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external payable returns (uint256[] memory amounts) {
        require (amountOutMin > 0);
        require(path.length == 2);
        require (path[0] != address(this) && path[1] != address(this));
        generatedToken = path[1];
        IERC20WithDummyFunctionality(generatedToken).transfer(to, amountOutMin);
        return someArr;
    }

    function swapTokensForExactETH(
        uint256 amountOut,
        uint256 amountInMax,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts) {
        require (amountOut > 0 && amountInMax > 0);
        require(path.length == 2);
        require (path[0] != address(this) && path[1] != address(this));
        consumedToken = path[0];
        shouldBeConsumedAmount = amountInMax;
        IERC20WithDummyFunctionality(consumedToken).transferFrom(msg.sender, address(this), amountInMax);
        Nothing(to).nop{value:amountOut}();
        return someArr;
    }

    function swapExactTokensForETH(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts) {
        require(amountIn > 0 && amountOutMin > 0);
        require (path.length == 2);
        require (path[0] != address(this) && path[1] != address(this));
        consumedToken = path[0];
        shouldBeConsumedAmount = amountIn;
        IERC20WithDummyFunctionality(consumedToken).transferFrom(msg.sender, address(this), amountIn);
        Nothing(to).nop{value:amountOutMin}();
        return someArr;
    }

    function swapETHForExactTokens(
        uint256 amountOut,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external payable returns (uint256[] memory amounts) {
        require (amountOut > 0);
        require (path.length == 2);
        require (path[0] != address(this) && path[1] != address(this));
        generatedToken = path[1];
        IERC20WithDummyFunctionality(generatedToken).transfer(to, amountOut);
        return someArr;
    }

    // HUniswapV3
    function toAddress(bytes memory _bytes, uint256 _start)
        internal
        pure
        returns (address)
    {
        require(_start + 20 >= _start, "toAddress_overflow");
        require(_bytes.length >= _start + 20, "toAddress_outOfBounds");
        address tempAddress;

        assembly {
            tempAddress := div(
                mload(add(add(_bytes, 0x20), _start)),
                0x1000000000000000000000000
            )
        }

        return tempAddress;
    }
    function _getFirstToken(bytes memory path) internal pure returns (address) {
        return toAddress(path, 0);
    }

    function _getLastToken(bytes memory path) internal view returns (address) {
        require(path.length >= 43, "Path size too small"); // PATH_SIZE = 43
        return toAddress(path, path.length - 43);
    }
    struct ExactInputSingleParams {
        address tokenIn;
        address tokenOut;
        uint24 fee;
        address recipient;
        uint256 deadline;
        uint256 amountIn;
        uint256 amountOutMinimum;
        uint160 sqrtPriceLimitX96;
    }
    struct ExactInputParams {
        bytes path;
        address recipient;
        uint256 deadline;
        uint256 amountIn;
        uint256 amountOutMinimum;
    }
    struct ExactOutputSingleParams {
        address tokenIn;
        address tokenOut;
        uint24 fee;
        address recipient;
        uint256 deadline;
        uint256 amountOut;
        uint256 amountInMaximum;
        uint160 sqrtPriceLimitX96;
    }
    struct ExactOutputParams {
        bytes path;
        address recipient;
        uint256 deadline;
        uint256 amountOut;
        uint256 amountInMaximum;
    }
    function exactInputSingle(ExactInputSingleParams calldata params) external payable returns (uint256 amountOut) {
        // only verify consumed token and amount when not using eth as input
        if (msg.value >= params.amountIn && params.tokenIn == getWethAddress(msg.sender)) {
            consumedToken = address(0);
        } else {
            consumedToken = params.tokenIn;
            shouldBeConsumedAmount = params.amountIn;
            IERC20WithDummyFunctionality(consumedToken).transferFrom(msg.sender, address(this), params.amountIn);
        }
        require (params.amountIn > 0 && params.amountOutMinimum > 0);
        require (params.tokenIn != address(this) && params.tokenOut != address(this));
        generatedToken = params.tokenOut;
        require (consumedToken != generatedToken);
        IERC20WithDummyFunctionality(generatedToken).transfer(params.recipient, params.amountOutMinimum);
        return params.amountOutMinimum;
    }
    function exactInput(ExactInputParams calldata params) external payable returns (uint256 amountOut) {
        address tokenIn = _getFirstToken(params.path);
        // only verify consumed token and amount when not using eth as input
        if (msg.value >= params.amountIn && tokenIn == getWethAddress(msg.sender)) {
            consumedToken = address(0);
        } else {
            consumedToken = tokenIn;
            shouldBeConsumedAmount = params.amountIn;
            IERC20WithDummyFunctionality(consumedToken).transferFrom(msg.sender, address(this), params.amountIn);
        }
        generatedToken = _getLastToken(params.path);
        require (params.amountIn > 0 && params.amountOutMinimum > 0);
        require (consumedToken != address(this) && generatedToken != address(this));
        require (consumedToken != generatedToken);
        IERC20WithDummyFunctionality(generatedToken).transfer(params.recipient, params.amountOutMinimum);
        return params.amountOutMinimum;
    }
    function exactOutputSingle(ExactOutputSingleParams calldata params) external payable returns (uint256 amountIn) {
        // only verify consumed token and amount when not using eth as input
        if (msg.value >= params.amountInMaximum && params.tokenIn == getWethAddress(msg.sender)) {
            consumedToken = address(0);
        } else {
            consumedToken = params.tokenIn;
            shouldBeConsumedAmount = params.amountInMaximum;
            IERC20WithDummyFunctionality(consumedToken).transferFrom(msg.sender, address(this), params.amountInMaximum);
        }
        require (params.amountInMaximum > 0 && params.amountOut > 0);
        require (params.tokenIn != address(this) && params.tokenOut != address(this));
        generatedToken = params.tokenOut;
        require (consumedToken != generatedToken);
        IERC20WithDummyFunctionality(generatedToken).transfer(params.recipient, params.amountOut);
        return params.amountInMaximum;
    }
    function exactOutput(ExactOutputParams calldata params) external payable returns (uint256 amountIn) {
        address tokenIn = _getLastToken(params.path);
        // only verify consumed token and amount when not using eth as input
        if (msg.value >= params.amountInMaximum && tokenIn == getWethAddress(msg.sender)) {
            consumedToken = address(0);
        } else {
            consumedToken = tokenIn;
            shouldBeConsumedAmount = params.amountInMaximum;
            IERC20WithDummyFunctionality(consumedToken).transferFrom(msg.sender, address(this), params.amountInMaximum);
        }
        generatedToken = _getFirstToken(params.path);
        require (params.amountInMaximum > 0 && params.amountOut > 0);
        require (consumedToken != address(this) && generatedToken != address(this));
        require (consumedToken != generatedToken);
        shouldBeConsumedAmount = params.amountInMaximum;
        IERC20WithDummyFunctionality(generatedToken).transfer(params.recipient, params.amountOut);
        return params.amountInMaximum;
    }
    function refundETH() external payable {
        Nothing(msg.sender).nop{value:0}();
    }

    // HKyberNetwork
    // function swapTokenToToken(address src, uint srcAmount, address dest, uint minConversionRate) external returns(uint) {
    //     consumedToken = src;
    //     generatedToken = dest;
    //     shouldBeConsumedAmount = srcAmount;
    //     IERC20WithDummyFunctionality(src).transferFrom(msg.sender, address(this), srcAmount);
    //     IERC20WithDummyFunctionality(dest).transfer(msg.sender, someAmount);
    // }
    // function swapEtherToToken(address token, uint minConversionRate) external payable returns(uint) {
    //     generatedToken = token;
    //     IERC20WithDummyFunctionality(token).transfer(msg.sender, someAmount);
    // }
    // function swapTokenToEther(address token, uint srcAmount, uint minConversionRate) external returns(uint) {
    //     consumedToken = token;
    //     shouldBeConsumedAmount = srcAmount;
    //     IERC20WithDummyFunctionality(token).transferFrom(msg.sender, address(this), srcAmount);
    //     Nothing(msg.sender).nop{value:someAmount}();
    // }

    // HBalancer
    function exitPool(uint256 poolAmountIn, uint256[] calldata minAmountsOut) external {
        consumedToken = address(this);
        shouldBeConsumedAmount = poolAmountIn;
        transferFrom(msg.sender, address(0), poolAmountIn);
    }
    function exitswapPoolAmountIn(address tokenOut, uint256 poolAmountIn, uint256 minAmountOut) external payable returns (uint256 tokenAmountOut) {
        consumedToken = address(this);
        shouldBeConsumedAmount = poolAmountIn;
        generatedToken = tokenOut;
        transferFrom(msg.sender, address(0), poolAmountIn);
        IERC20WithDummyFunctionality(tokenOut).transfer(msg.sender, minAmountOut);
    }

    // HGasTokens
    function freeFromUpTo(address from, uint256 value)
        external
        returns (uint256) {
            consumedToken = address(this);
            shouldBeConsumedAmount = value;
            transferFrom(from, address(0), value);
        }

    // HMooniswap
    // function deposit(uint256[] calldata amounts, uint256[] calldata minAmounts) external payable returns(uint256) {
    //     // two tokens here
    //     consumedToken = address(erc20A);
    //     shouldBeConsumedAmount = amounts[0];
    //     require (erc20A < erc20B);
    //     erc20A.transferFrom(msg.sender, address(this), amounts[0]);
    //     erc20B.transferFrom(msg.sender, address(this), amounts[1]);
    //     generatedToken = address(this);
    //     transfer(msg.sender, someAmount);
    //     return someAmount;
    // }
    // function withdraw(uint256 amount, uint256[] calldata minAmounts) external {
    //     generatedToken = address(erc20A);
    //     consumedToken = address(this);
    //     shouldBeConsumedAmount = amount;
    //     transferFrom(msg.sender, address(this), amount);
    //     erc20A.transfer(msg.sender, minAmounts[0]);
    //     erc20B.transfer(msg.sender, minAmounts[1]);
    // }
    // function getTokens() external returns (address[] memory) {
    //     address[] memory ret = new address[](2);
    //     ret[0] = address(erc20A);
    //     ret[1] = address(erc20B);
    //     return ret;
    // }

    // HStakingRewardsAdapter, partially HFurucomboStaking
    function stakingToken() external view returns (address) {
        return address(erc20A);
    }
    function rewardsToken() external view returns (address) {
        return address(erc20B);   
    }
    function stakeFor(address account, uint256 amount) external {
        consumedToken = address(erc20A);
        shouldBeConsumedAmount = amount;
        erc20A.transferFrom(account, address(this), amount);
    }
    function withdrawFor(address account, uint256 amount) external {
        generatedToken = address(erc20A);
        erc20A.transfer(account, amount);
    }
    function getRewardFor(address account) external {
        generatedToken = address(erc20B);
        erc20B.transfer(msg.sender, someAmount);
    }
    function exitFor(address account) external {
        generatedToken = address(erc20A);
        erc20A.transfer(msg.sender, someAmount);
    }

    // HFurucomboStaking
    function unstakeFor(address account, uint256 amount) external {
        generatedToken = address(erc20A);
        erc20A.transfer(account, amount);
    }
    struct Claim {
        uint256 week;
        uint256 balance;
        bytes32[] merkleProof;
    }
    function claimWeeks(address user, Claim[] calldata claim) external {
        havocDummyToken();
    }

    // HCToken
    // underlying is ERC20A
    function mint(uint256 mintAmount) external returns (uint256) {
        require (address(erc20A) != address(this)); // underlying != cToken by comptroller
        consumedToken = address(erc20A);
        shouldBeConsumedAmount = mintAmount;
        generatedToken = address(this);
        uint rc;
        if ((mintAmount == 0 && someAmount == 0) || (mintAmount > 0 && someAmount > 0)) {
            rc = 0;
            erc20A.transferFrom(msg.sender, address(this), mintAmount);
            transferFrom(address(0), msg.sender, someAmount);
        } else {
            rc = 1;
        }
        return rc;
    }
    /* HCEther */ function mint() external payable returns (uint256) {
        uint mintAmount = msg.value;
        generatedToken = address(this);
        uint rc;
        if ((mintAmount == 0 && someAmount == 0) || (mintAmount > 0 && someAmount > 0)) {
            rc = 0;
            transferFrom(address(0), msg.sender, someAmount);
        } else {
            rc = 1;
        }
        return rc;
    }
    function compoundredeem(uint256 redeemTokens) external returns (uint256) {
        require (address(erc20A) != address(this)); // underlying != cToken by comptroller
        consumedToken = address(this);
        shouldBeConsumedAmount = redeemTokens;
        generatedToken = address(erc20A);
        uint rc;
        if ((redeemTokens == 0 && someAmount == 0) || (redeemTokens > 0 && someAmount > 0)) {
            rc = 0;
            transferFrom(msg.sender, address(0), redeemTokens);
            erc20A.transfer(msg.sender, someAmount);
        } else {
            rc = 1;
        }
        return rc;
    }
    function redeemUnderlying(uint256 redeemAmount) external returns (uint256) {
        require (address(erc20A) != address(this)); // underlying != cToken by comptroller
        consumedToken = address(this);
        shouldBeConsumedAmount = someAmount;
        generatedToken = address(erc20A);
        uint rc;
        if ((redeemAmount == 0 && someAmount == 0) || (redeemAmount > 0 && someAmount > 0)) {
            rc = 0;
            transferFrom(msg.sender, address(0), someAmount);
            erc20A.transfer(msg.sender, redeemAmount);
        } else {
            rc = 1;
        }
        return rc;
    }
    function repayBorrowBehalf(address borrower, uint256 debt) external returns (uint256) {
        require (address(erc20A) != address(this)); // underlying != cToken by comptroller
        consumedToken = address(erc20A);
        uint pay = debt;
        shouldBeConsumedAmount = pay;
        erc20A.transferFrom(msg.sender, address(this), pay);
        compoundDebt[borrower] = sub(compoundDebt[borrower],pay);
        return 0;
    }
    /* HCEther */function repayBorrowBehalf(address borrower) external payable returns (uint256) {
        uint pay = msg.value;
        compoundDebt[borrower] = sub(compoundDebt[borrower],pay);
        return 0;
    }
    mapping (address => uint256) compoundDebt;
    uint interest;
    function borrowBalanceCurrent(address borrower) external returns (uint256) {
        compoundDebt[borrower] = add(compoundDebt[borrower],interest);
        return compoundDebt[borrower];
    }

    // HCurve
    mapping (int128 => address) indexToToken;
    function correctIndexing(int128 i, int128 j) private {
        require (indexToToken[i] != indexToToken[j]);
    }
    function exchange(
        int128 i,
        int128 j,
        uint256 dx,
        uint256 min_dy
    ) external payable {
        correctIndexing(i,j);
        IERC20WithDummyFunctionality tokenI = IERC20WithDummyFunctionality(indexToToken[i]);
        IERC20WithDummyFunctionality tokenJ = IERC20WithDummyFunctionality(indexToToken[j]);
        consumedToken = address(tokenI);
        generatedToken = address(tokenJ);
        shouldBeConsumedAmount = dx;
        tokenI.transferFrom(msg.sender, address(this), dx);
        tokenJ.transfer(msg.sender, min_dy);
    }

    function exchange_underlying(
        int128 i,
        int128 j,
        uint256 dx,
        uint256 min_dy
    ) external payable {
        correctIndexing(i,j);
        IERC20WithDummyFunctionality tokenI = IERC20WithDummyFunctionality(indexToToken[i]);
        IERC20WithDummyFunctionality tokenJ = IERC20WithDummyFunctionality(indexToToken[j]);
        consumedToken = address(tokenI);
        generatedToken = address(tokenJ);
        shouldBeConsumedAmount = dx;
        tokenI.transferFrom(msg.sender, address(this), dx);
        tokenJ.transfer(msg.sender, min_dy);
    }

    function add_liquidity(uint256[2] calldata amounts, uint256 min_mint_amount)
        external
        payable {
            // we do not model in transfers
            transfer(msg.sender, min_mint_amount);
        }

    function add_liquidity(uint256[3] calldata amounts, uint256 min_mint_amount)
        external
        payable {
            // we do not model in transfers
            transfer(msg.sender, min_mint_amount);
        }

    function add_liquidity(uint256[4] calldata amounts, uint256 min_mint_amount)
        external
        payable {
            // we do not model in transfers
            transfer(msg.sender, min_mint_amount);
        }

    function add_liquidity(uint256[5] calldata amounts, uint256 min_mint_amount)
        external
        payable {
            // we do not model in transfers
            transfer(msg.sender, min_mint_amount);
        }

    function add_liquidity(uint256[6] calldata amounts, uint256 min_mint_amount)
        external
        payable {
            // we do not model in transfers
            transfer(msg.sender, min_mint_amount);
        }

    function add_liquidity(
        uint256[2] calldata amounts,
        uint256 min_mint_amount,
        bool use_underlying
    ) external payable {
        // we do not model in transfers
        transfer(msg.sender, min_mint_amount);
    }

    function add_liquidity(
        uint256[3] calldata amounts,
        uint256 min_mint_amount,
        bool use_underlying
    ) external payable {
        // we do not model in transfers
        transfer(msg.sender, min_mint_amount);
    }

    function add_liquidity(
        uint256[4] calldata amounts,
        uint256 min_mint_amount,
        bool use_underlying
    ) external payable {
        // we do not model in transfers
        transfer(msg.sender, min_mint_amount);
    }

    function add_liquidity(
        uint256[5] calldata amounts,
        uint256 min_mint_amount,
        bool use_underlying
    ) external payable {
        // we do not model in transfers
        transfer(msg.sender, min_mint_amount);
    }

    function add_liquidity(
        uint256[6] calldata amounts,
        uint256 min_mint_amount,
        bool use_underlying
    ) external payable {
        // we do not model in transfers
        transfer(msg.sender, min_mint_amount);
    }

    function remove_liquidity_one_coin(
        uint256 _token_amount,
        int128 i,
        uint256 min_amount
    ) external {
        IERC20WithDummyFunctionality tokenI = IERC20WithDummyFunctionality(indexToToken[i]);
        require (address(tokenI) != address(this));
        consumedToken = address(this);
        shouldBeConsumedAmount = _token_amount;
        generatedToken = address(tokenI);
        transferFrom(msg.sender, address(this), _token_amount);
        tokenI.transfer(msg.sender, min_amount);
    }

    function remove_liquidity_one_coin(
        uint256 _token_amount,
        int128 i,
        uint256 min_uamount,
        bool boolean // donate_dust or use_underlying
    ) external {
        IERC20WithDummyFunctionality tokenI = IERC20WithDummyFunctionality(indexToToken[i]);
        require (address(tokenI) != address(this));
        consumedToken = address(this);
        shouldBeConsumedAmount = _token_amount;
        generatedToken = address(tokenI);
        transferFrom(msg.sender, address(this), _token_amount);
        tokenI.transfer(msg.sender, min_uamount);
    }

    // HCurveDao
    // erc20B will be CRV
    function mint_for(address gaugeAddr,address user) external payable {
        generatedToken = address(erc20B);
        erc20B.transfer(user, someAmount);
    }
    function deposit(uint256 value, address user) external payable {
        // gauge address will point to erc20A
        consumedToken = address(erc20A);
        shouldBeConsumedAmount = value;
        erc20A.transferFrom(msg.sender, address(this), value);
    }

    // HYVault
    // the underlying vault token is erc20A
    function deposit(uint256 a) external payable {
        consumedToken = address(erc20A);
        shouldBeConsumedAmount = a;
        generatedToken = address(this);
        erc20A.transferFrom(msg.sender, address(this), a);
        transfer(msg.sender, someAmount);
    }

    function depositETH() external payable {
        generatedToken = address(this);
        transfer(msg.sender, someAmount);
    }

    function yvault_withdraw(uint256 a) external payable {
        consumedToken = address(this);
        shouldBeConsumedAmount = a;
        generatedToken = address(erc20A);
        transferFrom(msg.sender, address(this), a);
        erc20A.transfer(msg.sender, someAmount);
    }

    function withdrawETH(uint256 a) external payable {
        consumedToken = address(this);
        shouldBeConsumedAmount = a;
        transferFrom(msg.sender, address(this), a);
        Nothing(msg.sender).nop{value:someAmount}();
    }

    // HPolygon
    function depositERC20ForUser(address token, address user, uint256 amount) external {
        consumedToken = token;
        generatedToken = address(0);
        shouldBeConsumedAmount = amount;
        IERC20WithDummyFunctionality(token).transferFrom(msg.sender, address(this), amount);
    }
    function depositFor(address user, address token, bytes calldata depositData) external {
        consumedToken = token;
        generatedToken = address(0);
        uint256 amount = abi.decode(depositData, (uint256));
        shouldBeConsumedAmount = amount;
        IERC20WithDummyFunctionality(token).transferFrom(msg.sender, address(this), amount);
    }
    function depositEtherFor(address user) external payable {
        consumedToken = address(0);
        generatedToken = address(0);
        shouldBeConsumedAmount = msg.value;
    }

    // HGelatoV2LimitOrder
    function encodeEthOrder(
        address _module,
        address _inputToken,
        address payable _owner,
        address _witness,
        bytes calldata _data,
        bytes32 _secret
    ) external pure returns (bytes memory) {
        return
            abi.encode(_module, _inputToken, _owner, _witness, _data, _secret);
    }
    function depositEth(bytes calldata _data) external payable {
        consumedToken = address(0);
        shouldBeConsumedAmount = msg.value;
    }

    address public consumedToken;
    address public generatedToken;
    uint public shouldBeConsumedAmount;
    function getBalance(address token, address who) public returns (uint) { return IERC20WithDummyFunctionality(token).balanceOf(who); }
}