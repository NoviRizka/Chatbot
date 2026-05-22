import streamlit as st
from FSM import FSM

# Config halaman
st.set_page_config(
    page_title="Chatbot Pemesanan",
    page_icon="🤖",
    layout="wide"
)

# CSS sederhana
st.markdown("""
<style>
.main {
    padding: 20px;
}

.chat-box {
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 10px;
    background-color: #f9f9f9;
}
</style>
""", unsafe_allow_html=True)

# Inisialisasi chatbot
if "chatbot" not in st.session_state:
    st.session_state.chatbot = FSM()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.title("🤖 Chatbot Pemesanan Makanan")
st.markdown("Silakan lakukan pemesanan melalui chatbot")

# Tab menu
tab1, tab2 = st.tabs(["💬 Pemesanan", "📋 Daftar Menu"])

# =========================
# TAB PEMESANAN
# =========================
with tab1:

    col1, col2 = st.columns([1, 2])

    # Keranjang belanja
    with col1:
        st.subheader("🛒 Keranjang")

        cart = st.session_state.chatbot.cart

        if len(cart) == 0:
            st.info("Keranjang masih kosong")

        else:
            total = 0

            for item in cart:
                st.write(
                    f"{item['item']} "
                    f"x{item['qty']} "
                    f"= Rp{item['total']}"
                )

                total += item["total"]

            st.success(f"Total : Rp{total}")

    # Chatbot
    with col2:
        st.subheader("💬 Chatbot")

        # Menampilkan chat
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Input user
        user_input = st.chat_input("Tulis pesan...")

        if user_input:

            # Simpan pesan user
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })

            # Response chatbot
            response = st.session_state.chatbot.step(user_input)

            # Simpan response bot
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            st.rerun()

# =========================
# TAB MENU
# =========================
with tab2:

    st.subheader("📋 Daftar Menu")

    menu = st.session_state.chatbot.engine.menu

    for item, harga in menu.items():
        st.write(f"🍽️ {item.title()} - Rp{harga}")
