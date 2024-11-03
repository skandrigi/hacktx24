# Mergr 🍒

Mergr is an interactive, command line interface application designed to simplify Git merge conflict resolution. It provides a visual interface for navigating through conflicting files and offers several options for handling conflicts: accepting the current version, incoming changes, or both.

Mergr integrates conflict detection, resolution, and staged merging into a unified and easy-to-use experience. This changes the developer experience for beginners who often struggle with understanding merge conflicts.

---

## Features

- **Conflict Detection and Highlighting**: Detects merge conflicts in selected files and highlights them with clear separation between current and incoming changes.
- **Multiple Resolution Options**: Allows you to resolve conflicts by accepting the current changes, incoming changes, a combination of both, and in the future provides AI-suggested resolutions.
- **AI-Powered Suggestions (Future)**: Integration with OpenAI provides suggestions based on context, assisting in complex conflict resolution.
- **Keyboard Binding for Efficiency**: Streamlined keyboard navigation and shortcuts enable rapid conflict resolution.
- **Visual Conflict Indicators**: A user-friendly, color-coded display that helps users visually track the sections of code in conflict.
- **Temporary Pop-up Messages**: Briefly displays pop-up notifications to guide or inform you during the resolution process.

---

## Getting Started

### Prerequisites

- **Python 3.7 or later** with the `textual` and `uv` libraries installed.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/mergr.git
   cd mergr
   ```

2. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Set up your OpenAI API key for AI-powered conflict suggestions. Replace `"your_openai_api_key_here"` in `ScreenApp` initialization.

### Running the App

To start the application, use:

```bash
uv run main.py
```
