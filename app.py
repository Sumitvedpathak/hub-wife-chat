import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import time
import html

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
claude_api_key = os.getenv("ANTHROPIC_API_KEY")

# Page configuration
st.set_page_config(page_title="Husband & Wife Conversation", layout="wide")

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'current_iteration' not in st.session_state:
    st.session_state.current_iteration = 0
if 'conversation_started' not in st.session_state:
    st.session_state.conversation_started = False
if 'message_index' not in st.session_state:
    st.session_state.message_index = 0
if 'streamed_messages' not in st.session_state:
    st.session_state.streamed_messages = {}  # Track which messages are fully streamed

# Sidebar Configuration
st.sidebar.title("Configuration")

# Topic of Fight
topic = st.sidebar.text_input(
    "Topic of Fight",
    value="",
    help="Enter the topic of conversation/argument"
)

# Number of Iterations
iterations = st.sidebar.number_input(
    "# of Iterations",
    min_value=1,
    max_value=20,
    value=3,
    help="Number of back-and-forth exchanges"
)

# Model Selection
st.sidebar.subheader("Husband Model")
husband_model = st.sidebar.selectbox(
    "Select Model",
    ["gpt-4o", "claude-3-5-haiku-latest"],
    index=0,
    key="husband_model"
)

st.sidebar.subheader("Wife Model")
wife_model = st.sidebar.selectbox(
    "Select Model",
    ["claude-3-5-haiku-latest", "gpt-4o"],
    index=0,
    key="wife_model"
)

# Start Conversation Button
start_button = st.sidebar.button("▶️ Start Conversation", type="primary", use_container_width=True)
clear_button = st.sidebar.button("🗑️ Clear Conversation", use_container_width=True)

# Main Content
st.title("Witty Conversation between Husband and Wife")

# Create single chat window - use empty placeholder for dynamic updates
chat_placeholder = st.empty()

# Helper function to display a message with streaming effect
def display_message_streaming(msg, msg_index, streamed_length=None):
    """Display a message with streaming effect (character by character)"""
    # Get the content to display
    full_content = msg["content"]
    
    # Determine how much to show
    if streamed_length is None:
        # Get current streamed length for this message
        current_length = st.session_state.streamed_messages.get(msg_index, 0)
        
        if current_length < len(full_content):
            # Increment by a few characters for streaming effect
            current_length = min(current_length + 3, len(full_content))
            st.session_state.streamed_messages[msg_index] = current_length
            displayed_content = full_content[:current_length]
        else:
            # Message is fully streamed
            displayed_content = full_content
    else:
        displayed_content = full_content[:streamed_length] if streamed_length < len(full_content) else full_content
    
    # Escape HTML to prevent XSS
    escaped_content = html.escape(displayed_content)
    
    if msg["role"] == "husband":
        st.markdown(f"""
        <div style='display: flex; justify-content: flex-start; margin: 10px 0;'>
            <div style='max-width: 70%;'>
                <div style='font-weight: bold; color: #1976d2; margin-bottom: 5px; font-size: 14px;'>Husband</div>
                <div style='background-color: #e3f2fd; color: #212121; padding: 15px; border-radius: 15px; border-top-left-radius: 5px;'>
                    {escaped_content}{'<span style="opacity: 0.5;">▊</span>' if len(displayed_content) < len(full_content) else ''}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='display: flex; justify-content: flex-end; margin: 10px 0;'>
            <div style='max-width: 70%;'>
                <div style='font-weight: bold; color: #c2185b; margin-bottom: 5px; font-size: 14px; text-align: right;'>Wife</div>
                <div style='background-color: #fce4ec; color: #212121; padding: 15px; border-radius: 15px; border-top-right-radius: 5px;'>
                    {escaped_content}{'<span style="opacity: 0.5;">▊</span>' if len(displayed_content) < len(full_content) else ''}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Return whether message is fully streamed
    return len(displayed_content) >= len(full_content)

# Clear conversation
if clear_button:
    st.session_state.conversation_history = []
    st.session_state.is_running = False
    st.session_state.current_iteration = 0
    st.session_state.conversation_started = False
    st.session_state.streamed_messages = {}
    st.rerun()

# Function to call LLM API via OpenAI library
def get_llm_response(role, topic, conversation_context, model):
    """Get response from LLM via OpenAI library (supports both OpenAI and Anthropic models)"""
    
    # Create system prompt based on role
    if role == "husband":
        system_prompt = f"""You are a calm husband.  You are having an argument with your wife about: {topic}
You are an husband who has a nature of being calm. You have trait of Echoism. But you have a very 
good response for any comment, question or response to the wife. And you always give a witty or comedy response. 
Give one liner response."""
    else:
        system_prompt = f"""You are a wife.  You are having an argument with your husband about: {topic}
You are an wife. You have trait of Narcissist. You always try to pick a fight, 
blame, criticise of every small thing that husband does. For any witty or comedy response, you get more annoyed. 
Give one liner response."""
    
    # Build conversation messages
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history
    for msg in conversation_context:
        messages.append({
            "role": "assistant" if msg["role"] == role else "user",
            "content": msg["content"]
        })
    
    # Add prompt to continue
    if conversation_context:
        messages.append({
            "role": "user",
            "content": "Continue the witty banter. Respond to what was just said!"
        })
    
    try:
        # Determine which client to use based on model
        if model.startswith("gpt"):
            # OpenAI model
            client = OpenAI(api_key=openai_api_key)
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=300,
                temperature=0.8
            )
            return response.choices[0].message.content
        else:
            # Anthropic model via OpenAI library (compatible interface)
            # Use the correct base URL with trailing slash
            client = OpenAI(
                api_key=claude_api_key,
                base_url="https://api.anthropic.com/v1/"
            )
            # Use the model name from selectbox (should be claude-3-5-haiku-latest)
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=300,
                temperature=0.8,
                extra_headers={"anthropic-version": "2023-06-01"}
            )
            return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Display existing conversation FIRST (so it shows before generation)
def render_chat():
    """Render all messages in the chat with streaming effect"""
    if st.session_state.conversation_history:
        # Create a container inside the placeholder for scrolling
        with chat_placeholder.container():
            for idx, msg in enumerate(st.session_state.conversation_history):
                # Check if message needs streaming
                is_fully_streamed = display_message_streaming(msg, idx)
                # If not fully streamed, we'll need to continue streaming
                if not is_fully_streamed:
                    # This will trigger a rerun to continue streaming
                    st.session_state.continue_streaming = True
    else:
        with chat_placeholder.container():
            st.info("Click 'Start Conversation' to begin...")

# Initialize streaming state
if 'continue_streaming' not in st.session_state:
    st.session_state.continue_streaming = False

# Render chat immediately
render_chat()

# Continue streaming if there are messages that need to be streamed
if st.session_state.continue_streaming:
    # Check if any message is still streaming
    all_streamed = True
    for idx, msg in enumerate(st.session_state.conversation_history):
        current_length = st.session_state.streamed_messages.get(idx, 0)
        if current_length < len(msg["content"]):
            all_streamed = False
            break
    
    if not all_streamed:
        # Continue streaming with a small delay
        time.sleep(0.03)  # Small delay for typing effect
        st.rerun()
    else:
        st.session_state.continue_streaming = False

# Run conversation - Start button clicked
if start_button:
    # Initialize with greeting messages
    st.session_state.conversation_history = [
        {"role": "husband", "content": "Hi Honey"},
        {"role": "wife", "content": "Hi"}
    ]
    st.session_state.is_running = True
    st.session_state.current_iteration = 0
    st.session_state.conversation_started = True
    st.session_state.message_index = 2  # Track how many messages we've displayed
    st.session_state.streamed_messages = {}  # Reset streaming state
    st.session_state.continue_streaming = True  # Start streaming
    st.rerun()

# Continue conversation generation (state-driven approach)
if st.session_state.conversation_started and st.session_state.is_running:
    # Progress bar
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    
    # Get current iteration
    i = st.session_state.current_iteration
    
    if i < iterations:
        # Determine whose turn it is based on message count
        # Initial: 2 messages (husband, wife)
        # Each iteration adds 2 more (husband, wife)
        current_count = len(st.session_state.conversation_history)
        expected_after_init = 2 + (i * 2)
        
        if current_count == expected_after_init:
            # It's husband's turn
            status_text.text(f"Iteration {i+1}/{iterations}: Husband thinking...")
            progress_bar.progress((i * 2) / (iterations * 2))
            
            husband_response = get_llm_response(
                "husband", 
                topic, 
                st.session_state.conversation_history,
                husband_model
            )
            new_msg_index = len(st.session_state.conversation_history)
            st.session_state.conversation_history.append({
                "role": "husband",
                "content": husband_response
            })
            # Initialize streaming for new message
            st.session_state.streamed_messages[new_msg_index] = 0
            st.session_state.continue_streaming = True
            progress_bar.progress((i * 2 + 1) / (iterations * 2))
            # Update display immediately
            render_chat()
            # Small delay to ensure UI updates
            time.sleep(0.1)
            st.rerun()
        
        elif current_count == expected_after_init + 1:
            # It's wife's turn
            status_text.text(f"Iteration {i+1}/{iterations}: Wife thinking...")
            progress_bar.progress((i * 2 + 1) / (iterations * 2))
            
            wife_response = get_llm_response(
                "wife", 
                topic, 
                st.session_state.conversation_history,
                wife_model
            )
            new_msg_index = len(st.session_state.conversation_history)
            st.session_state.conversation_history.append({
                "role": "wife",
                "content": wife_response
            })
            # Initialize streaming for new message
            st.session_state.streamed_messages[new_msg_index] = 0
            st.session_state.continue_streaming = True
            st.session_state.current_iteration += 1
            progress_bar.progress((i * 2 + 2) / (iterations * 2))
            # Update display immediately
            render_chat()
            # Small delay to ensure UI updates
            time.sleep(0.1)
            st.rerun()
    
    else:
        # Conversation complete
        status_text.text("Conversation complete! 🎉")
        st.session_state.is_running = False
        st.session_state.conversation_started = False
        st.session_state.current_iteration = 0

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("💡 Tip: Try different topics and models for varied conversations!")