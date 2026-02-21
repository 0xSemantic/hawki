// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract OracleManipulation {
    mapping(address => uint256) public reserves;

    function getPrice() public view returns (uint256) {
        return reserves[address(0xA)] / reserves[address(0xB)];
    }
}