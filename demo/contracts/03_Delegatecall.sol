// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DelegatecallExample {
    address public implementation;
    uint256 public data;

    function execute(address _impl, bytes memory _data) public {
        (bool success, ) = _impl.delegatecall(_data);
        require(success);
        implementation = _impl;
    }
}