# ... (Keep the Blockchain class from before) ...

# --- Main Display ---
st.subheader("The Blockchain Ledger")

chain = st.session_state.blockchain.chain
chain_is_corrupted = False  # Track if any previous block was tampered with

for i, block in enumerate(chain):
    current_hash = st.session_state.blockchain.hash(block)
    
    # Check if THIS specific block is valid compared to the previous one
    link_broken = False
    if i > 0:
        prev_block_actual_hash = st.session_state.blockchain.hash(chain[i-1])
        if block['previous_hash'] != prev_block_actual_hash:
            link_broken = True
            chain_is_corrupted = True # Mark the rest of the chain as corrupted

    with st.expander(f"Block #{block['index']}", expanded=True):
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Edit Data
            user_data = st.text_input(f"Edit Data", value=block['data'], key=f"input_{i}")
            st.session_state.blockchain.chain[i]['data'] = user_data
            
            st.write(f"**Current Hash:** `{current_hash}`")
            st.write(f"**Previous Hash:** `{block['previous_hash']}`")
        
        with col2:
            # UI logic to show the "Ripple Effect"
            if i == 0:
                st.info("Genesis Block (Root)")
            elif chain_is_corrupted:
                st.error("❌ CHAIN BROKEN")
                st.caption("This block is invalid because a previous block was tampered with.")
            else:
                st.success("🔗 Link Secure")
