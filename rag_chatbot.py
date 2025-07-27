import google.generativeai as genai
import requests
import json
import re
from typing import Dict, List, Optional
from config import GEMINI_API_KEY, API_BASE_URL, BOT_RESPONSES
import os

class SimpleRAGChatbot:
    def __init__(self):
        # Check API key
        api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
        if not api_key or api_key == "your_gemini_api_key_here":
            raise ValueError("Gemini API key not found or not set properly.")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Simple keyword-based knowledge base (no embeddings needed)
        self.knowledge_base = {
            "complaint_registration": "To register a complaint, I need your name, mobile number, and complaint details. I can help you with laptop issues, software problems, hardware malfunctions, and other technical grievances.",
            "status_inquiry": "To check complaint status, I can look up your complaint using your mobile number or complaint ID. Status can be: Registered, In Progress, Under Review, Resolved, or Closed.",
            "laptop_issues": "Common laptop issues include: slow performance, battery problems, screen issues, keyboard malfunctions, overheating, connectivity problems, and software crashes.",
            "greeting": "Hello! I'm here to help you with your grievances. I can register complaints and check status of existing complaints. How can I assist you today?"
        }
        
        # Conversation state
        self.conversation_state = {}
        self.pending_registrations = {}
    
    def _get_relevant_context(self, query: str) -> str:
        """Simple keyword-based context retrieval"""
        query_lower = query.lower()
        context_parts = []
        
        # Check for keywords and add relevant context
        if any(word in query_lower for word in ["register", "complaint", "issue", "problem", "laptop"]):
            context_parts.append(self.knowledge_base["complaint_registration"])
            
        if any(word in query_lower for word in ["status", "check", "complaint"]):
            context_parts.append(self.knowledge_base["status_inquiry"])
            
        if any(word in query_lower for word in ["hello", "hi", "hey", "greet"]):
            context_parts.append(self.knowledge_base["greeting"])
            
        return " ".join(context_parts)
    
    def _classify_intent(self, user_message: str) -> str:
        """Classify user intent using Gemini with simple context"""
        context = self._get_relevant_context(user_message)
        
        prompt = f"""
        Analyze the following user message and classify the intent. Return only one of these intents:
        - complaint_registration: User wants to register a new complaint
        - status_inquiry: User wants to check complaint status
        - greeting: User is greeting or asking general questions
        - unknown: Intent is unclear
        
        Context: {context}
        User message: "{user_message}"
        
        Intent:
        """
        
        try:
            response = self.model.generate_content(prompt)
            intent = response.text.strip().lower()
            
            if "complaint_registration" in intent:
                return "complaint_registration"
            elif "status_inquiry" in intent:
                return "status_inquiry"
            elif "greeting" in intent:
                return "greeting"
            else:
                return "unknown"
        except Exception as e:
            print(f"Error in intent classification: {e}")
            return "unknown"
    
    def _extract_information(self, user_message: str, info_type: str) -> Optional[str]:
        """Extract specific information from user message using Gemini"""
        prompts = {
            "name": f"Extract the person's name from this message. Return only the name or 'None' if not found: {user_message}",
            "mobile": f"Extract the mobile/phone number from this message. Return only the number or 'None' if not found: {user_message}",
            "complaint_details": f"Extract the complaint or issue details from this message. Return the details or 'None' if not found: {user_message}"
        }
        
        try:
            response = self.model.generate_content(prompts[info_type])
            extracted = response.text.strip()
            return extracted if extracted.lower() != "none" else None
        except Exception as e:
            print(f"Error extracting {info_type}: {e}")
            return None
    
    def _register_complaint_api(self, name: str, mobile: str, complaint_details: str) -> Dict:
        """Call API to register complaint"""
        try:
            response = requests.post(
                f"{API_BASE_URL}/register_complaint",
                json={
                    "name": name,
                    "mobile": mobile,
                    "complaint_details": complaint_details
                }
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Failed to register complaint"}
        except Exception as e:
            return {"error": f"API call failed: {str(e)}"}
    
    def _get_complaint_status_api(self, mobile: str = None, complaint_id: int = None) -> Dict:
        """Call API to get complaint status"""
        try:
            if complaint_id:
                response = requests.get(f"{API_BASE_URL}/complaint_status/{complaint_id}")
            elif mobile:
                response = requests.get(f"{API_BASE_URL}/complaint_status_by_mobile/{mobile}")
            else:
                return {"error": "Either mobile number or complaint ID is required"}
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Complaint not found"}
        except Exception as e:
            return {"error": f"API call failed: {str(e)}"}
    
    def chat(self, user_message: str, session_id: str = "default") -> str:
        """Main chat function"""
        # Initialize session state
        if session_id not in self.conversation_state:
            self.conversation_state[session_id] = {"step": "initial"}
        
        # Handle ongoing complaint registration
        if session_id in self.pending_registrations:
            return self._handle_complaint_registration(user_message, session_id)
        
        # Classify intent
        intent = self._classify_intent(user_message)
        
        if intent == "greeting":
            return BOT_RESPONSES["greeting"]
        
        elif intent == "complaint_registration":
            # Start complaint registration process
            self.pending_registrations[session_id] = {"step": "name"}
            return "I'll help you register a complaint. Let me collect some information.\n\nFirst, could you please provide your full name?"
        
        elif intent == "status_inquiry":
            # Extract mobile number or complaint ID
            mobile = self._extract_information(user_message, "mobile")
            complaint_id_match = re.search(r'\b\d+\b', user_message)
            complaint_id = int(complaint_id_match.group()) if complaint_id_match else None
            
            if mobile or complaint_id:
                result = self._get_complaint_status_api(mobile=mobile, complaint_id=complaint_id)
                if "error" in result:
                    return f"Sorry, I couldn't find your complaint. {result['error']}"
                else:
                    return f"""Here's your complaint status:
                    
**Complaint ID:** {result['complaint_id']}
**Name:** {result['name']}
**Mobile:** {result['mobile']}
**Status:** {result['status']}
**Complaint:** {result['complaint_details']}
**Registered on:** {result['created_at']}"""
            else:
                return "To check your complaint status, please provide your mobile number or complaint ID."
        
        else:
            return BOT_RESPONSES["unknown"]
    
    def _handle_complaint_registration(self, user_message: str, session_id: str) -> str:
        """Handle the complaint registration flow"""
        registration = self.pending_registrations[session_id]
        
        if registration["step"] == "name":
            name = self._extract_information(user_message, "name")
            if name:
                registration["name"] = name
                registration["step"] = "mobile"
                return f"Thank you, {name}! Now, please provide your mobile number."
            else:
                return "I couldn't extract your name. Please provide your full name clearly."
        
        elif registration["step"] == "mobile":
            mobile = self._extract_information(user_message, "mobile")
            if mobile and len(re.sub(r'\D', '', mobile)) >= 10:
                registration["mobile"] = re.sub(r'\D', '', mobile)[-10:]  # Last 10 digits
                registration["step"] = "complaint"
                return "Got it! Now, please describe your complaint or issue in detail."
            else:
                return "Please provide a valid mobile number."
        
        elif registration["step"] == "complaint":
            complaint_details = self._extract_information(user_message, "complaint_details") or user_message
            registration["complaint_details"] = complaint_details
            
            # Register the complaint
            result = self._register_complaint_api(
                name=registration["name"],
                mobile=registration["mobile"],
                complaint_details=complaint_details
            )
            
            # Clean up
            del self.pending_registrations[session_id]
            
            if "error" in result:
                return f"Sorry, there was an error registering your complaint: {result['error']}"
            else:
                return f"""✅ **Complaint Registered Successfully!**

**Complaint ID:** {result['id']}
**Name:** {registration['name']}
**Mobile:** {registration['mobile']}
**Issue:** {complaint_details}

Please save your Complaint ID: **{result['id']}** for future reference. You can use it to check the status of your complaint anytime."""
        
        return "Something went wrong. Please start over." 