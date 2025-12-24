import datetime
import hashlib
import json
import streamlit as st

# --- 1. Blockchain Logic ---
class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 2 
        # Create the Genesis Block immediately
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

# --- 2. Streamlit UI Setup ---
st.set_page_config(page_title="Blockchain Ripple Lab", layout="wide")
st.title("⛓️ Blockchain 'Ripple Effect' Lab")

# INITIALIZATION: show blocks 
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

# --- 3. Sidebar Controls ---
st.sidebar.header("Controls")

if st.sidebar.button("⛏️ Mine New Block"):
    bc = st.session_state.blockchain
    prev_block = bc.get_previous_block()
    
    with st.sidebar.status("Computing Hash..."):
        new_proof = bc.proof_of_work(prev_block['proof'])
        # Use the hash of the current last block as the previous_hash for the new one
        actual_prev_hash = bc.hash(prev_block)
        new_block = bc.create_block(proof=new_proof, previous_hash=actual_prev_hash)
    st.sidebar.success(f"Block #{new_block['index']} Added!")

if st.sidebar.button("♻️ Reset Blockchain"):
    st.session_state.blockchain = Blockchain()
    st.rerun()

# --- 4. Main Ledger Display ---
st.subheader("The Distributed Ledger")



# We pull the list from session state to display it
chain_to_display = st.session_state.blockchain.chain
corrupted_chain_flag = False 

for i, block in enumerate(chain_to_display):
    # Calculate hash of this block in its current state (with whatever text is in the box)
    current_hash_calc = st.session_state.blockchain.hash(block)
    
    # Check if the chain is broken at this point
    if i > 0:
        actual_prev_hash = st.session_state.blockchain.hash(chain_to_display[i-1])
        if block['previous_hash'] != actual_prev_hash:
            corrupted_chain_flag = True

    # Visual Card for the Block
    with st.expander(f"📦 Block #{block['index']}", expanded=True):
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # The input field that allows tampering
            user_input = st.text_input(f"Data", value=block['data'], key=f"input_{i}")
            # Update the session state immediately
            st.session_state.blockchain.chain[i]['data'] = user_input
            
            st.write(f"**Current Hash:** `{current_hash_calc}`")
            st.write(f"**Previous Hash:** `{block['previous_hash']}`")
        
        with col2:
            if i == 0:
                st.info("Genesis Block")
            elif corrupted_chain_flag:
                st.error("❌ INVALIDATED")
            else:
                st.success("🔗 SECURE")

# Global Status in Sidebar
if corrupted_chain_flag:
    st.sidebar.error("Global Status: TAMPERED ❌")
else:
    st.sidebar.success("Global Status: VALID ✅")
