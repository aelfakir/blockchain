
import datetime
import hashlib
import json

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            # This simplified validation doesn't check the 'proof' of work,
            # which would be part of a real blockchain's validation.
            previous_block = block
            block_index += 1
        return True

!pip install streamlit pyngrok
import streamlit as st

st.set_page_config(page_title="Simple Python Blockchain", layout="wide")

st.title("⛓️ Simple Blockchain Demo")

# Initialize the blockchain in the session state
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

# Sidebar actions
st.sidebar.header("Controls")
if st.sidebar.button("Mine New Block"):
    prev_block = st.session_state.blockchain.get_previous_block()
    prev_hash = st.session_state.blockchain.hash(prev_block)
    # In a real blockchain, 'proof' comes from solving a puzzle
    new_block = st.session_state.blockchain.create_block(proof=100, previous_hash=prev_hash)
    st.sidebar.success("Block Mined!")

# Display the Chain
st.subheader("The Ledger")
for block in st.session_state.blockchain.chain:
    with st.expander(f"Block #{block['index']}"):
        st.json(block)
