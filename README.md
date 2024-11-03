# Mergr 🍒

Mergr is an interactive, command line interface application designed to simplify Git merge conflict resolution. It provides a visual interface for navigating through conflicting files and offers several options for handling conflicts: accepting the current version, incoming changes, or both.

Mergr integrates conflict detection, resolution, and staged merging into a unified and easy-to-use experience. This changes the developer experience for beginners who often struggle with understanding merge conflicts.

---

## Features

- **✅ Conflict Detection and Highlighting**: Detects merge conflicts in selected files and highlights them with clear separation between current and incoming changes.
- **⚙️ Multiple Resolution Options**: Allows you to resolve conflicts by accepting the current changes, incoming changes, a combination of both, or (in the future) AI-suggested resolutions.
- **🤖 AI-Powered Suggestions**: Integration with OpenAI provides suggestions based on context, assisting in complex conflict resolution.
- **💻 Keyboard Binding for Efficiency**: Streamlined keyboard navigation and shortcuts enable rapid conflict resolution.
- **🤩 Visual Conflict Indicators**: A user-friendly, color-coded display that helps users visually track the sections of code in conflict.
- **🛎️ Temporary Alerts**: Briefly displays pop-up notifications to guide and inform you during the resolution process.

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
   uv sync
   ```

3. (Optional) Set up your OpenAI API key for AI-powered conflict suggestions.

   ```bash
   export OPENAI_API_KEY=<sk-yourkey>
   ```

### Running the App

To start the application, use:

   ```bash
   uv run main.py
   ```
