# PromptForge Mobile - Dynamic AI Prompt Generator

## Overview
PromptForge Mobile is a hybrid mobile application that helps users create robust, tool-specific prompts for various AI tools. The application features a cyberpunk dark neon UI, camera integration for text extraction, and offline support for creating prompts on the go.

## Key Features
- **Camera Integration**: Capture images and extract text to use as a starting point for prompts
- **Dynamic Questionnaire**: Adapts based on the selected template and initial input
- **Multiple Templates**: Pre-defined templates for different AI use cases (code generation, content creation, image generation, text-to-video)
- **Tool-specific Prompt Construction**: Generates optimized prompts for different AI tools
- **Offline Support**: Create and save prompts even when offline
- **Local Storage**: Save and reuse prompts across sessions
- **Mobile-Optimized UI**: Cyberpunk dark neon theme designed for mobile devices

## Technical Implementation
- Built with React and TypeScript
- Uses Capacitor for native mobile functionality
- Camera access via Capacitor Camera plugin
- Simulated on-device AI text extraction (can be replaced with real ML implementation)
- Offline detection and synchronization
- Responsive design for all mobile screen sizes

## Installation and Setup

### Prerequisites
- Node.js (v16 or higher)
- npm or pnpm
- Android Studio (for Android builds)
- Xcode (for iOS builds, macOS only)

### Installation Steps
1. Clone the repository or extract the provided files
2. Navigate to the project directory
3. Install dependencies:
   ```
   pnpm install
   ```
4. Build the web assets:
   ```
   pnpm run build
   ```
5. Sync with Capacitor:
   ```
   npx cap sync
   ```

### Running on Android
1. Open the Android project in Android Studio:
   ```
   npx cap open android
   ```
2. Build and run the project on a device or emulator

### Running on iOS (macOS only)
1. Add the iOS platform:
   ```
   npx cap add ios
   ```
2. Open the iOS project in Xcode:
   ```
   npx cap open ios
   ```
3. Build and run the project on a device or simulator

## Usage Guide

### Creating a New Prompt with Camera
1. Tap the "Use Camera Input" button on the home screen
2. Take a photo of text, notes, or any visual reference
3. The app will extract text from the image
4. Use the extracted text as a starting point for your prompt
5. Continue with the questionnaire to refine your prompt

### Creating a New Prompt Manually
1. Enter a brief description of what you want to create in the text area on the home screen, or select a template directly
2. Fill out the dynamic questionnaire with details specific to your needs
3. Review the generated prompt and make any necessary adjustments
4. Copy or share the prompt to use with your preferred AI tool, or save it for future use

### Managing Saved Prompts
1. Navigate to the "Saved Prompts" page to view all your saved prompts
2. Tap "View" to see the full prompt
3. Tap "Delete" to remove a prompt from your saved list
4. Prompts are saved locally and can be accessed even when offline

## Offline Functionality
- The app detects when you're offline and notifies you
- All prompts created while offline are saved locally
- When you come back online, any pending changes are synchronized

## Project Structure
- `src/components/`: React components for the UI
- `src/context/`: Context providers for state management
- `src/data/`: Data files including questionnaire templates
- `src/hooks/`: Custom React hooks including camera and offline support
- `src/pages/`: Page components for routing
- `src/types/`: TypeScript type definitions
- `android/`: Android platform files

## Customization
- To add new templates, edit the `questionnaireTemplates.ts` file in the `src/data/` directory
- To modify the UI theme, edit the CSS variables in `src/index.css`
- To implement real ML-based text extraction, replace the mock function in `useCameraWithTextExtraction.ts`

## Technologies Used
- React
- TypeScript
- Capacitor
- Tailwind CSS
- Local Storage API
