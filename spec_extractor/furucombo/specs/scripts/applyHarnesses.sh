# Virtualize
perl -0777 -i -pe 's/(function _parse\(\s*bytes32\[256\] memory localStack,\s*bytes memory ret,\s*uint256 index\s*\)) internal/\1 virtual internal/g' contracts/Proxy.sol
perl -0777 -i -pe 's/(function _trim\(\s*bytes memory data,\s*bytes32 config,\s*bytes32\[256\] memory localStack,\s*uint256 index\s*\)) internal/\1 virtual internal/g' contracts/Proxy.sol
perl -0777 -i -pe 's/(function _exec\(address _to, bytes memory _data\))\s*internal/\1 virtual internal/g' contracts/Proxy.sol
perl -0777 -i -pe 's/(function _execs\(\s*address\[\] memory tos,\s*bytes32\[\] memory configs,\s*bytes\[\] memory datas\s*\)) internal/\1 virtual internal/g' contracts/Proxy.sol


# 256 to 2 [or whatever bound we choose in -b]
perl -0777 -i -pe 's/bytes32\[256\]/bytes32\[2\]/g' contracts/Proxy.sol
perl -0777 -i -pe 's/bytes32\[256\]/bytes32\[2\]/g' specs/harnesses/ProxyHarness.sol
perl -0777 -i -pe 's/require\(newIndex <= 256\);/require\(newIndex <= 2\);/g' specs/harnesses/ProxyHarness.sol

# Temporary internal to public
#perl -0777 -i -pe 's/internal/public/g' contracts/Proxy.sol
#perl -0777 -i -pe 's/internal/public/g' specs/harnesses/ProxyHarness.sol

# Append Nothing interface for controlling havocs by transfers
echo "interface Nothing { function nop() external payable; }" >> contracts/handlers/HandlerBase.sol
