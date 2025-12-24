import datetime
import hashlib
import json
import streamlit as st

class Blockchain:
    def __init__(self):
        self.chain = []
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

    def is_chain_valid(self, chain):
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i-1]
            # Check if the link is broken
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
        return True

# --- Streamlit UI ---
st.set_page_config(page_title="Blockchain Tamper Lab", layout="wide")
st.title("🧪 Blockchain Tamper & Validation Lab")

if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

# Sidebar: Actions
st.sidebar.header("Actions")
if st.sidebar.button("Mine New Block"):
    bc = st.session_state.blockchain
    new_block = bc.create_block(proof=100, previous_hash=bc.hash(bc.get_previous_block()))
    st.sidebar.success(f"Block #{new_block['index']} Added!")

# Sidebar: Validation Status
is_valid = st.session_state.blockchain.is_chain_valid(st.session_state.blockchain.chain)
if is_valid:
    st.sidebar.success("Chain Status: VALID ✅")
else:
    st.sidebar.error("Chain Status: TAMPERED ❌")

# --- Main Display ---
st.subheader("The Blockchain")



for i, block in enumerate(st.session_state.blockchain.chain):
    current_hash = st.session_state.blockchain.hash(block)
    
    with st.expander(f"Block #{block['index']} - Hash: {current_hash[:15]}...", expanded=True):
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # We use text_input to allow users to "tamper" with the data
            new_data = st.text_input(f"Data for Block {block['index']}", value=block['data'], key=f"data_{i}")
            # Update the block data in real-time
            st.session_state.blockchain.chain[i]['data'] = new_data
            
            st.write(f"**Previous Hash:** `{block['previous_hash']}`")
            st.write(f"**Current Hash:** `{current_hash}`")
        
        with col2:
            if i > 0:
                prev_hash_actual = st.session_state.blockchain.hash(st.session_state.blockchain.chain[i-1])
                if block['previous_hash'] == prev_hash_actual:
                    st.info("Link is Secure 🔗")
                else:
                    st.error("Link is Broken! 💥")

st.divider()
