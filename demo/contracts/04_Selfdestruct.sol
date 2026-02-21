// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SelfdestructVulnerable {
    address public owner;

    function kill() public {
        selfdestruct(payable(owner));
    }
}