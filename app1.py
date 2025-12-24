import datetime
import hashlib
import json
import streamlit as st

# --- 1. Blockchain Logic ---
class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 2 # Number of leading zeros required for mining
        # Create the Genesis Block
        self.create_block(proof=1, previous_hash='0', data="Genesis Block")

    def create_block(self, proof, previous_hash, data="Block Data"):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'data': data
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def hash(self, block):
        # We must sort the keys to ensure the hash is always the same for the same data
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:self.difficulty] == '0' * self.difficulty:
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def is_chain_valid(self, chain):
        for i in range(1, len(chain)):
            if chain[i]['previous_hash'] != self.hash(chain[i-1]):
                return False
        return True

# --- 2. Streamlit UI Setup ---
st.set_page_config(page_title="Blockchain Ripple Lab", layout="wide")
st.title("⛓️ Blockchain 'Ripple Effect' Lab")
st.markdown("""
    Change the data in any block to see how it invalidates **every single block** that follows it.
""")

# Initialize or Reset the Blockchain in Session State
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

# --- 3. Sidebar Controls ---
st.sidebar.header("Controls")

if st.sidebar.button("⛏️ Mine New Block"):
    bc = st.session_state.blockchain
    prev_block = bc.get_previous_block()
    
    with st.sidebar.status("Computing Hash..."):
        new_proof = bc.proof_of_work(prev_block['proof'])
        # Link the new block to the hash of the
