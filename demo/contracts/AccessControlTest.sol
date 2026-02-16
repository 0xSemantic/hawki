// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title AccessControlTest
 * @dev Misconfigured access control: critical functions are public.
 */
contract AccessControlTest {
    address public admin;
    mapping(address => bool) public allowed;

    constructor() {
        admin = msg.sender;
    }

    // Should be restricted to admin
    function addAllowed(address user) public {
        allowed[user] = true;
    }

    // Should be restricted to admin
    function removeAllowed(address user) public {
        allowed[user] = false;
    }

    // Anyone can change admin? No, but missing modifier makes admin variable writable?
    // Actually admin is just a public variable, not a function. To change admin we'd need a setter.
    // So no direct vulnerability here, but the allowed functions are unprotected.
}