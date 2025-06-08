export const fetchDataFromIPFS = async (cid) => {
    try {
      const response = await fetch(`https://ipfs.io/ipfs/${cid}`);
      if (!response.ok) throw new Error("Failed to fetch IPFS data");
  
      const data = await response.json();
      return data;
    } catch (err) {
      console.error("Error fetching IPFS data:", err);
      return null;
    }
  };
  