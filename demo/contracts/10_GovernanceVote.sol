// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GovernanceVote {
    mapping(address => uint256) public votes;

    function vote(uint256 proposalId) public {
        uint256 votingPower = token.balanceOf(msg.sender); // uses current balance
        votes[msg.sender] += votingPower;
    }
}