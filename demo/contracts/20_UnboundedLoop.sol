// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UnboundedLoop {
    address[] public users;

    function distribute() public {
        for (uint i = 0; i < users.length; i++) {
            payable(users[i]).transfer(1 ether);
        }
    }
}