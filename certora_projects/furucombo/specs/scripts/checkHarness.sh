#!/bin/bash
B=2
certoraRun specs/harnesses/ProxyHarness.sol \
    --verify ProxyHarness:specs/sanity.spec \
    --settings -assumeUnwindCond,-b=$B --javaArgs '"-Dtopic.decompiler -Dtopic.function.builder"'
