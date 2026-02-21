// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GasGriefing {
    uint256[] public data;

    function process() public {
        for (uint i = 0; i < data.length; i++) {
            // expensive operation
        }
    }
}