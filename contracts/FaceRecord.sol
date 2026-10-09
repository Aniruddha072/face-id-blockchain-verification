// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FaceRecord {
    struct Record {
        bytes32 recordHash;
        string metadataURI; // IPFS CID, or "" if you skip IPFS
        address submitter;
        uint256 timestamp;
        uint8 modelsAgreed; // how many face-verification models confirmed the match
        uint8 modelsTotal; // how many models were tried
    }

    mapping(bytes32 => Record) public records; // keyed by recordHash

    event RecordStored(
        address indexed submitter,
        bytes32 indexed recordHash,
        string metadataURI,
        uint256 timestamp,
        uint8 modelsAgreed,
        uint8 modelsTotal
    );

    function storeRecord(
        bytes32 recordHash,
        string calldata metadataURI,
        uint8 modelsAgreed,
        uint8 modelsTotal
    ) external {
        records[recordHash] = Record(recordHash, metadataURI, msg.sender, block.timestamp, modelsAgreed, modelsTotal);
        emit RecordStored(msg.sender, recordHash, metadataURI, block.timestamp, modelsAgreed, modelsTotal);
    }

    function getRecord(bytes32 recordHash) external view returns (Record memory) {
        return records[recordHash];
    }
}
