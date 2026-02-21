// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DoS {
    address[] public users;

    function addUser(address user) public {
        users.push(user);
    }

    function payAll() public {
        for (uint i = 0; i < users.length; i++) {
            payable(users[i]).transfer(1 ether);
        }
    }
}