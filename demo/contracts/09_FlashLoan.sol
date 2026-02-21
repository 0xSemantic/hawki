// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FlashLoanVulnerable {
    mapping(address => uint256) public balances;

    function swap(uint256 amount) public returns (uint256) {
        uint256 price = getPrice(); // uses spot price
        // ... swap logic ...
    }
}