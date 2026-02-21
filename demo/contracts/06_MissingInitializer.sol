// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

contract MissingInitializer is Initializable {
    address public owner;

    function initialize() public {
        owner = msg.sender; // missing initializer modifier
    }
}