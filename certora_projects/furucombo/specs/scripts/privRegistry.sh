certoraRun contracts/Registry.sol \
	--verify Registry:specs/privileged.spec \
	--settings -t=300,-ignoreViewFunctions \
	--msg "Registry Privileged"
