// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TxOriginAuth {
    address public owner;

    function withdraw() public {
        require(tx.origin == owner);
        payable(msg.sender).transfer(address(this).balance);
    }
}