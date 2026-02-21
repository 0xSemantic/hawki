// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UninitializedStorage {
    struct Data { uint256 a; uint256 b; }
    Data public data;

    function write() public {
        Data storage d; // uninitialized
        d.a = 42;
    }
}