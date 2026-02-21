// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IntegerOverflowUnchecked {
    function add(uint256 x, uint256 y) public pure returns (uint256) {
        unchecked {
            return x + y;
        }
    }
}