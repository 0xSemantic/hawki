// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CrossFunctionReentrancy {
    mapping(address => uint256) public balances;

    function withdraw() public {
        uint256 bal = balances[msg.sender];
        require(bal > 0);
        (bool success, ) = msg.sender.call{value: bal}("");
        require(success);
        // state update is in another function
    }

    function updateBalance() public {
        balances[msg.sender] = 0;
    }
}