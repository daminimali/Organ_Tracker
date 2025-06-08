// src/utils/web3.js
import Web3 from "web3";

let web3;

if (window.ethereum) {
  web3 = new Web3(window.ethereum);
  window.ethereum.request({ method: "eth_requestAccounts" });
} else if (window.web3) {
  web3 = new Web3(window.web3.currentProvider);
} else {
  web3 = new Web3("http://localhost:8545"); // fallback
}

export default web3;
