from ai_parser import parse_with_ollama_two
from sql_handler import write_trade, read_trades
import streamlit as st

st.title("Trade Journal Assistant")

# Initialize the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

Prompt = st.chat_input("Enter your trade log/query here")
if Prompt:
    st.chat_message("🦊").markdown(Prompt)
    st.session_state.messages.append({"role": "🦊", "content": Prompt})
    with st.chat_message("🤖"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Processing...")

        # Parse the input using the Ollama model
        result = parse_with_ollama_two(Prompt)
        message_placeholder.markdown(result)

        # Log the trade if the intent is "trade_logging"
        if result["intent"] == "trade_logging":
            write_trade(result["entities"])
            st.success("Trade logged successfully!")
            st.session_state.messages.append(
                {"role": "🤖", "content": "Trade logged successfully!"}
            )
        elif result["intent"] == "query":
            trades_df = read_trades()
            st.dataframe(trades_df)
        elif result["intent"] == "unsure":
            st.warning(f'Dumbass!{result["entities"]["message"]}')
            st.session_state.messages.append(
                {"role": "🤖", "content": f'Dumbass!{result["entities"]["message"]}'}
            )
        else:
            st.warning("Unable to determine intent. Please clarify your request.")
            st.session_state.messages.append(
                "Unable to determine intent. Please clarify your request."
            )


# result = parse_with_ollama_two("I bought 100 shares of BTC at 50000")
