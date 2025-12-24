import datetime
import hashlib
import json
import streamlit as st

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 2 # Change this to 3 or 4 to make mining harder
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
            # This is the "puzzle": find a hash that starts with '00'
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

# --- Streamlit UI ---
st.set_page_config(page_title="Blockchain Lab", layout="wide")
st.title("⛓️ Interactive Blockchain Lab")

# CRITICAL: This ensures the blockchain is saved between clicks
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

# Sidebar: Mining
st.sidebar.header("Mining")
if st.sidebar.button("Mine New Block"):
    bc = st.session_state.blockchain
    prev_block = bc.get_previous_block()
    
    # Proof of Work
    with st.sidebar.status("Mining..."):
        new_proof = bc.proof_of_work(prev_block['proof'])
        new_block = bc.create_block(proof=new_proof, previous_hash=bc.hash(prev_block))
    
    st.sidebar.success(f"Block #{new_block['index']} Mined!")

# Sidebar: Status
is_valid = st.session_state.blockchain.is_chain_valid(st.session_state.blockchain.chain)
if is_valid:
    st.sidebar.success("Chain Status: VALID ✅")
else:
    st.sidebar.error("Chain Status: TAMPERED ❌")

# --- Main Display ---
st.subheader("The Blockchain Ledger")



# We display blocks in reverse (newest at the top) or standard order
for i, block in enumerate(st.session_state.blockchain.chain):
    current_hash = st.session_state.blockchain.hash(block)
    
    with st.expander(f"Block #{block['index']}", expanded=True):
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Real-time data editing
            user_data = st.text_input(f"Edit Data", value=block['data'], key=f"input_{i}")
            # Update the stored data immediately
            st.session_state.blockchain.chain[i]['data'] = user_data
            
            st.write(f"**Current Hash:** `{current_hash}`")
            st.write(f"**Previous Hash:** `{block['previous_hash']}`")
        
        with col2:
            st.write(f"**Proof:** `{block['proof']}`")
            st.write(f"**Timestamp:** {block['timestamp']}")
            
            if i > 0:
                prev_actual = st.session_state.blockchain.hash(st.session_state.blockchain.chain[i-1])
                if block['previous_hash'] == prev_actual:
                    st.success("Link Secure")
                else:
                    st.error("Link Broken")
