// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ZeroAddress {
    address public owner;

    function setOwner(address _owner) public {
        owner = _owner; // no zero check
    }
}