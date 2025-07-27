import streamlit as st
import time
from rag_chatbot import SimpleRAGChatbot
from config import GEMINI_API_KEY

# Configure Streamlit page
st.set_page_config(
    page_title="Grievance Management Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI with dark theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        animation: slideIn 0.3s ease-in;
        color: white;
        font-weight: 500;
    }
    .user-message {
        background: linear-gradient(135deg, #4a6cf7 0%, #667eea 100%);
        border-left: 4px solid #2196f3;
        color: white !important;
    }
    .bot-message {
        background: linear-gradient(135deg, #9c27b0 0%, #673ab7 100%);
        border-left: 4px solid #e91e63;
        color: white !important;
    }
    .user-message strong {
        color: #e3f2fd !important;
    }
    .bot-message strong {
        color: #f8bbd9 !important;
    }
    .status-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: white;
    }
    .success-box {
        background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%);
        border-left: 4px solid #2e7d32;
        color: white !important;
    }
    .error-box {
        background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
        border-left: 4px solid #c62828;
        color: white !important;
    }
    .info-box {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        border-left: 4px solid #1565c0;
        color: white !important;
    }
    .status-box h3 {
        color: white !important;
        margin-top: 0;
    }
    .status-box p, .status-box ul, .status-box li {
        color: white !important;
    }
    @keyframes slideIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
        color: white !important;
    }
    
    /* Dark theme for text areas and inputs */
    .stTextArea textarea {
        background-color: #2b2b2b !important;
        color: white !important;
        border: 2px solid #667eea !important;
    }
    
    /* Make sure all text in status boxes is white */
    .status-box * {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_chatbot():
    """Initialize the chatbot with error handling"""
    if 'chatbot' not in st.session_state:
        try:
            with st.spinner("🔄 Initializing RAG chatbot... This may take a moment."):
                st.session_state.chatbot = SimpleRAGChatbot()
                st.session_state.initialized = True
        except Exception as e:
            st.error(f"❌ Failed to initialize chatbot: {str(e)}")
            st.session_state.initialized = False
            return False
    return True

def display_message(message, is_user=False):
    """Display a chat message with proper styling"""
    if is_user:
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You:</strong><br>{message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>🤖 Assistant:</strong><br>{message}
        </div>
        """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Grievance Management Chatbot</h1>
        <p>Powered by Google Gemini Flash & RAG Technology</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ Information")
        
        # API Key input
        if not GEMINI_API_KEY:
            st.warning("⚠️ Gemini API Key not found in environment variables")
            api_key = st.text_input("Enter your Gemini API Key:", type="password")
            if api_key:
                st.session_state.temp_api_key = api_key
        else:
            st.success("✅ API Key configured")
        
        st.markdown("---")
        
        # Instructions
        st.markdown("""
        ### 📋 How to use:
        
        **Register a Complaint:**
        - Say: "I have issues with my laptop"
        - Follow the prompts for name, mobile, details
        
        **Check Status:**
        - Say: "What's the status of my complaint?"
        - Provide your mobile number or complaint ID
        
        **Sample Messages:**
        - "Hello"
        - "Register a complaint for me"
        - "My laptop is not working"
        - "Check complaint status for 9876543210"
        """)
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.session_state.session_id = f"session_{int(time.time())}"
            st.rerun()
    
    # Check API configuration
    if not GEMINI_API_KEY and 'temp_api_key' not in st.session_state:
        st.markdown("""
        <div class="status-box error-box">
            <h3>⚠️ Configuration Required</h3>
            <p>Please provide your Gemini API Key in the sidebar to continue.</p>
            <p>You can get your API key from: <a href="https://makersuite.google.com/app/apikey" target="_blank" style="color: #ffcdd2 !important;">Google AI Studio</a></p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'session_id' not in st.session_state:
        st.session_state.session_id = f"session_{int(time.time())}"
    
    # Initialize chatbot
    if not initialize_chatbot():
        st.markdown("""
        <div class="status-box error-box">
            <h3>❌ Initialization Failed</h3>
            <p>Failed to initialize the chatbot. Please check your API key and try again.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Success message
    if st.session_state.get('initialized', False):
        st.markdown("""
        <div class="status-box success-box">
            <h3>✅ System Ready</h3>
            <p>The RAG chatbot is initialized and ready to help with your grievances!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat history
    if st.session_state.messages:
        st.subheader("💬 Chat History")
        for message in st.session_state.messages:
            display_message(message["content"], message["role"] == "user")
    else:
        # Welcome message
        st.markdown("""
        <div class="status-box info-box">
            <h3>👋 Welcome!</h3>
            <p>I'm your AI assistant for grievance management. I can help you:</p>
            <ul>
                <li>Register new complaints</li>
                <li>Check complaint status</li>
                <li>Provide general assistance</li>
            </ul>
            <p>Start by typing a message below!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat input
    st.subheader("💭 Your Message")
    user_input = st.text_area(
        "Type your message here...",
        height=100,
        placeholder="e.g., 'I have issues with my laptop. Register a complaint for me.'"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("📤 Send Message", use_container_width=True):
            if user_input.strip():
                # Add user message to history
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Get bot response
                with st.spinner("🤖 Thinking..."):
                    try:
                        bot_response = st.session_state.chatbot.chat(
                            user_input, 
                            st.session_state.session_id
                        )
                        
                        # Add bot response to history
                        st.session_state.messages.append({"role": "bot", "content": bot_response})
                        
                        # Rerun to update the display
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("Please enter a message before sending.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🔒 Your data is secure | 🤖 Powered by Google Gemini Flash | 🚀 Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 