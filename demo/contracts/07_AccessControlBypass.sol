// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AccessControlBypass {
    address public owner;

    function setOwner(address _newOwner) public {
        owner = _newOwner; // anyone can change owner
    }
}