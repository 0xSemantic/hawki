// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UpgradeAdmin {
    address public admin;

    function changeAdmin(address _newAdmin) public {
        admin = _newAdmin; // anyone can change admin
    }
}