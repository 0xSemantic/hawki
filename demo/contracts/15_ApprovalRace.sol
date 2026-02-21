// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ApprovalRace {
    mapping(address => mapping(address => uint256)) public allowance;

    function approve(address spender, uint256 amount) public returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }
}