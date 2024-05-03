certoraRun specs/harnesses/LibParamHarness.sol \
    --verify LibParamHarness:specs/libParam.spec \
    --settings -b=64,-smt_bitVectorTheory=true \
    --msg "LibParam"
