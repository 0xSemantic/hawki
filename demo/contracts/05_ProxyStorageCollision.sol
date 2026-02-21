// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Implementation {
    uint256 public value;
}

contract Proxy {
    address public implementation;
    uint256 public value; // same slot as Implementation.value? collision!
    function upgrade(address _newImpl) public {
        implementation = _newImpl;
    }
}