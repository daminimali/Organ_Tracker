const SmartContract = artifacts.require("SmartContract");

contract("SmartContract", (accounts) => {
    let contractInstance;

    before(async () => {
        contractInstance = await SmartContract.deployed();
    });

    it("should store and retrieve compatibility results", async () => {
        await contractInstance.storeCompatibility(1, 2, 85, true);
        let result = await contractInstance.getCompatibility(1);
        
        assert.equal(result.donorId, 1, "Incorrect donor ID");
        assert.equal(result.recipientId, 2, "Incorrect recipient ID");
        assert.equal(result.compatibilityScore, 85, "Incorrect compatibility score");
        assert.equal(result.isCompatible, true, "Incorrect compatibility result");
    });

    it("should record and retrieve organ donation transactions", async () => {
        await contractInstance.recordTransaction(1, 2, "Kidney");
        let history = await contractInstance.getTransactionHistory(1);
        
        assert.equal(history.length, 1, "Transaction not recorded");
        assert.equal(history[0].donorId, 1, "Incorrect donor ID");
        assert.equal(history[0].recipientId, 2, "Incorrect recipient ID");
        assert.equal(history[0].organType, "Kidney", "Incorrect organ type");
    });

    it("should store and retrieve file metadata", async () => {
        await contractInstance.storeFileMetadata(1, "Qm12345", "Medical Record");
        let files = await contractInstance.getFileMetadata(1);
        
        assert.equal(files.length, 1, "File metadata not stored");
        assert.equal(files[0].cid, "Qm12345", "Incorrect CID");
        assert.equal(files[0].description, "Medical Record", "Incorrect description");
    });
});
