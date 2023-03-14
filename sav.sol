// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract AchievementTracker {
    address public immutable owner;

    struct Achievement {
        string description;
        uint timestamp;
    }

    constructor() {
        owner = msg.sender;
    }

    mapping(address => Achievement[]) public achievements;

    function addAchievement(string memory description, address addr) public {
        achievements[addr].push(Achievement(description, block.timestamp));
    }

    function getAchievements(
        address user
    ) public view returns (Achievement[] memory) {
        return achievements[user];
    }

    function registerWallet() public {
        // no-op function, can be used to register a new wallet address on the blockchain
    }
}
