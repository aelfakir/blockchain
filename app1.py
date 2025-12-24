import datetime
import hashlib
import json
import streamlit as st

# --- 1. Blockchain Logic ---
class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 2 
        # We now "mine" the genesis block so it starts with a valid hash
        genesis_proof = self.proof_of_work(0) 
        self.create_block(proof=genesis_proof, previous_hash='0', data="Genesis Block")

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
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # Mathematical puzzle to find a hash starting with '00'
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:self.difficulty] == '0' * self.difficulty:
                check_proof = True
            else:
                new_proof += 1
        return new_proof

# --- 2. Streamlit UI Setup ---
st.set_page_config(page_title="Blockchain Ripple Lab", layout="wide")
st.title("⛓️ Blockchain 'Ripple Effect' Lab")

if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

# --- 3. Sidebar Controls ---
st.sidebar.header("Controls")
if st.sidebar.button("⛏️ Mine New Block"):
    bc = st.session_state.blockchain
    prev_block = bc.get_previous_block()
    with st.sidebar.status("Computing Hash..."):
        new_proof = bc.proof_of_work(prev_block['proof'])
        new_block = bc.create_block(proof=new_proof, previous_hash=bc.hash(prev_block))
    st.sidebar.success(f"Block #{new_block['index']} Added!")

if st.sidebar.button("♻️ Reset Blockchain"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# --- 4. Main Ledger Display ---
st.subheader("The Distributed Ledger")

chain = st.session_state.blockchain.chain
corrupted_chain_flag = False 



for i, block in enumerate(chain):
    current_hash = st.session_state.blockchain.hash(block)
    
    # VALIDATION CHECKS
    # 1. Does this block's hash meet the difficulty?
    is_pow_valid = current_hash[:st.session_state.blockchain.difficulty] == '0' * st.session_state.blockchain.difficulty
    
    # 2. Does it link correctly to the previous block?
    link_broken = False
    if i > 0:
        actual_prev_hash = st.session_state.blockchain.hash(chain[i-1])
        if block['previous_hash'] != actual_prev_hash:
            link_broken = True

    # If the POW is wrong (tampered) OR the link is broken, this block and all following are invalid
    if not is_pow_valid or link_broken:
        corrupted_chain_flag = True

    with st.expander(f"📦 Block #{block['index']}", expanded=True):
        col1, col2 = st.columns([3, 2])
        with col1:
            # text_input triggers a rerun on every change
            user_input = st.text_input(f"Edit Data", value=block['data'], key=f"input_{i}")
            st.session_state.blockchain.chain[i]['data'] = user_input
            
            st.write(f"**Current Hash:** `{current_hash}`")
            st.write(f"**Previous Hash:** `{block['previous_hash']}`")
        
        with col2:
            if not corrupted_chain_flag:
                st.success("🔗 SECURE")
                st.caption("Hash matches Proof of Work and links are intact.")
            else:
                st.error("❌ INVALID / BROKEN")
                if not is_pow_valid:
                    st.warning("Tamper Detected: Hash does not match Proof of Work!")
                if link_broken:
                    st.warning("Link Broken: Previous hash does not match.")

# Sidebar Global Status
if corrupted_chain_flag:
    st.sidebar.error("Global Status: TAMPERED ❌")
else:
    st.sidebar.success("Global Status: VALID ✅")
