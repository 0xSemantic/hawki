// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InputValidation {
    uint256[] public array;

    function get(uint256 index) public view returns (uint256) {
        return array[index]; // no bounds check
    }
}