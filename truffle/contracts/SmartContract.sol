// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SmartContract {
    // Struct to store compatibility results
    struct Compatibility {
        uint256 donorId;
        uint256 recipientId;
        uint256 compatibilityScore;
        bool isCompatible;
    }

    // Struct to store transaction details
    struct Transaction {
        uint256 donorId;
        uint256 recipientId;
        string organType;
        uint256 timestamp;
    }

    // Struct to store file metadata
    struct File {
        string cid; // IPFS CID
        string description; // File description (e.g., "Medical Record")
    }

    // Mappings to store data
    mapping(uint256 => Compatibility) public compatibilities;
    mapping(uint256 => Transaction[]) public transactions;
    mapping(uint256 => File[]) public files;

    // Events to log important actions
    event CompatibilityStored(uint256 donorId, uint256 recipientId, uint256 compatibilityScore, bool isCompatible);
    event TransactionRecorded(uint256 donorId, uint256 recipientId, string organType, uint256 timestamp);
    event FileMetadataStored(uint256 userId, string cid, string description);

    // Function to store compatibility results
    function storeCompatibility(uint256 donorId, uint256 recipientId, uint256 compatibilityScore, bool isCompatible) public {
        compatibilities[donorId] = Compatibility(donorId, recipientId, compatibilityScore, isCompatible);
        emit CompatibilityStored(donorId, recipientId, compatibilityScore, isCompatible);
    }

    // Function to record a transaction
    function recordTransaction(uint256 donorId, uint256 recipientId, string memory organType) public {
        transactions[donorId].push(Transaction(donorId, recipientId, organType, block.timestamp));
        emit TransactionRecorded(donorId, recipientId, organType, block.timestamp);
    }

    // Function to store file metadata
    function storeFileMetadata(uint256 userId, string memory cid, string memory description) public {
        files[userId].push(File(cid, description));
        emit FileMetadataStored(userId, cid, description);
    }

    // Function to get compatibility results
    function getCompatibility(uint256 donorId) public view returns (Compatibility memory) {
        return compatibilities[donorId];
    }

    // Function to get transaction history
    function getTransactionHistory(uint256 donorId) public view returns (Transaction[] memory) {
        return transactions[donorId];
    }

    // Function to get file metadata
    function getFileMetadata(uint256 userId) public view returns (File[] memory) {
        return files[userId];
    }
}
