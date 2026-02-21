// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UnsafeExternalCall {
    function withdraw() public {
        uint amount = balances[msg.sender];
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);
        balances[msg.sender] = 0; // update after call
    }
}