// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FaceRegistry {

    struct Record {
        string fingerprint;
        string sourceUrl;
        uint256 timestamp;
        address registeredBy;
    }

    mapping(string => Record) private records;

    event FingerprintRegistered(
        string fingerprint,
        string sourceUrl,
        uint256 timestamp,
        address registeredBy
    );

    function registerFingerprint(
        string memory fingerprint,
        string memory sourceUrl
    ) public {
        require(
            bytes(records[fingerprint].fingerprint).length == 0,
            "Fingerprint already registered"
        );

        records[fingerprint] = Record(
            fingerprint,
            sourceUrl,
            block.timestamp,
            msg.sender
        );

        emit FingerprintRegistered(
            fingerprint,
            sourceUrl,
            block.timestamp,
            msg.sender
        );
    }

    function getRecord(
        string memory fingerprint
    )
        public
        view
        returns (
            string memory,
            string memory,
            uint256,
            address
        )
    {
        Record memory record = records[fingerprint];

        require(
            bytes(record.fingerprint).length != 0,
            "Fingerprint not found"
        );

        return (
            record.fingerprint,
            record.sourceUrl,
            record.timestamp,
            record.registeredBy
        );
    }

    function isRegistered(
        string memory fingerprint
    ) public view returns (bool) {
        return bytes(records[fingerprint].fingerprint).length != 0;
    }
}