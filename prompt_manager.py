"""
Prompt manager module for handling prompt enhancement through questionnaires.
"""

import json
import logging
import os
import re
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Base directory for prompt templates
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "templates")
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Default questionnaire templates
DEFAULT_TEMPLATES = {
    "code-generation": {
        "id": "code-generation",
        "name": "Code Generation",
        "description": "Generate prompts for code generation, debugging, or refactoring tasks",
        "icon": "code",
        "questions": [
            {
                "id": "programming-language",
                "type": "text",
                "label": "Programming Language",
                "placeholder": "e.g., Python, JavaScript, Java",
                "required": True,
            },
            {
                "id": "framework",
                "type": "text",
                "label": "Framework/Library",
                "placeholder": "e.g., React, Django, Spring",
                "required": False,
            },
            {
                "id": "task-description",
                "type": "textarea",
                "label": "Task Description",
                "placeholder": "Describe what you want the code to do",
                "required": True,
            },
            {
                "id": "requirements",
                "type": "textarea",
                "label": "Requirements",
                "placeholder": "List any specific requirements or constraints",
                "required": False,
            },
            {
                "id": "input-output",
                "type": "textarea",
                "label": "Expected Input/Output",
                "placeholder": "Describe the expected inputs and outputs",
                "required": False,
            },
            {
                "id": "code-style",
                "type": "textarea",
                "label": "Code Style Preferences",
                "placeholder": "Any specific coding style or patterns you prefer",
                "required": False,
            },
            {
                "id": "include-tests",
                "type": "checkbox",
                "label": "Include unit tests",
                "defaultValue": True,
            },
            {
                "id": "include-examples",
                "type": "checkbox",
                "label": "Include usage examples",
                "defaultValue": True,
            },
            {
                "id": "additional-context",
                "type": "textarea",
                "label": "Additional Context",
                "placeholder": "Any other information that might be helpful",
                "required": False,
            },
        ],
        "prompt_template": """
I need help with {programming-language} code{framework ? " using " + framework : ""}.

Task: {task-description}

{requirements ? "Requirements:\n" + requirements : ""}

{input-output ? "Expected Input/Output:\n" + input-output : ""}

{code-style ? "Code Style Preferences:\n" + code-style : ""}

{include-tests ? "Please include unit tests." : ""}
{include-examples ? "Please include usage examples." : ""}

{additional-context ? "Additional Context:\n" + additional-context : ""}
        """.strip()
    },
    "content-creation": {
        "id": "content-creation",
        "name": "Content Creation",
        "description": "Generate prompts for blog posts, articles, social media content, etc.",
        "icon": "file-text",
        "questions": [
            {
                "id": "content-type",
                "type": "select",
                "label": "Content Type",
                "options": [
                    { "value": "blog-post", "label": "Blog Post" },
                    { "value": "article", "label": "Article" },
                    { "value": "social-media", "label": "Social Media Post" },
                    { "value": "email", "label": "Email" },
                    { "value": "product-description", "label": "Product Description" },
                    { "value": "other", "label": "Other" },
                ],
                "required": True,
            },
            {
                "id": "target-audience",
                "type": "text",
                "label": "Target Audience",
                "placeholder": "Who is this content for?",
                "required": True,
            },
            {
                "id": "tone",
                "type": "select",
                "label": "Tone",
                "options": [
                    { "value": "formal", "label": "Formal" },
                    { "value": "conversational", "label": "Conversational" },
                    { "value": "humorous", "label": "Humorous" },
                    { "value": "technical", "label": "Technical" },
                    { "value": "persuasive", "label": "Persuasive" },
                    { "value": "inspirational", "label": "Inspirational" },
                ],
                "required": True,
            },
            {
                "id": "main-topic",
                "type": "textarea",
                "label": "Main Topic",
                "placeholder": "What is the main topic or subject?",
                "required": True,
            },
            {
                "id": "key-points",
                "type": "textarea",
                "label": "Key Points",
                "placeholder": "List the key points you want to include",
                "required": False,
            },
            {
                "id": "content-length",
                "type": "select",
                "label": "Content Length",
                "options": [
                    { "value": "short", "label": "Short (< 300 words)" },
                    { "value": "medium", "label": "Medium (300-800 words)" },
                    { "value": "long", "label": "Long (800-1500 words)" },
                    { "value": "very-long", "label": "Very Long (1500+ words)" },
                ],
                "required": True,
            },
            {
                "id": "seo-keywords",
                "type": "textarea",
                "label": "SEO Keywords",
                "placeholder": "List any SEO keywords to include",
                "required": False,
            },
            {
                "id": "additional-instructions",
                "type": "textarea",
                "label": "Additional Instructions",
                "placeholder": "Any other specific instructions",
                "required": False,
            },
        ],
        "prompt_template": """
Please write a {content-type} for {target-audience} with a {tone} tone.

Topic: {main-topic}

{key-points ? "Key Points to Include:\n" + key-points : ""}

Length: {content-length}

{seo-keywords ? "SEO Keywords to Include:\n" + seo-keywords : ""}

{additional-instructions ? "Additional Instructions:\n" + additional-instructions : ""}
        """.strip()
    },
    "general": {
        "id": "general",
        "name": "General Purpose",
        "description": "A general-purpose questionnaire for any type of request",
        "icon": "help-circle",
        "questions": [
            {
                "id": "main-goal",
                "type": "textarea",
                "label": "Main Goal",
                "placeholder": "What are you trying to accomplish?",
                "required": True,
            },
            {
                "id": "context",
                "type": "textarea",
                "label": "Context",
                "placeholder": "Provide any relevant background information",
                "required": False,
            },
            {
                "id": "specific-requirements",
                "type": "textarea",
                "label": "Specific Requirements",
                "placeholder": "List any specific requirements or constraints",
                "required": False,
            },
            {
                "id": "preferred-format",
                "type": "text",
                "label": "Preferred Format",
                "placeholder": "How would you like the response formatted?",
                "required": False,
            },
            {
                "id": "level-of-detail",
                "type": "select",
                "label": "Level of Detail",
                "options": [
                    { "value": "brief", "label": "Brief" },
                    { "value": "moderate", "label": "Moderate" },
                    { "value": "detailed", "label": "Detailed" },
                    { "value": "comprehensive", "label": "Comprehensive" },
                ],
                "required": True,
            },
            {
                "id": "additional-notes",
                "type": "textarea",
                "label": "Additional Notes",
                "placeholder": "Any other information that might be helpful",
                "required": False,
            },
        ],
        "prompt_template": """
I need help with the following:

Main Goal: {main-goal}

{context ? "Context:\n" + context : ""}

{specific-requirements ? "Specific Requirements:\n" + specific-requirements : ""}

{preferred-format ? "Preferred Format: " + preferred-format : ""}

Level of Detail: {level-of-detail}

{additional-notes ? "Additional Notes:\n" + additional-notes : ""}
        """.strip()
    }
}

class PromptManager:
    """
    Manages prompt enhancement through questionnaires.
    """
    
    def __init__(self, templates_dir: str = None):
        """
        Initialize the prompt manager.
        
        Args:
            templates_dir: Directory for storing prompt templates
        """
        self.templates_dir = templates_dir or TEMPLATES_DIR
        self._templates = {}
        self._load_default_templates()
        self._load_custom_templates()
    
    def _load_default_templates(self):
        """Load the default templates."""
        for template_id, template_data in DEFAULT_TEMPLATES.items():
            self._templates[template_id] = template_data
            
            # Save default templates to disk if they don't exist
            file_path = os.path.join(self.templates_dir, f"{template_id}.json")
            if not os.path.exists(file_path):
                os.makedirs(self.templates_dir, exist_ok=True)
                with open(file_path, 'w') as f:
                    json.dump(template_data, f, indent=2)
    
    def _load_custom_templates(self):
        """Load custom templates from the templates directory."""
        if not os.path.exists(self.templates_dir):
            return
        
        for filename in os.listdir(self.templates_dir):
            if filename.endswith('.json'):
                template_id = os.path.splitext(filename)[0]
                if template_id not in self._templates:  # Don't overwrite default templates
                    file_path = os.path.join(self.templates_dir, filename)
                    try:
                        with open(file_path, 'r') as f:
                            template_data = json.load(f)
                            self._templates[template_id] = template_data
                    except Exception as e:
                        logger.error(f"Error loading template from {file_path}: {e}")
    
    def select_template(self, message: str) -> str:
        """
        Select the most appropriate template based on the user's message.
        
        Args:
            message: The user's message
            
        Returns:
            The ID of the selected template
        """
        message = message.lower()
        
        # Define keywords for each template
        template_keywords = {
            "code-generation": ["code", "program", "function", "bug", "error", "debug", "algorithm", "python", "javascript", "java", "c++", "programming"],
            "content-creation": ["write", "article", "blog", "post", "content", "essay", "email", "social media", "marketing", "copywriting"],
        }
        
        # Count keyword matches for each template
        template_scores = {template_id: 0 for template_id in self._templates.keys()}
        
        for template_id, keywords in template_keywords.items():
            for keyword in keywords:
                if keyword in message:
                    template_scores[template_id] += 1
        
        # Find the template with the highest score
        best_template_id = max(template_scores.items(), key=lambda x: x[1])[0]
        
        # If no keywords matched significantly, use the general template
        if template_scores[best_template_id] == 0:
            return "general"
        
        return best_template_id
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a template by ID.
        
        Args:
            template_id: ID of the template
            
        Returns:
            Template data or None if not found
        """
        return self._templates.get(template_id)
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """
        List all available templates.
        
        Returns:
            List of templates with their IDs
        """
        return [{"id": template_id, **template_data} for template_id, template_data in self._templates.items()]
    
    def get_current_question(self, conversation: Any) -> str:
        """
        Get the current question for a conversation.
        
        Args:
            conversation: The conversation object
            
        Returns:
            The current question text
        """
        if not conversation.questionnaire:
            return "What can I help you with today?"
        
        template_id = conversation.questionnaire.get("templateId")
        template = self.get_template(template_id)
        
        if not template:
            return "I'm sorry, but I couldn't find the questionnaire template. How can I help you?"
        
        current_index = conversation.questionnaire.get("currentQuestionIndex", 0)
        
        if current_index >= len(template["questions"]):
            return "Thank you for providing all the information. I'll generate a response for you now."
        
        question = template["questions"][current_index]
        
        # Format the question based on its type
        if question["type"] == "select":
            options_text = "\n".join([f"- {option['label']}" for option in question["options"]])
            return f"{question['label']}:\n{options_text}\n\nPlease select one of the options above."
        else:
            return f"{question['label']}: {question.get('placeholder', '')}"
    
    def get_next_question(self, conversation: Any) -> str:
        """
        Move to the next question and return it.
        
        Args:
            conversation: The conversation object
            
        Returns:
            The next question text
        """
        if not conversation.questionnaire:
            return "What can I help you with today?"
        
        # Increment the current question index
        current_index = conversation.questionnaire.get("currentQuestionIndex", 0)
        conversation.questionnaire["currentQuestionIndex"] = current_index + 1
        
        return self.get_current_question(conversation)
    
    def has_next_question(self, conversation: Any) -> bool:
        """
        Check if there are more questions in the questionnaire.
        
        Args:
            conversation: The conversation object
            
        Returns:
            True if there are more questions, False otherwise
        """
        if not conversation.questionnaire:
            return False
        
        template_id = conversation.questionnaire.get("templateId")
        template = self.get_template(template_id)
        
        if not template:
            return False
        
        current_index = conversation.questionnaire.get("currentQuestionIndex", 0)
        
        return current_index < len(template["questions"]) - 1
    
    def store_answer(self, conversation: Any, answer: str) -> None:
        """
        Store the user's answer to the current question.
        
        Args:
            conversation: The conversation object
            answer: The user's answer
        """
        if not conversation.questionnaire:
            return
        
        template_id = conversation.questionnaire.get("templateId")
        template = self.get_template(template_id)
        
        if not template:
            return
        
        current_index = conversation.questionnaire.get("currentQuestionIndex", 0)
        
        if current_index >= len(template["questions"]):
            return
        
        question = template["questions"][current_index]
        question_id = question["id"]
        
        # Process the answer based on the question type
        if question["type"] == "checkbox":
            # Convert string "yes"/"no"/"true"/"false" to boolean
            processed_answer = answer.lower() in ["yes", "true", "1", "y"]
        elif question["type"] == "select":
            # Try to match the answer to one of the options
            options = question.get("options", [])
            matched_option = None
            
            for option in options:
                if option["label"].lower() in answer.lower() or option["value"].lower() in answer.lower():
                    matched_option = option["value"]
                    break
            
            processed_answer = matched_option or answer
        else:
            processed_answer = answer
        
        # Store the answer
        if "answers" not in conversation.questionnaire:
            conversation.questionnaire["answers"] = {}
        
        conversation.questionnaire["answers"][question_id] = processed_answer
    
    def generate_prompt(self, conversation: Any) -> str:
        """
        Generate an enhanced prompt based on the questionnaire answers.
        
        Args:
            conversation: The conversation object
            
        Returns:
            The enhanced prompt
        """
        if not conversation.questionnaire or "answers" not in conversation.questionnaire:
            return conversation.original_message
        
        template_id = conversation.questionnaire.get("templateId")
        template = self.get_template(template_id)
        
        if not template or "prompt_template" not in template:
            # Fallback to a simple concatenation of answers
            answers = conversation.questionnaire.get("answers", {})
            prompt_parts = [conversation.original_message]
            
            for question_id, answer in answers.items():
                prompt_parts.append(f"{question_id}: {answer}")
            
            return "\n\n".join(prompt_parts)
        
        # Use the template's prompt template
        prompt_template = template["prompt_template"]
        answers = conversation.questionnaire.get("answers", {})
        
        # Replace placeholders in the template
        for question_id, answer in answers.items():
            # Handle conditional sections with ternary operators
            # Format: {variable ? "text if true" : "text if false"}
            pattern = r'\{' + re.escape(question_id) + r'\s*\?\s*"([^"]*)"\s*:\s*"([^"]*)"\}'
            
            for match in re.finditer(pattern, prompt_template):
                true_text, false_text = match.groups()
                replacement = true_text if answer else false_text
                prompt_template = prompt_template.replace(match.group(0), replacement)
            
            # Replace simple variables
            placeholder = '{' + question_id + '}'
            if placeholder in prompt_template:
                prompt_template = prompt_template.replace(placeholder, str(answer))
        
        # Clean up any remaining conditional placeholders
        prompt_template = re.sub(r'\{[^{}]*\?\s*"[^"]*"\s*:\s*"[^"]*"\}', '', prompt_template)
        
        # Clean up any remaining simple placeholders
        prompt_template = re.sub(r'\{[^{}]*\}', '', prompt_template)
        
        # Combine with original message
        return f"{conversation.original_message}\n\n{prompt_template}"

# Initialize the prompt manager
prompt_manager = PromptManager()
