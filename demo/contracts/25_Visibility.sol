// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Visibility {
    function _internal() public { // should be internal
        // sensitive logic
    }
}