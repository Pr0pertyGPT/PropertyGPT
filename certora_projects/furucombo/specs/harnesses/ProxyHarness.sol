pragma solidity ^0.8.0;

import "../../contracts/Proxy.sol";

contract ProxyHarness is Proxy {
    constructor(address registry) public Proxy(registry) {}

    function getSlot(uint256 s) external view returns (uint256 x) {
        assembly {
            x := sload(s)
        }
    }

    function getStackLengthSlot() external view returns (uint256 x) {
        assembly {
            x := stack_slot
        }
    }

    function getStackLength() external view returns (uint256) {
        return stack.length;
    }

    function ethBalance(address who) external view returns (uint256) {
        return who.balance;
    }

    // internal-to-public
    function getSender() public view returns (address) {
        return _getSender();
    }

    function getCubeCounter() public view returns (uint256) {
        return _getCubeCounter();
    }

    // to distinguish handlers from proxy
    function isHandler() public view returns (bool) {
        return false;
    }

    // to align with handlers, but not existing here
    function postProcess() external {
        revert();
    }

    // simplifying summaries of certain functions in proxy
    function _parse(
        bytes32[2] memory localStack,
        bytes memory ret,
        uint256 index
    ) internal pure override returns (uint256) {
        uint256 sz = ret.length / 32;
        uint256 newIndex = index + sz;
        require(newIndex <= 2);

        for (uint256 i = 0; i < sz; i++) {
            localStack[index + i * 32] = ret[i * 32];
        }

        return newIndex;
    }

    function _trim(
        bytes memory data,
        bytes32 config,
        bytes32[2] memory localStack,
        uint256 index
    ) internal pure override {
        // no-op
    }

    address dummy;

    function _exec(address _to, bytes memory _data)
        internal
        override
        returns (bytes memory result)
    {
        require(_isValidHandler(_to), "Invalid handler");
        _addCubeCounter();
        bool success;
        (success, result) = dummy.call(abi.encodeWithSelector(0x12345678));
    }

    // should be optional once issue is resolved
    function _execs(
        address[] memory tos,
        bytes32[] memory configs,
        bytes[] memory datas
    ) internal override {
        bytes32[2] memory localStack;
        uint256 index = 0;
        require(tos.length == 1);
        require(configs.length == 1);
        require(datas.length == 1);
        address to = tos[0];
        bytes32 config = configs[0];
        bytes memory data = datas[0];
        if (!config.isStatic()) {
            // If so, trim the exectution data base on the configuration and stack content
            _trim(data, config, localStack, index);
        }
        // Check if the output will be referenced afterwards
        if (config.isReferenced()) {
            // If so, parse the output and place it into local stack
            uint256 num = config.getReturnNum();
            uint256 newIndex = _parse(localStack, _exec(to, data), index);
            require(
                newIndex == index + num,
                "Return num and parsed return num not matched"
            );
            index = newIndex;
        } else {
            _exec(to, data);
        }
        // Setup the process to be triggered in the post-process phase
        _setPostProcess(to);
    }
}
