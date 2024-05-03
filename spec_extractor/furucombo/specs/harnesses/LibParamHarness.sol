import "../../contracts/lib/LibParam.sol";

contract LibParamHarness {
	using LibParam for bytes32;

 	bytes32 private constant REFS_MASK =
        0x00000000000000000000000000000000000000000000000000000000000000FF;
    uint256 private constant REFS_LIMIT = 22;
	
	function isStatic(bytes32 x) external returns (bool) { return x.isStatic(); }
	function isReferenced(bytes32 x) external returns (bool) { return x.isReferenced(); }
	function getReturnNum(bytes32 x) external returns (uint256) { return x.getReturnNum(); }
	function getParams(bytes32 x) external { x.getParams(); }
	function getNumOfReferences(bytes32 conf) external returns (uint256) {
		// copied from getParams()
		uint256 n = 0;
        while (conf & REFS_MASK == REFS_MASK && n < REFS_LIMIT) {
            n++;
            conf = conf >> 8;
        }
        n = REFS_LIMIT - n;
		return n;
	}
}
