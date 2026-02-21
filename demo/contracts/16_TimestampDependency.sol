// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TimestampDependency {
    function isDeadlinePassed(uint256 deadline) public view returns (bool) {
        return block.timestamp > deadline;
    }
}