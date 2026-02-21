// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PermitReplay {
    mapping(address => uint256) public nonces;

    function permit(...) public {
        // no nonce check
    }
}