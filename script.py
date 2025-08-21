import os

def create_file(path, content):
    """Creates a file with the given content."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

def setup_template_bot_project():
    """Sets up the project directory and files for the Template Bot."""

    project_root = "template_bot_project"

    # Ensure the root directory exists
    os.makedirs(project_root, exist_ok=True)
    print(f"Created project root: {project_root}")

    # --- File Contents ---

    # index.html content
    index_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Template Bot: Roles & Assets Hub</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
        .btn {
            @apply px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors duration-300 shadow-md text-sm;
        }
        .btn-green {
            @apply bg-green-600 hover:bg-green-700;
        }
        .btn-purple {
            @apply bg-purple-600 hover:bg-purple-700;
        }
        .btn-red {
            @apply bg-red-600 hover:bg-red-700;
        }
        .btn-yellow {
            @apply bg-yellow-600 hover:bg-yellow-700;
        }
        .btn-teal {
            @apply bg-teal-600 hover:bg-teal-700;
        }
        .modal {
            display: none; /* Hidden by default */
            position: fixed; /* Stay in place */
            z-index: 1000; /* Sit on top */
            left: 0;
            top: 0;
            width: 100%; /* Full width */
            height: 100%; /* Full height */
            overflow: auto; /* Enable scroll if needed */
            background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
            justify-content: center;
            align-items: center;
        }
        .modal-content {
            background-color: #fefefe;
            margin: auto;
            padding: 20px;
            border-radius: 8px;
            width: 90%;
            max-width: 800px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            position: relative;
        }
        .close-button {
            color: #aaa;
            position: absolute;
            top: 10px;
            right: 20px;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }
        .close-button:hover,
        .close-button:focus {
            color: black;
            text-decoration: none;
            cursor: pointer;
        }
        .code-display { /* For non-interactive code/markdown */
            background-color: #e2e8f0; /* gray-200 */
            padding: 1rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            white-space: pre-wrap; /* Ensures long lines wrap */
            word-break: break-all; /* Breaks words if necessary */
            max-height: 70vh; /* Limit height for long content */
        }
        .interactive-template { /* For interactive bot role templates */
            max-height: 70vh;
            overflow-y: auto;
            padding: 1rem;
            border: 1px solid #e2e8f0;
            border-radius: 0.5rem;
            background-color: #f8fafc; /* gray-50 */
        }
    </style>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4">

    <div class="w-full max-w-5xl bg-white rounded-xl shadow-lg p-8 text-center">
        <h1 class="text-4xl font-extrabold text-gray-900 mb-8">Template Bot: Specialized Roles & Core Assets</h1>
        <p class="text-lg text-gray-700 mb-10">
            This template bot demonstrates various specialized functionalities and the underlying assets required for its operation.
            Click on a role or asset type to explore its conceptual details.
        </p>

        <h2 class="text-2xl font-bold text-gray-800 mb-6">Bot Roles (Interactive Templates)</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            <button class="btn btn-teal" onclick="showCode('content-creator')">
                Content Creator
            </button>
            <button class="btn btn-teal" onclick="showCode('prompt-creator')">
                Prompt Creator
            </button>
            <button class="btn btn-teal" onclick="showCode('media-creator')">
                Audio/Video/Image Creator
            </button>
            <button class="btn btn-teal" onclick="showCode('seo-writer')">
                SEO Writer
            </button>
            <button class="btn btn-teal" onclick="showCode('tutor')">
                Tutor
            </button>
            <button class="btn btn-teal" onclick="showCode('financial-consultant')">
                Financial Consultant
            </button>
            <button class="btn btn-teal" onclick="showCode('legal-consultant')">
                Legal Consultant
            </button>
            <button class="btn btn-teal" onclick="showCode('medical-consultant')">
                Medical Consultant
            </button>
            <button class="btn btn-teal" onclick="showCode('cook')">
                Cook
            </button>
            <button class="btn btn-teal" onclick="showCode('personal-assistant')">
                Personal Assistant (Work)
            </button>
            <button class="btn btn-teal" onclick="showCode('personal-secretary')">
                Personal Secretary (Casual)
            </button>
        </div>

        <h2 class="text-2xl font-bold text-gray-800 mb-6">Deployment & Core Assets (Code/Markdown)</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <button class="btn" onclick="showCode('pwa')">
                Progressive Web App (PWA)
            </button>
            <button class="btn" onclick="showCode('react-native')">
                Native Mobile App (React Native)
            </button>
            <button class="btn" onclick="showCode('hybrid')">
                Hybrid App (Capacitor/Cordova)
            </button>
            <button class="btn btn-green" onclick="showCode('training-data')">
                Training Data (.md Files)
            </button>
            <button class="btn btn-purple" onclick="showCode('small-llm-model')">
                Small LLM Models
            </button>
        </div>
    </div>

    <div id="pwaModal" class="modal">
        <div class="modal-content">
            <span class="close-button" onclick="closeModal('pwaModal')">&times;</span>
            <h2 class="text-2xl font-bold mb-4">Progressive Web App (PWA) Example</h2>
            <p class="mb-4 text-gray-700">
                This is a basic HTML structure for a PWA. In a real PWA, `manifest.json` and `service-worker.js` would be separate files in your project root.
            </p>
            <div id="pwaCode" class="code-display"></div>
        </div>
    </div>

    <div id="reactNativeModal" class="modal">
        <div class="modal-content">
            <span class="close-button" onclick="closeModal('reactNativeModal')">&times;</span>
            <h2 class="text-2xl font-bold mb-4">Native Mobile App (React Native) Guide</h2>
            <p class="mb-4 text-gray-700">
                React Native apps require a specific development environment. Below are instructions and the core `App.js` code.
            </p>
            <div id="reactNativeCode" class="code-display"></div>
        </div>
    </div>

    <div id="hybridModal" class="modal">
        <div class="modal-content">
            <span class="close-button" onclick="closeModal('hybridModal')">&times;</span>
            <h2 class="text-2xl font-bold mb-4">Hybrid App (Capacitor/Cordova) Example</h2>
            <p class="mb-4 text-gray-700">
                This HTML represents the web content that would be wrapped by a Capacitor or Cordova project.
            </p>
            <div id="hybridCode" class="code-display"></div>
        </div>
    </div>

    <div id="trainingDataModal" class="modal">
        <div class="modal-content">
            <span class="close-button" onclick="closeModal('trainingDataModal')">&times;</span>
            <h2 class="text-2xl font-bold mb-4">Training Data (.md Files) Example</h2>
            <p class="mb-4 text-gray-700">
                Markdown files can be used to store conversational training data for your bot.
            </p>
            <div id="trainingDataCode" class="code-display"></div>
        </div>
    </div>

    <div id="smallLlmModelModal" class="modal">
        <div class="modal-content">
            <span class="close-button" onclick="closeModal('smallLlmModelModal')">&times;</span>
            <h2 class="text-2xl font-bold mb-4">Small LLM Models Concept</h2>
            <p class="mb-4 text-gray-700">
                Small Language Models are optimized for specific tasks or on-device deployment.
            </p>
            <div id="smallLlmModelCode" class="code-display"></div>
        </div>
    </div>

    <div id="contentCreatorModal" class="modal">
        <div class="modal-content">
            <span class="close-button" onclick="closeModal('contentCreatorModal')">&times;</span>
            <div id="contentCreatorContent" class="interactive-template"></div>
        </div>
    </div>
    <div id="promptCreatorModal" class="modal">
        <div class="modal-content">
            <span class="close-button" onclick="closeModal('promptCreatorModal')">&times;</span>
            <div id="promptCreatorContent" class="interactive-template"></div>
        </div>
    </div>
    <div id="mediaCreatorModal" class="modal">
        <div class="modal-content">
            <span class="close-button" onclick="closeModal('mediaCreatorModal')">&times;</span>
            <div id="mediaCreatorContent" class="interactive-template"></div>
        </div>
    </div>
    <div id="seoWriterModal" class="modal">
        <div class="modal-content">
            <span class="close-button" onclick="closeModal('seoWriterModal')">&times;</span>
            <div id="seoWriterContent" class="interactive-template"></div>
        </div>
    </div>
    <div id="tutorModal" class="modal">
        <div class="modal-content">
            <span class="close-button" onclick="closeModal('tutorModal')">&times;</span>
            <div id="tutorContent" class="interactive-template"></div>
        </div>
    </div>
    <div id="financialConsultantModal" class="modal">
        <div class="modal-content">
            <span class="close-button" onclick="closeModal('financialConsultantModal')">&times;</span>
            <div id="financialConsultantContent" class="interactive-template"></div>
        </div>
    </div>
    <div id="legalConsultantModal" class="modal">
        <div class="modal-content">
            <span class="close-button" onclick="closeModal('legalConsultantModal')">&times;</span>
            <div id="legalConsultantContent" class="interactive-template"></div>
        </div>
    </div>
    <div id="medicalConsultantModal" class="modal">
        <div class="modal-content">
            <span class="close-button" onclick="closeModal('medicalConsultantModal')">&times;</span>
            <div id="medicalConsultantContent" class="interactive-template"></div>
        </div>
    </div>
    <div id="cookModal" class="modal">
        <div class="modal-content">
            <span class="close-button" onclick="closeModal('cookModal')">&times;</span>
            <div id="cookContent" class="interactive-template"></div>
        </div>
    </div>
    <div id="personalAssistantModal" class="modal">
        <div class="modal-content">
            <span class="close-button" onclick="closeModal('personalAssistantModal')">&times;</span>
            <div id="personalAssistantContent" class="interactive-template"></div>
        </div>
    </div>
    <div id="personalSecretaryModal" class="modal">
        <div class="modal-content">
            <span class="close-button" onclick="closeModal('personalSecretaryModal')">&times;</span>
            <div id="personalSecretaryContent" class="interactive-template"></div>
        </div>
    </div>

    <script>
        // Function to fetch and display content in a modal
        async function showCode(type) {
            let content = '';
            let modalId = '';
            let contentElementId = '';
            let filePath = '';
            let isCodeDisplay = true; // Flag to determine if it's a code/markdown display or interactive HTML

            switch (type) {
                case 'pwa':
                    filePath = './pwa-example.html';
                    modalId = 'pwaModal';
                    contentElementId = 'pwaCode';
                    break;
                case 'react-native':
                    filePath = './react-native-guide.md';
                    modalId = 'reactNativeModal';
                    contentElementId = 'reactNativeCode';
                    break;
                case 'hybrid':
                    filePath = './hybrid-example.html';
                    modalId = 'hybridModal';
                    contentElementId = 'hybridCode';
                    break;
                case 'training-data':
                    filePath = './training-data-example.md';
                    modalId = 'trainingDataModal';
                    contentElementId = 'trainingDataCode';
                    break;
                case 'small-llm-model':
                    filePath = './small-llm-model-guide.md';
                    modalId = 'smallLlmModelModal';
                    contentElementId = 'smallLlmModelCode';
                    break;
                // Bot Roles - these will load interactive HTML
                case 'content-creator':
                    filePath = './bot-roles-interactive/content-creator.html';
                    modalId = 'contentCreatorModal';
                    contentElementId = 'contentCreatorContent';
                    isCodeDisplay = false;
                    break;
                case 'prompt-creator':
                    filePath = './bot-roles-interactive/prompt-creator.html';
                    modalId = 'promptCreatorModal';
                    contentElementId = 'promptCreatorContent';
                    isCodeDisplay = false;
                    break;
                case 'media-creator':
                    filePath = './bot-roles-interactive/media-creator.html';
                    modalId = 'mediaCreatorModal';
                    contentElementId = 'mediaCreatorContent';
                    isCodeDisplay = false;
                    break;
                case 'seo-writer':
                    filePath = './bot-roles-interactive/seo-writer.html';
                    modalId = 'seoWriterModal';
                    contentElementId = 'seoWriterContent';
                    isCodeDisplay = false;
                    break;
                case 'tutor':
                    filePath = './bot-roles-interactive/tutor.html';
                    modalId = 'tutorModal';
                    contentElementId = 'tutorContent';
                    isCodeDisplay = false;
                    break;
                case 'financial-consultant':
                    filePath = './bot-roles-interactive/financial-consultant.html';
                    modalId = 'financialConsultantModal';
                    contentElementId = 'financialConsultantContent';
                    isCodeDisplay = false;
                    break;
                case 'legal-consultant':
                    filePath = './bot-roles-interactive/legal-consultant.html';
                    modalId = 'legalConsultantModal';
                    contentElementId = 'legalConsultantContent';
                    isCodeDisplay = false;
                    break;
                case 'medical-consultant':
                    filePath = './bot-roles-interactive/medical-consultant.html';
                    modalId = 'medicalConsultantModal';
                    contentElementId = 'medicalConsultantContent';
                    isCodeDisplay = false;
                    break;
                case 'cook':
                    filePath = './bot-roles-interactive/cook.html';
                    modalId = 'cookModal';
                    contentElementId = 'cookContent';
                    isCodeDisplay = false;
                    break;
                case 'personal-assistant':
                    filePath = './bot-roles-interactive/personal-assistant.html';
                    modalId = 'personalAssistantModal';
                    contentElementId = 'personalAssistantContent';
                    isCodeDisplay = false;
                    break;
                case 'personal-secretary':
                    filePath = './bot-roles-interactive/personal-secretary.html';
                    modalId = 'personalSecretaryModal';
                    contentElementId = 'personalSecretaryContent';
                    isCodeDisplay = false;
                    break;
            }

            try {
                // Fetch content from the specified file path
                const response = await fetch(filePath);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                content = await response.text();
            } catch (error) {
                console.error('Error fetching file:', filePath, error);
                content = `Failed to load content from ${filePath}.`;
            }

            const contentElement = document.getElementById(contentElementId);
            if (isCodeDisplay) {
                contentElement.textContent = content; // For raw code/markdown
            } else {
                contentElement.innerHTML = content; // For interactive HTML
                // Re-execute scripts within the loaded HTML for interactive templates
                const scripts = contentElement.querySelectorAll('script');
                scripts.forEach(oldScript => {
                    const newScript = document.createElement('script');
                    Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
                    newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                    oldScript.parentNode.replaceChild(newScript, oldScript);
                });
            }

            document.getElementById(modalId).style.display = 'flex'; // Use flex to center
        }

        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }

        // Add event listener for Escape key to close modals
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                const modals = document.querySelectorAll('.modal');
                modals.forEach(modal => {
                    if (modal.style.display === 'flex') {
                        modal.style.display = 'none';
                    }
                });
            }
        });

        // Close modal when clicking outside of it
        document.addEventListener('click', function(event) {
            const modals = document.querySelectorAll('.modal');
            modals.forEach(modal => {
                if (modal.style.display === 'flex' && !modal.querySelector('.modal-content').contains(event.target) && !event.target.closest('.btn')) {
                    modal.style.display = 'none';
                }
            });
        });

    </script>
</body>
</html>"""

    pwa_example_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot PWA Interface</title>
    <link rel="manifest" href="/manifest.json">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
    </style>
</head>
<body class="bg-gray-100 flex flex-col items-center justify-center min-h-screen p-4">
    <div class="w-full max-w-2xl bg-white rounded-xl shadow-lg p-6">
        <h1 class="text-3xl font-bold text-gray-800 mb-4 text-center">Your Bot's PWA</h1>
        <p class="text-gray-700 mb-6 text-center">
            This is where your bot's interactive interface and generated responses would appear.
            It's designed to be installable and work offline.
        </p>

        <div class="bg-blue-50 p-4 rounded-lg shadow-inner mb-4">
            <div id="chat-output" class="h-48 overflow-y-auto bg-white p-3 rounded-md border border-gray-200 mb-3 text-sm text-gray-800">
                <p class="mb-1"><span class="font-semibold text-blue-700">Bot:</span> Hello! How can I assist you today?</p>
            </div>
            <div class="flex">
                <input type="text" id="user-input" placeholder="Type your message..." class="flex-grow p-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                <button id="send-button" class="px-4 py-2 bg-blue-600 text-white rounded-r-md hover:bg-blue-700 transition-colors duration-300">Send</button>
            </div>
        </div>

        <p class="text-sm text-gray-500 text-center">
            To install this PWA, look for an "Add to Home Screen" or "Install App" option in your browser menu.
            (Requires manifest.json and service-worker.js to be present in the root.)
        </p>
    </div>

    <script>
        // Service Worker Registration (service-worker.js would be a separate file)
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                // navigator.serviceWorker.register('/service-worker.js')
                //     .then(registration => {
                //         console.log('Service Worker registered:', registration);
                //     })
                //     .catch(error => {
                //         console.error('Service Worker registration failed:', error);
                //     });
                console.log('Service Worker registration commented out for this demo. In a real PWA, uncomment this line and ensure service-worker.js exists.');
            });
        }

        // Basic Bot Interaction (for demonstration)
        document.addEventListener('DOMContentLoaded', () => {
            const userInput = document.getElementById('user-input');
            const sendButton = document.getElementById('send-button');
            const chatOutput = document.getElementById('chat-output');

            sendButton.addEventListener('click', () => {
                const message = userInput.value.trim();
                if (message) {
                    // Display user message
                    const userMessage = document.createElement('p');
                    userMessage.className = 'mb-1 text-right';
                    userMessage.innerHTML = `<span class="font-semibold text-green-700">You:</span> ${message}`;
                    chatOutput.appendChild(userMessage);

                    // Simulate bot response
                    setTimeout(() => {
                        const botResponse = document.createElement('p');
                        botResponse.className = 'mb-1';
                        botResponse.innerHTML = `<span class="font-semibold text-blue-700">Bot:</span> I received "${message}". How else can I help?`;
                        chatOutput.appendChild(botResponse);
                        chatOutput.scrollTop = chatOutput.scrollHeight; // Scroll to bottom
                    }, 500);

                    userInput.value = ''; // Clear input
                    chatOutput.scrollTop = chatOutput.scrollHeight; // Scroll to bottom
                }
            });

            userInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendButton.click();
                }
            });
        });
    </script>
</body>
</html>"""

    react_native_guide_md_content = """# Native Mobile App (React Native) Guide

To build a native mobile app with React Native, you'll need a development environment set up.

## Prerequisites

* Node.js and npm/yarn
* Expo CLI or React Native CLI
* Xcode (for iOS development on macOS)
* Android Studio (for Android development)

## Steps to Run

1.  **Create a new React Native project:**
    ```bash
    npx create-expo-app MyBotApp --template blank
    # or if using React Native CLI
    # npx react-native init MyBotApp
    ```

2.  **Navigate into your project directory:**
    ```bash
    cd MyBotApp
    ```

3.  **Replace `App.js` with the following code:**

    ```javascript
    import React, { useState } from 'react';
    import {
      SafeAreaView,
      StyleSheet,
      View,
      Text,
      TextInput,
      TouchableOpacity,
      ScrollView,
      KeyboardAvoidingView,
      Platform,
    } from 'react-native';

    const App = () => {
      const [messages, setMessages] = useState([
        { id: '1', sender: 'bot', text: 'Hello! How can I assist you today?' },
      ]);
      const [inputText, setInputText] = useState('');

      const handleSendMessage = () => {
        if (inputText.trim()) {
          const newUserMessage = { id: String(messages.length + 1), sender: 'user', text: inputText.trim() };
          setMessages((prevMessages) => [...prevMessages, newUserMessage]);
          setInputText('');

          // Simulate bot response
          setTimeout(() => {
            const botResponseText = `I received "${newUserMessage.text}". How else can I help?`;
            const newBotMessage = { id: String(messages.length + 2), sender: 'bot', text: botResponseText };
            setMessages((prevMessages) => [...prevMessages, newBotMessage]);
          }, 1000);
        }
      };

      return (
        <SafeAreaView style={styles.container}>
          <KeyboardAvoidingView
            style={styles.keyboardAvoidingView}
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 20} // Adjust offset as needed
          >
            <Text style={styles.header}>Your Bot's Native App</Text>

            <ScrollView style={styles.chatArea} contentContainerStyle={styles.chatContent}>
              {messages.map((message) => (
                <View
                  key={message.id}
                  style={[
                    styles.messageBubble,
                    message.sender === 'user' ? styles.userMessage : styles.botMessage,
                  ]}
                >
                  <Text style={message.sender === 'user' ? styles.userText : styles.botText}>
                    {message.sender === 'user' ? 'You: ' : 'Bot: '}
                    {message.text}
                  </Text>
                </View>
              ))}
            </ScrollView>

            <View style={styles.inputContainer}>
              <TextInput
                style={styles.textInput}
                placeholder="Type your message..."
                placeholderTextColor="#9ca3af"
                value={inputText}
                onChangeText={setInputText}
                onSubmitEditing={handleSendMessage} // Send on Enter key
                returnKeyType="send"
              />
              <TouchableOpacity style={styles.sendButton} onPress={handleSendMessage}>
                <Text style={styles.sendButtonText}>Send</Text>
              </TouchableOpacity>
            </View>
          </KeyboardAvoidingView>
        </SafeAreaView>
      );
    };

    const styles = StyleSheet.create({
      container: {
        flex: 1,
        backgroundColor: '#f3f4f6', // gray-100
      },
      keyboardAvoidingView: {
        flex: 1,
        justifyContent: 'space-between',
      },
      header: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#1f2937', // gray-800
        textAlign: 'center',
        paddingVertical: 16,
        backgroundColor: '#ffffff',
        borderBottomWidth: 1,
        borderBottomColor: '#e5e7eb', // gray-200
      },
      chatArea: {
        flex: 1,
        paddingHorizontal: 16,
        paddingVertical: 10,
      },
      chatContent: {
        justifyContent: 'flex-end', // Keep messages at the bottom
      },
      messageBubble: {
        maxWidth: '80%',
        padding: 10,
        borderRadius: 10,
        marginBottom: 8,
      },
      userMessage: {
        alignSelf: 'flex-end',
        backgroundColor: '#3b82f6', // blue-500
      },
      botMessage: {
        alignSelf: 'flex-start',
        backgroundColor: '#e0f2fe', // blue-100
      },
      userText: {
        color: '#ffffff',
      },
      botText: {
        color: '#1e3a8a', // blue-900
      },
      inputContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: 10,
        backgroundColor: '#ffffff',
        borderTopWidth: 1,
        borderTopColor: '#e5e7eb', // gray-200
      },
      textInput: {
        flex: 1,
        height: 40,
        borderColor: '#d1d5db', // gray-300
        borderWidth: 1,
        borderRadius: 20,
        paddingHorizontal: 15,
        marginRight: 10,
        fontSize: 16,
        color: '#1f2937', // gray-800
      },
      sendButton: {
        backgroundColor: '#2563eb', // blue-600
        paddingVertical: 10,
        paddingHorizontal: 15,
        borderRadius: 20,
      },
      sendButtonText: {
        color: '#ffffff',
        fontWeight: 'bold',
        fontSize: 16,
      },
    });

    export default App;
    ```

4.  **Run your app:**
    ```bash
    npx expo start
    # or
    # npx react-native run-ios
    # npx react-native run-android
    ```

    Follow the instructions in your terminal to open the app on an emulator or your physical device.

This setup provides a native mobile experience for your bot.
"""

    hybrid_example_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot Hybrid App Web Content</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 0;
            overflow: hidden; /* Prevent scrolling outside the main content */
        }
        #app-container {
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background-color: #f3f4f6; /* gray-100 */
        }
        .content-box {
            width: 95%; /* Responsive width */
            max-width: 600px; /* Max width for larger screens */
            background-color: #ffffff;
            border-radius: 12px; /* rounded-xl */
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); /* shadow-lg */
            padding: 24px; /* p-6 */
            text-align: center;
        }
    </style>
</head>
<body>
    <div id="app-container">
        <div class="content-box">
            <h1 class="text-3xl font-bold text-gray-800 mb-4">Your Bot's Hybrid App</h1>
            <p class="text-gray-700 mb-6">
                This is your web app running inside a native wrapper (Capacitor/Cordova).
                It leverages web technologies while gaining access to native device features.
            </p>
            <div class="bg-blue-50 p-4 rounded-lg shadow-inner mb-4">
                <p class="text-blue-800">
                    Imagine your interactive bot chat, input fields, and response displays here.
                </p>
                <button class="mt-4 px-6 py-3 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 transition-colors duration-300 shadow-md">
                    Interact with Bot
                </button>
            </div>
            <p class="text-sm text-gray-500 mt-4">
                Native features can be accessed via Capacitor/Cordova plugins.
            </p>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            console.log('Hybrid app web content loaded.');
            // This is where your bot's web app logic would go.
            // For a hybrid app, you might also import Capacitor/Cordova plugins here.
            // Example for Capacitor:
            // import { Camera } from '@capacitor/camera';
            // async function takePhoto() {
            //    const photo = await Camera.getPhoto({
            //        quality: 90,
            //        allowEditing: true,
            //        resultType: 'uri'
            //    });
            //    console.log(photo.webPath);
            // }
        });
    </script>
</body>
</html>"""

    training_data_example_md_content = """# Training Data Example for Your Bot

This Markdown file demonstrates how you might structure conversational training data for your bot. Each section can represent a different intent or topic, with example user queries and expected bot responses.

## Intent: Greeting
- User: Hello!
- User: Hi there.
- User: Good morning.
- User: Hey bot.
- Bot: Hello! How can I assist you today?
- Bot: Hi! What can I do for you?

## Intent: Farewell
- User: Goodbye.
- User: See you later.
- User: Bye.
- Bot: Goodbye! Have a great day.
- Bot: See you next time!

## Intent: Ask About Capabilities
- User: What can you do?
- User: What are your features?
- User: Can you help me with something?
- Bot: I can help you with content creation, prompt generation, media inquiries, SEO writing, tutoring, financial, legal, and medical consulting, cooking advice, and act as a personal assistant or secretary.
- Bot: My capabilities include generating text, creating prompts, assisting with media, optimizing for SEO, and providing specialized advice in various domains.

## Intent: Content Creation Request
- User: Write a blog post about AI.
- User: Generate an article on sustainable living.
- User: Create a short story.
- Bot: What specific topic within AI would you like for the blog post?
- Bot: Please provide more details for the article on sustainable living.

## Intent: Prompt Creation Request
- User: Give me a prompt for an image of a futuristic city.
- User: Design a prompt for a video on cooking.
- Bot: What style or specific elements should be included in the futuristic city image?
- Bot: For the cooking video, what cuisine or dish are you focusing on?

## Intent: Financial Advice Request
- User: How can I save money?
- User: What's a good investment?
- Bot: I can offer general financial tips. For personalized advice, please consult a certified financial advisor.
- Bot: Investment decisions depend on your risk tolerance and goals. I can provide educational resources, but professional consultation is recommended.

## Entities and Slots (Example)
- User: Book a meeting for **tomorrow** at **3 PM** with **John**.
- Intent: Schedule Meeting
- Slots:
    - date: tomorrow
    - time: 3 PM
    - attendee: John

## Key Principles for Training Data:
- **Diversity:** Include varied phrasing for the same intent.
- **Coverage:** Address all expected user intents and edge cases.
- **Clarity:** Ensure bot responses are clear and helpful.
- **Iteration:** Continuously update and expand your training data based on user interactions.
"""

    small_llm_model_guide_md_content = """# Small LLM Models: Concept and Use Cases

Small Language Models (SLLMs) are optimized versions of larger LLMs, designed for efficiency, specific tasks, or on-device deployment.

## What are Small LLM Models?

* **Fewer Parameters:** They have significantly fewer parameters than large models (e.g., billions vs. trillions), making them smaller in size.
* **Faster Inference:** Their smaller size leads to faster processing and lower computational requirements.
* **Specialization:** Often fine-tuned for specific tasks (e.g., sentiment analysis, summarization, specific domain chatbots) rather than general-purpose understanding.
* **Edge Deployment:** Can run on devices with limited resources (smartphones, IoT devices, embedded systems) without requiring constant cloud connectivity.

## Advantages

* **Cost-Effective:** Lower computational costs for training and inference.
* **Privacy:** Data can be processed locally, enhancing user privacy.
* **Low Latency:** Responses are quicker due to local processing.
* **Offline Capability:** Can function without an internet connection.
* **Resource Efficiency:** Ideal for environments with power or memory constraints.

## Common Techniques for Creating SLLMs

* **Quantization:** Reducing the precision of numerical representations (e.g., from float32 to int8) to decrease model size and speed up computation.
* **Pruning:** Removing redundant or less important connections (weights) in the neural network.
* **Distillation:** Training a smaller "student" model to mimic the behavior of a larger, more complex "teacher" model.
* **Parameter Efficient Fine-tuning (PEFT):** Methods like LoRA (Low-Rank Adaptation) that allow adapting large models to specific tasks with minimal trainable parameters.
* **Architectural Optimization:** Designing inherently smaller and more efficient model architectures.

## Use Cases for Your Bot

* **On-device processing:** Running core bot functionalities directly on a user's phone for instant responses (e.g., basic FAQs, common commands).
* **Specific intent recognition:** A small model dedicated solely to identifying if a user's query is about "financial advice" or "cooking."
* **Personalized recommendations:** A lightweight model trained on a user's local data to provide tailored suggestions.
* **Offline assistants:** Bots that provide essential functionality even without network access.
* **Edge AI applications:** Deploying the bot's core logic on industrial devices, smart home hubs, etc.

## Examples of SLLMs/Frameworks

* **Mobile-optimized models:** Many research efforts focus on creating models specifically for mobile.
* **Lite versions of larger models:** Companies release smaller versions of their flagship models (e.g., smaller versions of BERT, GPT-2).
* **TinyLlama, Phi-2, Gemma (smaller variants):** Recent developments are pushing powerful models into smaller footprints.
* **TensorFlow Lite / ONNX Runtime:** Frameworks for deploying machine learning models on edge devices.
"""

    content_creator_html_content = """<h2 class="text-2xl font-bold mb-4">Content Creator Bot Role</h2>
<p class="mb-4 text-gray-700">
    As a Content Creator Bot, I specialize in generating various forms of textual content.
    I can adapt my writing style, tone, and format based on your requirements.
</p>

<div class="mb-6">
    <label for="contentType" class="block text-left text-gray-800 text-sm font-medium mb-2">Select Content Type:</label>
    <select id="contentType" class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="blog_post">Blog Post</option>
        <option value="social_media_post">Social Media Post</option>
        <option value="email_newsletter">Email Newsletter</option>
        <option value="product_description">Product Description</option>
        <option value="story_snippet">Short Story / Snippet</option>
    </select>
</div>

<div class="mb-6">
    <label for="contentTopic" class="block text-left text-gray-800 text-sm font-medium mb-2">Topic/Keywords:</label>
    <input type="text" id="contentTopic" placeholder="e.g., benefits of remote work, new smartphone features"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>

<div class="mb-6">
    <label for="contentTone" class="block text-left text-gray-800 text-sm font-medium mb-2">Tone:</label>
    <input type="text" id="contentTone" placeholder="e.g., formal, casual, enthusiastic, persuasive"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>

<div class="mb-6">
    <label for="contentLength" class="block text-left text-gray-800 text-sm font-medium mb-2">Desired Length (words):</label>
    <input type="number" id="contentLength" value="200" min="50" max="2000"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>

<button class="btn btn-yellow w-full" onclick="generateContent()">Generate Content</button>

<div id="contentOutput" class="mt-8 bg-gray-50 p-4 rounded-md border border-gray-200 hidden">
    <h3 class="text-lg font-semibold mb-2">Generated Content:</h3>
    <p id="generatedText" class="text-left text-gray-800 text-sm"></p>
</div>

<script>
    function generateContent() {
        const type = document.getElementById('contentType').value;
        const topic = document.getElementById('contentTopic').value;
        const tone = document.getElementById('contentTone').value;
        const length = document.getElementById('contentLength').value;
        const outputDiv = document.getElementById('contentOutput');
        const generatedTextElem = document.getElementById('generatedText');

        if (!topic) {
            alert('Please provide a topic for the content!');
            return;
        }

        let placeholderContent = '';
        switch (type) {
            case 'blog_post':
                placeholderContent = `<h3>The Future of ${topic} in a ${tone} World</h3><p>In today's rapidly evolving landscape, the concept of ${topic} is becoming increasingly vital. This blog post will explore the nuances, challenges, and exciting opportunities that lie ahead. Our aim is to provide a comprehensive yet ${tone} overview, highlighting key aspects and offering fresh perspectives. We'll delve into how advancements are shaping its trajectory and what it means for the future. Stay tuned for deeper insights...</p><p>(This is a placeholder for a ${length}-word blog post on "${topic}" with a ${tone} tone.)</p>`;
                break;
            case 'social_media_post':
                placeholderContent = `✨ Dive into the world of ${topic}! 🚀 Discover why it's changing everything. #${topic.replace(/ /g, '')} #FutureIsNow (This is a placeholder for a ${tone} social media post.)`;
                break;
            case 'email_newsletter':
                placeholderContent = `Subject: Exciting Updates on ${topic}!

Dear Subscriber,

We're thrilled to bring you the latest insights on ${topic}. Our recent findings suggest... (This is a placeholder for a ${tone} email newsletter, approx. ${length} words.)`;
                break;
            case 'product_description':
                placeholderContent = `Introducing the revolutionary new product that harnesses the power of ${topic}! Experience unparalleled ${tone} performance and discover a new level of efficiency. Perfect for your needs! (This is a placeholder for a product description, approx. ${length} words.)`;
                break;
            case 'story_snippet':
                placeholderContent = `The old house creaked, echoing the whispers of ${topic} from forgotten times. Sarah, a ${tone} explorer, pushed open the dusty door, unaware of the adventure that awaited her within. (This is a placeholder for a short story snippet, approx. ${length} words.)`;
                break;
            default:
                placeholderContent = `Generating ${type} about ${topic} with a ${tone} tone and length of ${length} words. (Placeholder content)`;
        }

        generatedTextElem.innerHTML = placeholderContent;
        outputDiv.classList.remove('hidden');
        outputDiv.scrollIntoView({ behavior: 'smooth' });

        // In a real application, you'd send these parameters to a backend LLM API
        console.log(`Requesting: Type=${type}, Topic=${topic}, Tone=${tone}, Length=${length}`);
    }
</script>"""

    prompt_creator_html_content = """<h2 class="text-2xl font-bold mb-4">Prompt Creator Bot Role</h2>
<p class="mb-4 text-gray-700">
    As a Prompt Creator Bot, I help you craft effective prompts for various AI models,
    including text generation, image generation, and more.
</p>

<div class="mb-6">
    <label for="promptType" class="block text-left text-gray-800 text-sm font-medium mb-2">Select AI Model Type:</label>
    <select id="promptType" class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="text_generation">Text Generation (e.g., stories, articles)</option>
        <option value="image_generation">Image Generation (e.g., Midjourney, DALL-E)</option>
        <option value="code_generation">Code Generation</option>
        <option value="chatbot_persona">Chatbot Persona</option>
    </select>
</div>

<div class="mb-6">
    <label for="promptGoal" class="block text-left text-gray-800 text-sm font-medium mb-2">Desired Output/Goal:</label>
    <textarea id="promptGoal" rows="3" placeholder="e.g., a futuristic cityscape, a Python function for sorting, a friendly customer service bot"
              class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
</div>

<div class="mb-6">
    <label for="promptKeywords" class="block text-left text-gray-800 text-sm font-medium mb-2">Key Elements/Keywords (comma-separated):</label>
    <input type="text" id="promptKeywords" placeholder="e.g., cyberpunk, neon lights, rainy; quicksort, array; empathetic, concise"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>

<div class="mb-6">
    <label for="promptStyle" class="block text-left text-gray-800 text-sm font-medium mb-2">Style/Tone/Constraints:</label>
    <input type="text" id="promptStyle" placeholder="e.g., vibrant, cinematic, concise, Python 3.9"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>

<button class="btn btn-yellow w-full" onclick="generatePrompt()">Generate Prompt</button>

<div id="promptOutput" class="mt-8 bg-gray-50 p-4 rounded-md border border-gray-200 hidden">
    <h3 class="text-lg font-semibold mb-2">Generated Prompt:</h3>
    <pre id="generatedPromptText" class="text-left text-gray-800 text-sm whitespace-pre-wrap"></pre>
</div>

<script>
    function generatePrompt() {
        const type = document.getElementById('promptType').value;
        const goal = document.getElementById('promptGoal').value;
        const keywords = document.getElementById('promptKeywords').value;
        const style = document.getElementById('promptStyle').value;
        const outputDiv = document.getElementById('promptOutput');
        const generatedPromptTextElem = document.getElementById('generatedPromptText');

        if (!goal) {
            alert('Please describe the desired output/goal!');
            return;
        }

        let prompt = '';
        switch (type) {
            case 'text_generation':
                prompt = `Generate a text that accomplishes the following goal: "${goal}".
Include the following key elements/keywords: ${keywords}.
Adopt a ${style} style/tone.`;
                break;
            case 'image_generation':
                prompt = `Create an image with the main subject/concept: "${goal}".
Incorporate these visual elements/keywords: ${keywords}.
Apply a ${style} artistic style.`;
                break;
            case 'code_generation':
                prompt = `Write code to fulfill the requirement: "${goal}".
Utilize these programming concepts/keywords: ${keywords}.
Adhere to ${style} coding practices/language version.`;
                break;
            case 'chatbot_persona':
                prompt = `Design a chatbot persona with the primary function: "${goal}".
Key characteristics/traits: ${keywords}.
The bot should communicate in a ${style} manner.`;
                break;
            default:
                prompt = `Create a prompt for AI model type "${type}" with the goal: "${goal}", keywords: "${keywords}", and style: "${style}".`;
        }

        generatedPromptTextElem.textContent = prompt;
        outputDiv.classList.remove('hidden');
        outputDiv.scrollIntoView({ behavior: 'smooth' });

        console.log(`Prompt Request: Type=${type}, Goal=${goal}, Keywords=${keywords}, Style=${style}`);
    }
</script>"""

    media_creator_html_content = """<h2 class="text-2xl font-bold mb-4">Audio/Video/Image Creator Bot Role</h2>
<p class="mb-4 text-gray-700">
    As a Media Creator Bot, I can describe and outline specifications for audio, video, and image generation,
    acting as a bridge to specialized AI media creation tools.
</p>

<div class="mb-6">
    <label for="mediaType" class="block text-left text-gray-800 text-sm font-medium mb-2">Select Media Type:</label>
    <select id="mediaType" class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="image">Image</option>
        <option value="video">Video</option>
        <option value="audio">Audio/Music</option>
    </select>
</div>

<div class="mb-6">
    <label for="mediaDescription" class="block text-left text-gray-800 text-sm font-medium mb-2">Detailed Description:</label>
    <textarea id="mediaDescription" rows="4" placeholder="e.g., a serene forest with a waterfall at sunset, a tutorial on baking a cake, a relaxing ambient track"
              class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
</div>

<div class="mb-6">
    <label for="mediaStyle" class="block text-left text-gray-800 text-sm font-medium mb-2">Style/Mood/Genre:</label>
    <input type="text" id="mediaStyle" placeholder="e.g., photorealistic, anime, cinematic, classical, upbeat"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>

<div class="mb-6" id="imageOptions" style="display: block;">
    <label for="imageRatio" class="block text-left text-gray-800 text-sm font-medium mb-2">Aspect Ratio (Image):</label>
    <input type="text" id="imageRatio" placeholder="e.g., 16:9, 1:1, 4:3" value="16:9"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>

<div class="mb-6" id="videoOptions" style="display: none;">
    <label for="videoDuration" class="block text-left text-gray-800 text-sm font-medium mb-2">Duration (seconds, Video):</label>
    <input type="number" id="videoDuration" value="30" min="5" max="300"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
    <label for="videoElements" class="block text-left text-gray-800 text-sm font-medium mt-4 mb-2">Key Scenes/Elements (Video):</label>
    <textarea id="videoElements" rows="2" placeholder="e.g., opening shot of landscape, character introduction, climax"
              class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
</div>

<div class="mb-6" id="audioOptions" style="display: none;">
    <label for="audioDuration" class="block text-left text-gray-800 text-sm font-medium mb-2">Duration (seconds, Audio):</label>
    <input type="number" id="audioDuration" value="60" min="10" max="600"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
    <label for="audioInstruments" class="block text-left text-gray-800 text-sm font-medium mt-4 mb-2">Key Instruments/Sounds (Audio):</label>
    <input type="text" id="audioInstruments" placeholder="e.g., piano, strings, synthesizers, rain sounds"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>

<button class="btn btn-yellow w-full" onclick="generateMediaSpec()">Generate Media Specification</button>

<div id="mediaOutput" class="mt-8 bg-gray-50 p-4 rounded-md border border-gray-200 hidden">
    <h3 class="text-lg font-semibold mb-2">Generated Media Specification:</h3>
    <pre id="generatedMediaSpec" class="text-left text-gray-800 text-sm whitespace-pre-wrap"></pre>
</div>

<script>
    document.getElementById('mediaType').addEventListener('change', function() {
        document.getElementById('imageOptions').style.display = 'none';
        document.getElementById('videoOptions').style.display = 'none';
        document.getElementById('audioOptions').style.display = 'none';

        const selectedType = this.value;
        if (selectedType === 'image') {
            document.getElementById('imageOptions').style.display = 'block';
        } else if (selectedType === 'video') {
            document.getElementById('videoOptions').style.display = 'block';
        } else if (selectedType === 'audio') {
            document.getElementById('audioOptions').style.display = 'block';
        }
    });

    function generateMediaSpec() {
        const type = document.getElementById('mediaType').value;
        const description = document.getElementById('mediaDescription').value;
        const style = document.getElementById('mediaStyle').value;
        const outputDiv = document.getElementById('mediaOutput');
        const generatedSpecElem = document.getElementById('generatedMediaSpec');

        if (!description) {
            alert('Please provide a detailed description for the media!');
            return;
        }

        let spec = `Media Type: ${type.toUpperCase()}\n`;
        spec += `Description: ${description}\n`;
        spec += `Style/Mood/Genre: ${style}\n`;

        if (type === 'image') {
            const ratio = document.getElementById('imageRatio').value;
            spec += `Aspect Ratio: ${ratio}\n`;
        } else if (type === 'video') {
            const duration = document.getElementById('videoDuration').value;
            const elements = document.getElementById('videoElements').value;
            spec += `Duration: ${duration} seconds\n`;
            spec += `Key Scenes/Elements: ${elements}\n`;
        } else if (type === 'audio') {
            const duration = document.getElementById('audioDuration').value;
            const instruments = document.getElementById('audioInstruments').value;
            spec += `Duration: ${duration} seconds\n`;
            spec += `Key Instruments/Sounds: ${instruments}\n`;
        }

        spec += `\n--- AI Media Generation Prompt Suggestion ---\n`;

        let promptSuggestion = '';
        if (type === 'image') {
            promptSuggestion = `Generate a ${style} image of "${description}" with an aspect ratio of ${document.getElementById('imageRatio').value}.`;
        } else if (type === 'video') {
            promptSuggestion = `Create a ${style} video, ${document.getElementById('videoDuration').value} seconds long, depicting "${description}". Include scenes like: ${document.getElementById('videoElements').value}.`;
        } else if (type === 'audio') {
            promptSuggestion = `Compose a ${style} audio track, ${document.getElementById('audioDuration').value} seconds long, featuring "${description}". Highlight instruments/sounds such as: ${document.getElementById('audioInstruments').value}.`;
        }
        spec += promptSuggestion;


        generatedSpecElem.textContent = spec;
        outputDiv.classList.remove('hidden');
        outputDiv.scrollIntoView({ behavior: 'smooth' });

        console.log(`Media Spec Request: Type=${type}, Description=${description}, Style=${style}`);
    }
</script>"""

    seo_writer_html_content = """<h2 class="text-2xl font-bold mb-4">SEO Writer Bot Role</h2>
<p class="mb-4 text-gray-700">
    As an SEO Writer Bot, I can generate content optimized for search engines, focusing on keywords,
    readability, and clear structure.
</p>

<div class="mb-6">
    <label for="seoTopic" class="block text-left text-gray-800 text-sm font-medium mb-2">Main Topic/Subject:</label>
    <input type="text" id="seoTopic" placeholder="e.g., 'best noise-cancelling headphones', 'healthy meal prep ideas'"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>

<div class="mb-6">
    <label for="targetKeywords" class="block text-left text-gray-800 text-sm font-medium mb-2">Target Keywords (comma-separated):</label>
    <input type="text" id="targetKeywords" placeholder="e.g., 'noise cancelling headphones, quiet headphones, active noise cancellation'"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>

<div class="mb-6">
    <label for="audience" class="block text-left text-gray-800 text-sm font-medium mb-2">Target Audience:</label>
    <input type="text" id="audience" placeholder="e.g., 'tech enthusiasts', 'busy parents', 'students'"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>

<div class="mb-6">
    <label for="wordCount" class="block text-left text-gray-800 text-sm font-medium mb-2">Desired Word Count:</label>
    <input type="number" id="wordCount" value="500" min="200" max="5000"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>

<div class="mb-6">
    <label for="callToAction" class="block text-left text-gray-800 text-sm font-medium mb-2">Call to Action (Optional):</label>
    <input type="text" id="callToAction" placeholder="e.g., 'Shop Now', 'Learn More', 'Subscribe to our Newsletter'"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>

<button class="btn btn-yellow w-full" onclick="generateSeoContent()">Generate SEO Content Outline</button>

<div id="seoOutput" class="mt-8 bg-gray-50 p-4 rounded-md border border-gray-200 hidden">
    <h3 class="text-lg font-semibold mb-2">Generated SEO Content Outline:</h3>
    <pre id="generatedSeoText" class="text-left text-gray-800 text-sm whitespace-pre-wrap"></pre>
</div>

<script>
    function generateSeoContent() {
        const topic = document.getElementById('seoTopic').value;
        const keywords = document.getElementById('targetKeywords').value;
        const audience = document.getElementById('audience').value;
        const wordCount = document.getElementById('wordCount').value;
        const cta = document.getElementById('callToAction').value;
        const outputDiv = document.getElementById('seoOutput');
        const generatedTextElem = document.getElementById('generatedSeoText');

        if (!topic || !keywords) {
            alert('Please provide a main topic and target keywords!');
            return;
        }

        let outline = `SEO Content Outline for: "${topic}"\n`;
        outline += `Target Keywords: ${keywords}\n`;
        outline += `Target Audience: ${audience || 'General'}\n`;
        outline += `Desired Word Count: ${wordCount} words\n\n`;

        outline += `--- Proposed Structure ---\n`;
        outline += `1.  **Catchy Title:** [Include primary keyword] (e.g., "Unlock Pure Silence: The Ultimate Guide to Noise-Cancelling Headphones")\n`;
        outline += `2.  **Introduction:** Hook the reader, briefly introduce the problem/topic, and state the article's purpose. (Approx. 50-70 words)\n`;
        outline += `3.  **H2: Section 1 - Understanding [Sub-topic related to topic]** (e.g., "How Active Noise Cancellation Works")\n`;
        outline += `    * Bullet points or short paragraphs explaining concepts.\n`;
        outline += `    * Naturally integrate secondary keywords.\n`;
        outline += `4.  **H2: Section 2 - Benefits of [Topic] for [Audience]** (e.g., "Why Students Need Quiet Headphones for Focus")\n`;
        outline += `    * Address specific pain points and solutions for the target audience.\n`;
        outline += `5.  **H2: Section 3 - Key Factors When Choosing [Topic/Product]** (e.g., "Choosing the Best Noise-Cancelling Headphones: A Buyer's Guide")\n`;
        outline += `    * Features to look for, comparisons, etc.\n`;
        outline += `6.  **Conclusion:** Summarize key takeaways, reiterate the main message, and provide a strong ${cta ? 'Call to Action' : 'closing statement'}.\n`;
        if (cta) {
            outline += `    * Call to Action: "${cta}"\n`;
        }
        outline += `\n--- SEO Best Practices to Implement ---\n`;
        outline += `-   Keyword Density: Aim for natural integration of target keywords throughout (1-2%).\n`;
        outline += `-   Readability: Use short paragraphs, clear sentences, and transition words.\n`;
        outline += `-   Internal & External Links: Link to relevant pages on your site and authoritative external sources.\n`;
        outline += `-   Meta Description: Craft a compelling meta description (150-160 characters) incorporating keywords.\n`;
        outline += `-   Image Alt Text: Use descriptive alt text for any images.\n`;

        generatedTextElem.textContent = outline;
        outputDiv.classList.remove('hidden');
        outputDiv.scrollIntoView({ behavior: 'smooth' });

        console.log(`SEO Content Request: Topic=${topic}, Keywords=${keywords}, Audience=${audience}, WordCount=${wordCount}, CTA=${cta}`);
    }
</script>"""

    tutor_html_content = """<h2 class="text-2xl font-bold mb-4">Tutor Bot Role</h2>
<p class="mb-4 text-gray-700">
    As a Tutor Bot, I provide educational assistance across various subjects.
    I can explain concepts, provide examples, and answer questions to help you learn.
</p>

<div class="mb-6">
    <label for="subject" class="block text-left text-gray-800 text-sm font-medium mb-2">Subject:</label>
    <input type="text" id="subject" placeholder="e.g., Algebra, Physics, Python Programming, History"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>

<div class="mb-6">
    <label for="topic" class="block text-left text-gray-800 text-sm font-medium mb-2">Specific Topic/Concept:</label>
    <input type="text" id="topic" placeholder="e.g., quadratic equations, Newton's laws, recursion, French Revolution"
           class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>

<div class="mb-6">
    <label for="learningStyle" class="block text-left text-gray-800 text-sm font-medium mb-2">Preferred Learning Style:</label>
    <select id="learningStyle" class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="explain">Just explain the concept</option>
        <option value="examples">Provide examples</option>
        <option value="analogies">Use analogies</option>
        <option value="step_by_step">Give step-by-step instructions</option>
    </select>
</div>

<div class="mb-6">
    <label for="difficulty" class="block text-left text-gray-800 text-sm font-medium mb-2">Your Current Understanding Level:</label>
    <select id="difficulty" class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="beginner">Beginner</option>
        <option value="intermediate">Intermediate</option>
        <option value="advanced">Advanced</option>
    </select>
</div>

<button class="btn btn-yellow w-full" onclick="getTutorExplanation()">Get Explanation</button>

<div id="tutorOutput" class="mt-8 bg-gray-50 p-4 rounded-md border border-gray-200 hidden">
    <h3 class="text-lg font-semibold mb-2">Tutor Explanation:</h3>
    <p id="tutorText" class="text-left text-gray-800 text-sm"></p>
</div>

<script>
    function getTutorExplanation() {
        const subject = document.getElementById('subject').value;
        const topic = document.getElementById('topic').value;
        const style = document.getElementById('learningStyle').value;
        const difficulty = document.getElementById('difficulty').value;
        const outputDiv = document.getElementById('tutorOutput');
        const tutorTextElem = document.getElementById('tutorText');

        if (!subject || !topic) {
            alert('Please provide both a subject and a specific topic!');
            return;
        }

        let explanation = ``;
        if (style === 'explain') {
            explanation = `Okay, let's explain ${topic} in ${subject} at a ${difficulty} level.
            \n\n[Placeholder: Here I would provide a concise explanation of ${topic} tailored to a ${difficulty} learner in ${subject}.]`;
        } else if (style === 'examples') {
            explanation = `Certainly, here are some examples to illustrate ${topic} in ${subject}.
            \n\n[Placeholder: Here I would generate specific examples for ${topic} in ${subject} appropriate for a ${difficulty} level.]`;
        } else if (style === 'analogies') {
            explanation = `Great, let's try to understand ${topic} in ${subject} using an analogy.
            \n\n[Placeholder: Here I would create an analogy to help you grasp ${topic} in ${subject} at a ${difficulty} level.]`;
        } else if (style === 'step_by_step') {
            explanation = `No problem! Here's a step-by-step guide to understanding or solving problems related to ${topic} in ${subject}.
            \n\n[Placeholder: Here I would break down ${topic} in ${subject} into easy-to-follow steps for a ${difficulty} learner.]`;
        }

        explanation += `\n\nDo you have any specific questions or want to try a practice problem?`;

        tutorTextElem.textContent = explanation;
        outputDiv.classList.remove('hidden');
        outputDiv.scrollIntoView({ behavior: 'smooth' });

        console.log(`Tutor Request: Subject=${subject}, Topic=${topic}, Style=${style}, Difficulty=${difficulty}`);
    }
</script>"""

    financial_consultant_html_content = """<h2 class="text-2xl font-bold mb-4">Financial Consultant Bot Role</h2>
<p class="mb-4 text-gray-700">
    As a Financial Consultant Bot, I can provide general financial information, tips, and insights.
    **Disclaimer: I am an AI and cannot provide personalized financial advice. Always consult a certified financial advisor for specific situations.**
</p>

<div class="mb-6">
    <label for="financialArea" class="block text-left text-gray-800 text-sm font-medium mb-2">Area of Interest:</label>
    <select id="financialArea" class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="budgeting">Budgeting & Saving</option>
        <option value="investing_basics">Investing Basics</option>
        <option value="debt_management">Debt Management</option>
        <option value="retirement_planning">Retirement Planning</option>
        <option value="financial_literacy">General Financial Literacy</option>
    </select>
</div>

<div class="mb-6">
    <label for="specificQuestion" class="block text-left text-gray-800 text-sm font-medium mb-2">Your Specific Question/Scenario (Optional):</label>
    <textarea id="specificQuestion" rows="3" placeholder="e.g., 'How can I create a simple budget?', 'What are ETFs?', 'Should I pay off credit card debt first?'"
              class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
</div>

<button class="btn btn-yellow w-full" onclick="getFinancialAdvice()">Get Financial Insights</button>

<div id="financialOutput" class="mt-8 bg-gray-50 p-4 rounded-md border border-gray-200 hidden">
    <h3 class="text-lg font-semibold mb-2">Financial Insights:</h3>
    <p id="financialText" class="text-left text-gray-800 text-sm"></p>
    <p class="text-xs text-red-600 mt-4 font-semibold">
        **Disclaimer:** This is AI-generated general information and not personalized financial advice. Please consult a qualified financial professional.
    </p>
</div>

<script>
    function getFinancialAdvice() {
        const area = document.getElementById('financialArea').value;
        const question = document.getElementById('specificQuestion').value;
        const outputDiv = document.getElementById('financialOutput');
        const financialTextElem = document.getElementById('financialText');

        let advice = ``;
        if (question) {
            advice = `Regarding your question about "${question}" in the context of ${area}:\n\n`;
        } else {
            advice = `Here's some general information on ${area}:\n\n`;
        }

        switch (area) {
            case 'budgeting':
                advice += `**Budgeting & Saving:** A good starting point is the 50/30/20 rule (50% needs, 30% wants, 20% savings/debt). Track your income and expenses to understand where your money goes. Automate savings to make it consistent. Setting clear financial goals can also provide motivation.`;
                break;
            case 'investing_basics':
                advice += `**Investing Basics:** Start by understanding your risk tolerance. Diversification is key – don't put all your eggs in one basket. Common investment vehicles include stocks, bonds, mutual funds, and ETFs. Consider long-term goals and dollar-cost averaging.`;
                break;
            case 'debt_management':
                advice += `**Debt Management:** Prioritize high-interest debt first (e.g., credit cards). Strategies like the debt snowball (pay smallest debt first) or debt avalanche (pay highest interest debt first) can be effective. Avoid taking on new unnecessary debt.`;
                break;
            case 'retirement_planning':
                advice += `**Retirement Planning:** Start early to leverage compounding. Understand different retirement accounts like 401(k)s and IRAs, and aim to contribute enough to get any employer match. Regularly review your plan and adjust as life circumstances change.`;
                break;
            case 'financial_literacy':
                advice += `**General Financial Literacy:** Understanding personal finance involves managing money, budgeting, investing, and understanding credit. It's about making informed decisions to achieve financial well-being and security. Continuously educate yourself on financial topics.`;
                break;
        }

        financialTextElem.textContent = advice;
        outputDiv.classList.remove('hidden');
        outputDiv.scrollIntoView({ behavior: 'smooth' });

        console.log(`Financial Request: Area=${area}, Question=${question}`);
    }
</script>"""

    legal_consultant_html_content = """<h2 class="text-2xl font-bold mb-4">Legal Consultant Bot Role</h2>
<p class="mb-4 text-gray-700">
    As a Legal Consultant Bot, I can provide general legal information, summaries of laws, and common legal concepts.
    **Disclaimer: I am an AI and cannot provide legal advice or form an attorney-client relationship. Always consult a qualified legal professional for specific legal issues.**
</p>

<div class="mb-6">
    <label for="legalArea" class="block text-left text-gray-800 text-sm font-medium mb-2">Area of Law:</label>
    <select id="legalArea" class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="contract_law">Contract Law</option>
        <option value="intellectual_property">Intellectual Property (IP)</option>
        <option value="employment_law">Employment Law</option>
        <option value="data_privacy">Data Privacy (e.g., GDPR, CCPA)</option>
        <option value="consumer_rights">Consumer Rights</option>
    </select>
</div>

<div class="mb-6">
    <label for="legalQuestion" class="block text-left text-gray-800 text-sm font-medium mb-2">Your Specific Legal Question/Scenario (Optional):</label>
    <textarea id="legalQuestion" rows="3" placeholder="e.g., 'What makes a contract legally binding?', 'How do I trademark a logo?', 'What are my rights if I'm unfairly dismissed?'"
              class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
</div>

<button class="btn btn-yellow w-full" onclick="getLegalInfo()">Get Legal Information</button>

<div id="legalOutput" class="mt-8 bg-gray-50 p-4 rounded-md border border-gray-200 hidden">
    <h3 class="text-lg font-semibold mb-2">Legal Information:</h3>
    <p id="legalText" class="text-left text-gray-800 text-sm"></p>
    <p class="text-xs text-red-600 mt-4 font-semibold">
        **Disclaimer:** This is AI-generated general information and not personalized legal advice. Please consult a qualified legal professional.
    </p>
</div>

<script>
    function getLegalInfo() {
        const area = document.getElementById('legalArea').value;
        const question = document.getElementById('legalQuestion').value;
        const outputDiv = document.getElementById('legalOutput');
        const legalTextElem = document.getElementById('legalText');

        let info = ``;
        if (question) {
            info = `Regarding your question about "${question}" in the context of ${area}:\n\n`;
        } else {
            info = `Here's some general information on ${area}:\n\n`;
        }

        switch (area) {
            case 'contract_law':
                info += `**Contract Law:** A legally binding contract generally requires an offer, acceptance, consideration (exchange of value), and intent to create legal relations. It can be written or oral, though written is usually preferable for clarity and enforceability. Elements like capacity and legality are also crucial.`;
                break;
            case 'intellectual_property':
                info += `**Intellectual Property (IP):** IP refers to creations of the mind. Key types include patents (for inventions), copyrights (for original artistic/literary works), trademarks (for brands/logos), and trade secrets. Each has specific protection requirements and durations.`;
                break;
            case 'employment_law':
                info += `**Employment Law:** This covers rights and obligations between employers and employees. Topics include fair wages, working conditions, discrimination, harassment, dismissal, and workplace safety. Laws vary significantly by jurisdiction.`;
                break;
            case 'data_privacy':
                info += `**Data Privacy:** Laws like GDPR (Europe) and CCPA (California) focus on how personal data is collected, stored, processed, and shared. Key principles include consent, data minimization, security, and the right to access/delete data. Compliance is complex and critical for businesses.`;
                break;
            case 'consumer_rights':
                info += `**Consumer Rights:** These protect individuals when purchasing goods or services. Common rights include the right to safe products, accurate information, choice, and redress for faulty goods or poor services. Specific consumer protection acts vary by country/region.`;
                break;
        }

        legalTextElem.textContent = info;
        outputDiv.classList.remove('hidden');
        outputDiv.scrollIntoView({ behavior: 'smooth' });

        console.log(`Legal Request: Area=${area}, Question=${question}`);
    }
</script>"""

    medical_consultant_html_content = """<h2 class="text-2xl font-bold mb-4">Medical Consultant Bot Role</h2>
<p class="mb-4 text-gray-700">
    As a Medical Consultant Bot, I can provide general health information, descriptions of conditions, and common wellness advice.
    **Disclaimer: I am an AI and cannot provide medical diagnosis, treatment, or personalized medical advice. Always consult a qualified healthcare professional for any health concerns.**
</p>

<div class="mb-6">
    <label for="medicalArea" class="block text-left text-gray-800 text-sm font-medium mb-2">Area of Interest:</label>
    <select id="medicalArea" class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="general_wellness">General Wellness & Prevention</option>
        <option value="symptom_info">Common Symptom Information</option>
        <option value="nutrition">Nutrition & Diet</option>
        <option value="mental_health">Mental Health Basics</option>
        <option value="first_aid">Basic First Aid Principles</option>
    </select>
</div>

<div class="mb-6">
    <label for="medicalQuestion" class="block text-left text-gray-800 text-sm font-medium mb-2">Your Specific Health Question/Concern (Optional):</label>
    <textarea id="medicalQuestion" rows="3" placeholder="e.g., 'What are common cold symptoms?', 'How much water should I drink daily?', 'What is anxiety?'"
              class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
</div>

<button class="btn btn-yellow w-full" onclick="getMedicalInfo()">Get Health Information</button>

<div id="medicalOutput" class="mt-8 bg-gray-50 p-4 rounded-md border border-gray-200 hidden">
    <h3 class="text-lg font-semibold mb-2">Health Information:</h3>
    <p id="medicalText" class="text-left text-gray-800 text-sm"></p>
    <p class="text-xs text-red-600 mt-4 font-semibold">
        **Disclaimer:** This is AI-generated general information and not personalized medical advice. Always consult a qualified healthcare professional. In case of emergency, seek immediate medical attention.
    </p>
</div>

<script>
    function getMedicalInfo() {
        const area = document.getElementById('medicalArea').value;
        const question = document.getElementById('medicalQuestion').value;
        const outputDiv = document.getElementById('medicalOutput');
        const medicalTextElem = document.getElementById('medicalText');

        let info = ``;
        if (question) {
            info = `Regarding your question about "${question}" in the context of ${area}:\n\n`;
        } else {
            info = `Here's some general information on ${area}:\n\n`;
        }

        switch (area) {
            case 'general_wellness':
                info += `**General Wellness & Prevention:** Focus on a balanced diet, regular physical activity, sufficient sleep (7-9 hours for adults), stress management, and maintaining good hygiene. Regular check-ups with your doctor are also crucial for preventive care.`;
                break;
            case 'symptom_info':
                info += `**Common Symptom Information:** Many symptoms can indicate various conditions. For instance, a cough might be a cold, flu, allergies, or something more serious. It's important not to self-diagnose. If symptoms persist or worsen, please consult a doctor for proper diagnosis and treatment.`;
                break;
            case 'nutrition':
                info += `**Nutrition & Diet:** A healthy diet includes a variety of fruits, vegetables, whole grains, lean proteins, and healthy fats. Limit processed foods, excessive sugars, and unhealthy fats. Hydration by drinking enough water is also vital. Dietary needs can vary based on age, activity level, and health conditions.`;
                break;
            case 'mental_health':
                info += `**Mental Health Basics:** Mental health is as important as physical health. It involves emotional, psychological, and social well-being. Common conditions include anxiety and depression. Strategies for support include mindfulness, talking to trusted individuals, seeking professional therapy, and maintaining a healthy lifestyle.`;
                break;
            case 'first_aid':
                info += `**Basic First Aid Principles:** In an emergency, ensure safety (yours and the injured person's), call for professional help if needed (e.g., 911/emergency services), and provide immediate care. For minor cuts, clean and cover. For sprains, R.I.C.E. (Rest, Ice, Compression, Elevation). Always prioritize calling emergency services for serious injuries or sudden severe symptoms.`;
                break;
        }

        medicalTextElem.textContent = info;
        outputDiv.classList.remove('hidden');
        outputDiv.scrollIntoView({ behavior: 'smooth' });

        console.log(`Medical Request: Area=${area}, Question=${question}`);
    }
</script>"""

    cook_html_content = """<h2 class="text-2xl font-bold mb-4">Cook Bot Role</h2>
<p class="mb-4 text-gray-700">
    As a Cook Bot, I can assist you with recipes, cooking techniques, meal planning, and food knowledge.
    Just tell me what you need help with in the kitchen!
</p>

<div class="mb-6">
    <label for="cookRequestType" class="block text-left text-gray-800 text-sm font-medium mb-2">What do you need?</label>
    <select id="cookRequestType" class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="recipe">Recipe Suggestion</option>
        <option value="technique">Cooking Technique Explanation</option>
        <option value="ingredient_substitute">Ingredient Substitute</option>
        <option value="meal_planning">Meal Planning Tip</option>
        <option value="food_fact">Food Fact</option>
    </select>
</div>

<div class="mb-6">
    <label for="cookQuery" class="block text-left text-gray-800 text-sm font-medium mb-2">Your Specific Query:</label>
    <textarea id="cookQuery" rows="3" placeholder="e.g., 'a quick chicken dinner', 'how to properly sauté vegetables', 'substitute for butter', 'easy weeknight meals'"
              class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
</div>

<button class="btn btn-yellow w-full" onclick="getCookingAssistance()">Get Cooking Assistance</button>

<div id="cookOutput" class="mt-8 bg-gray-50 p-4 rounded-md border border-gray-200 hidden">
    <h3 class="text-lg font-semibold mb-2">Cooking Advice:</h3>
    <p id="cookText" class="text-left text-gray-800 text-sm"></p>
</div>

<script>
    function getCookingAssistance() {
        const requestType = document.getElementById('cookRequestType').value;
        const query = document.getElementById('cookQuery').value;
        const outputDiv = document.getElementById('cookOutput');
        const cookTextElem = document.getElementById('cookText');

        if (!query) {
            alert('Please tell me your cooking query!');
            return;
        }

        let assistance = ``;

        switch (requestType) {
            case 'recipe':
                assistance = `**Recipe Suggestion:** For "${query}", I suggest a quick and delicious [Placeholder: Specific Recipe Name].
                \n\n**Ingredients:** [Placeholder: List of ingredients]
                \n**Instructions:** [Placeholder: Step-by-step cooking instructions]
                \n\nEnjoy your meal!`;
                break;
            case 'technique':
                assistance = `**Cooking Technique Explanation: "${query}"**
                \n\n[Placeholder: Here I would explain the technique '${query}' in detail, including tips and common pitfalls. For example, for 'sautéing vegetables', I'd cover heat, oil, pan crowding, etc.]
                \n\nPractice makes perfect!`;
                break;
            case 'ingredient_substitute':
                assistance = `**Ingredient Substitute for "${query}"**
                \n\n[Placeholder: Here I would provide common and effective substitutes for '${query}', along with notes on quantity and impact on flavor/texture. For example, for 'butter', I'd suggest applesauce, mashed banana, or various oils.]
                \n\nHappy cooking!`;
                break;
            case 'meal_planning':
                assistance = `**Meal Planning Tip for "${query}"**
                \n\n[Placeholder: Here I would offer practical meal planning tips relevant to '${query}'. For 'easy weeknight meals', I'd suggest batch cooking, simple one-pan dishes, or theme nights.]
                \n\nConsistency is key to successful meal planning!`;
                break;
            case 'food_fact':
                assistance = `**Fun Food Fact about "${query}"**
                \n\n[Placeholder: Here I would share an interesting fact or bit of trivia related to '${query}'. For 'chocolate', I'd mention its origin or health benefits.]
                \n\nDid you know that?`;
                break;
        }

        cookTextElem.textContent = assistance;
        outputDiv.classList.remove('hidden');
        outputDiv.scrollIntoView({ behavior: 'smooth' });

        console.log(`Cook Bot Request: Type=${requestType}, Query=${query}`);
    }
</script>"""

    personal_assistant_html_content = """<h2 class="text-2xl font-bold mb-4">Personal Assistant Bot Role (Work-Oriented)</h2>
<p class="mb-4 text-gray-700">
    As your Personal Assistant Bot for work, I can help you manage tasks, schedule appointments,
    organize information, and draft professional communications.
</p>

<div class="mb-6">
    <label for="paTaskType" class="block text-left text-gray-800 text-sm font-medium mb-2">What can I help with?</label>
    <select id="paTaskType" class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="schedule_meeting">Schedule a meeting</option>
        <option value="draft_email">Draft an email</option>
        <option value="summarize_document">Summarize a document</option>
        <option value="create_todo">Create a to-do list item</option>
        <option value="research_topic">Research a topic</option>
    </select>
</div>

<div class="mb-6">
    <label for="paQuery" class="block text-left text-gray-800 text-sm font-medium mb-2">Details/Instructions:</label>
    <textarea id="paQuery" rows="3" placeholder="e.g., 'Meeting with John and Jane next Tuesday at 10 AM regarding Q3 report', 'Email to client about project delay', 'Key points from the attached PDF', 'Add 'Send Q4 budget' to my list'"
              class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
</div>

<button class="btn btn-yellow w-full" onclick="getPersonalAssistantHelp()">Get Assistance</button>

<div id="paOutput" class="mt-8 bg-gray-50 p-4 rounded-md border border-gray-200 hidden">
    <h3 class="text-lg font-semibold mb-2">Assistant Response:</h3>
    <p id="paText" class="text-left text-gray-800 text-sm"></p>
</div>

<script>
    function getPersonalAssistantHelp() {
        const taskType = document.getElementById('paTaskType').value;
        const query = document.getElementById('paQuery').value;
        const outputDiv = document.getElementById('paOutput');
        const paTextElem = document.getElementById('paText');

        if (!query) {
            alert('Please provide details for your request!');
            return;
        }

        let response = ``;

        switch (taskType) {
            case 'schedule_meeting':
                response = `**Scheduling Request:** I understand you want to schedule a meeting with the following details: "${query}".
                \n\n[Placeholder: I would now integrate with your calendar (e.g., Google Calendar, Outlook) to find availability and send invitations. Confirmation message would appear here.]
                \n\nConfirming your meeting details shortly!`;
                break;
            case 'draft_email':
                response = `**Email Draft Request:** I'll draft an email based on your instructions: "${query}".
                \n\n[Placeholder: Here I would generate a professional email draft based on the query. For example, Subject: 'Update on Project X Delay', Body: 'Dear [Client Name], I am writing to inform you...']
                \n\nReview the draft and let me know if any changes are needed.`;
                break;
            case 'summarize_document':
                response = `**Document Summarization Request:** Please provide the document or its content for summarization based on: "${query}".
                \n\n[Placeholder: If I had access to the document, I would provide a concise summary of key points and actionable insights here.]
                \n\nOnce you provide the document, I'll get started!`;
                break;
            case 'create_todo':
                response = `**To-Do Item Creation:** Adding "${query}" to your to-do list.
                \n\n[Placeholder: I would integrate with your task management app (e.g., Todoist, Asana) and confirm the addition.]
                \n\nConsider it done!`;
                break;
            case 'research_topic':
                response = `**Research Request:** I will gather information on "${query}".
                \n\n[Placeholder: I would perform a quick search and provide key findings, links to reputable sources, or a brief overview of the topic.]
                \n\nHere's what I found: ...`;
                break;
        }

        paTextElem.textContent = response;
        outputDiv.classList.remove('hidden');
        outputDiv.scrollIntoView({ behavior: 'smooth' });

        console.log(`PA Request: Task=${taskType}, Query=${query}`);
    }
</script>"""

    personal_secretary_html_content = """<h2 class="text-2xl font-bold mb-4">Personal Secretary Bot Role (Casual/Home)</h2>
<p class="mb-4 text-gray-700">
    As your Personal Secretary Bot for casual and home-related tasks, I can help you with reminders,
    shopping lists, simple inquiries, and personal organization.
</p>

<div class="mb-6">
    <label for="psTaskType" class="block text-left text-gray-800 text-sm font-medium mb-2">How can I assist you at home?</label>
    <select id="psTaskType" class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="set_reminder">Set a reminder</option>
        <option value="add_to_shopping">Add to shopping list</option>
        <option value="answer_casual_q">Answer a casual question</option>
        <option value="plan_event">Help plan a personal event</option>
        <option value="suggest_activity">Suggest a leisure activity</option>
    </select>
</div>

<div class="mb-6">
    <label for="psQuery" class="block text-left text-gray-800 text-sm font-medium mb-2">Details/Instructions:</label>
    <textarea id="psQuery" rows="3" placeholder="e.g., 'Remind me to water plants daily at 7 PM', 'Add milk and eggs to grocery list', 'What's the weather tomorrow?', 'Plan a birthday party for my kid', 'Suggest a movie to watch tonight'"
              class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
</div>

<button class="btn btn-yellow w-full" onclick="getPersonalSecretaryHelp()">Get Assistance</button>

<div id="psOutput" class="mt-8 bg-gray-50 p-4 rounded-md border border-gray-200 hidden">
    <h3 class="text-lg font-semibold mb-2">Secretary Response:</h3>
    <p id="psText" class="text-left text-gray-800 text-sm"></p>
</div>

<script>
    function getPersonalSecretaryHelp() {
        const taskType = document.getElementById('psTaskType').value;
        const query = document.getElementById('psQuery').value;
        const outputDiv = document.getElementById('psOutput');
        const psTextElem = document.getElementById('psText');

        if (!query) {
            alert('Please provide details for your request!');
            return;
        }

        let response = ``;

        switch (taskType) {
            case 'set_reminder':
                response = `**Reminder Set:** I've noted down your reminder: "${query}".
                \n\n[Placeholder: I would integrate with your chosen reminder app or system (e.g., phone's reminders, smart speaker) and confirm.]
                \n\nI'll make sure you don't forget!`;
                break;
            case 'add_to_shopping':
                response = `**Shopping List Update:** Adding "${query}" to your shopping list.
                \n\n[Placeholder: I would integrate with your shopping list app (e.g., Google Keep, AnyList) and confirm the addition.]
                \n\nYour list is updated!`;
                break;
            case 'answer_casual_q':
                response = `**Casual Inquiry:** You asked: "${query}".
                \n\n[Placeholder: Here I would provide a factual, quick answer to a general knowledge or real-time query, e.g., 'The weather tomorrow in your area is expected to be sunny with a high of 25°C.']
                \n\nHope that helps!`;
                break;
            case 'plan_event':
                response = `**Event Planning Assistance:** Let's plan "${query}". What's the occasion and desired date?
                \n\n[Placeholder: I would ask follow-up questions to gather details (e.g., guest count, theme, budget) and help brainstorm ideas or find local vendors.]
                \n\nTell me more so we can make it perfect!`;
                break;
            case 'suggest_activity':
                response = `**Activity Suggestion:** For "${query}", how about trying...
                \n\n[Placeholder: I would suggest a movie, book, game, outdoor activity, or restaurant based on the query and your preferences.]
                \n\nHope you have fun!`;
                break;
        }

        psTextElem.textContent = response;
        outputDiv.classList.remove('hidden');
        outputDiv.scrollIntoView({ behavior: 'smooth' });

        console.log(`PS Request: Task=${taskType}, Query=${query}`);
    }
</script>"""

    # --- File Creation ---

    # Main HTML file
    create_file(os.path.join(project_root, "index.html"), index_html_content)

    # Core Assets
    create_file(os.path.join(project_root, "pwa-example.html"), pwa_example_html_content)
    create_file(os.path.join(project_root, "react-native-guide.md"), react_native_guide_md_content)
    create_file(os.path.join(project_root, "hybrid-example.html"), hybrid_example_html_content)
    create_file(os.path.join(project_root, "training-data-example.md"), training_data_example_md_content)
    create_file(os.path.join(project_root, "small-llm-model-guide.md"), small_llm_model_guide_md_content)

    # Bot Roles (interactive HTML)
    bot_roles_dir = os.path.join(project_root, "bot-roles-interactive")
    create_file(os.path.join(bot_roles_dir, "content-creator.html"), content_creator_html_content)
    create_file(os.path.join(bot_roles_dir, "prompt-creator.html"), prompt_creator_html_content)
    create_file(os.path.join(bot_roles_dir, "media-creator.html"), media_creator_html_content)
    create_file(os.path.join(bot_roles_dir, "seo-writer.html"), seo_writer_html_content)
    create_file(os.path.join(bot_roles_dir, "tutor.html"), tutor_html_content)
    create_file(os.path.join(bot_roles_dir, "financial-consultant.html"), financial_consultant_html_content)
    create_file(os.path.join(bot_roles_dir, "legal-consultant.html"), legal_consultant_html_content)
    create_file(os.path.join(bot_roles_dir, "medical-consultant.html"), medical_consultant_html_content)
    create_file(os.path.join(bot_roles_dir, "cook.html"), cook_html_content)
    create_file(os.path.join(bot_roles_dir, "personal-assistant.html"), personal_assistant_html_content)
    create_file(os.path.join(bot_roles_dir, "personal-secretary.html"), personal_secretary_html_content)

if __name__ == "__main__":
    setup_template_bot_project()
    print("\nProject setup complete! Navigate to 'template_bot_project' directory and open 'index.html' in your browser.")