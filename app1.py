import datetime
import hashlib
import json
import streamlit as st

# --- 1. Blockchain Logic ---
class Blockchain:
    def __init__(self, difficulty):
        self.chain = []
        self.difficulty = difficulty
        # We mine the very first block so it starts as "Valid"
        self.create_genesis_block()

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

    def create_genesis_block(self):
        # Find a valid proof for the first block
        proof = self.proof_of_work(0)
        self.create_block(proof, '0', "Genesis Block")

    def hash(self, block):
        # sort_keys=True is vital for consistent hashing
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # This logic mimics the "puzzle" found in real blockchains
            hash_op = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_op[:self.difficulty] == '0' * self.difficulty:
                check_proof = True
            else:
                new_proof += 1
        return new_proof

# --- 2. Streamlit UI Setup ---
st.set_page_config(page_title="Blockchain Lab", layout="wide")
st.title("⛓️ Fully Validated Blockchain Lab")

# Sidebar Configuration
st.sidebar.header("Configuration")
difficulty = st.sidebar.slider("Mining Difficulty", 1, 4, 2)

# Initialization
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain(difficulty)

# --- 3. Sidebar Controls ---
st.sidebar.header("Actions")
if st.sidebar.button("⛏️ Mine New Block"):
    bc = st.session_state.blockchain
    bc.difficulty = difficulty # Update difficulty if changed
    prev_block = bc.get_previous_block()
    
    with st.sidebar.status("Mining..."):
        new_proof = bc.proof_of_work(prev_block['proof'])
        new_block = bc.create_block(new_proof, bc.hash(prev_block))
    st.sidebar.success(f"Block #{new_block['index']} Mined!")

if st.sidebar.button("♻️ Reset Chain"):
    st.session_state.blockchain = Blockchain(difficulty)
    st.rerun()

# --- 4. Display & Validation ---
st.subheader("The Blockchain Ledger")



chain = st.session_state.blockchain.chain
corrupted = False

for i, block in enumerate(chain):
    # Calculate current hash on the fly
    current_hash = st.session_state.blockchain.hash(block)
    
    # 1. Check Proof of Work (Does it have the required zeros?)
    pow_valid = current_hash.startswith('0' * difficulty)
    
    # 2. Check Link (Does previous_hash match the actual hash of the last block?)
    link_valid = True
    if i > 0:
        actual_prev_hash = st.session_state.blockchain.hash(chain[i-1])
        if block['previous_hash'] != actual_prev_hash:
            link_valid = False
    
    # If THIS block is wrong OR a previous one was, mark it as corrupted
    if not pow_valid or not link_valid:
        corrupted = True

    # Render Block
    with st.expander(f"📦 Block #{block['index']}", expanded=True):
        col1, col2 = st.columns([3, 2])
        with col1:
            # Edit data to trigger tampering
            new_data = st.text_input(f"Data", value=block['data'], key=f"input_{i}")
            chain[i]['data'] = new_data
            
            st.write(f"**Hash:** `{current_hash}`")
            st.write(f"**Prev Hash:** `{block['previous_hash']}`")
        
        with col2:
            if not corrupted:
                st.success("✅ VALID")
            else:
                st.error("❌ INVALID")
                if not pow_valid:
                    st.caption("Proof of Work broken (Hash changed).")
                if not link_valid:
                    st.caption("Chain link broken (Previous hash mismatch).")

# Global Status
if corrupted:
    st.sidebar.error("Status: TAMPERED ❌")
else:
    st.sidebar.success("Status: SECURE ✅")
