# Hub-Wife Chat 💬

A witty AI-powered conversation simulator that creates entertaining banter between a husband and wife using different AI models. This Streamlit application allows you to configure the conversation topic, select different AI models for each character, and watch as they engage in humorous exchanges.

image.png

## Features

- 🤖 **Multi-Model Support**: Choose from GPT-4o or Claude 3.5 Haiku for each character
- 💭 **Customizable Topics**: Set any conversation topic or argument theme
- 🎭 **Character Personalities**: 
  - **Husband**: Calm, echoistic, with witty and comedic responses
  - **Wife**: Narcissistic, argumentative, easily annoyed by humor
- ✨ **Real-time Streaming**: Messages appear with a typing effect for a natural conversation feel
- 🎨 **Beautiful UI**: Chat-style interface with color-coded message bubbles
- 📊 **Progress Tracking**: Visual progress bar showing conversation status
- 🔄 **Flexible Iterations**: Configure the number of back-and-forth exchanges (1-20)

## Prerequisites

- Python 3.12 or higher
- OpenAI API key (for GPT models)
- Anthropic API key (for Claude models)
- `uv` package manager (recommended) or `pip`

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd hub-wife-chat
   ```

2. **Install dependencies using `uv` (recommended):**
   ```bash
   uv sync
   ```

   Or using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file in the project root:**
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

## Usage

1. **Start the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

   Or with `uv`:
   ```bash
   uv run streamlit run app.py
   ```

2. **Configure the conversation:**
   - Enter a **Topic of Fight** (e.g., "Who should do the dishes tonight")
   - Set the **Number of Iterations** (1-20)
   - Select AI models for **Husband** and **Wife** from the dropdown menus

3. **Start the conversation:**
   - Click the **"▶️ Start Conversation"** button
   - Watch as the characters exchange witty banter with a streaming typing effect
   - Monitor progress in the sidebar

4. **Clear and restart:**
   - Use the **"🗑️ Clear Conversation"** button to reset and start fresh

## Configuration

### Supported Models

- **OpenAI Models:**
  - `gpt-4o`

- **Anthropic Models:**
  - `claude-3-5-haiku-latest`

### Environment Variables

The application requires the following environment variables (set in `.env` file):

- `OPENAI_API_KEY`: Your OpenAI API key for GPT models
- `ANTHROPIC_API_KEY`: Your Anthropic API key for Claude models

## Project Structure

```
hub-wife-chat/
├── app.py              # Main Streamlit application
├── main.py             # Alternative entry point (if exists)
├── pyproject.toml      # Project dependencies and metadata
├── uv.lock             # Lock file for dependency versions
├── .env                # Environment variables (create this)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## How It Works

1. **Character Setup**: Each character (husband/wife) has a distinct personality defined by system prompts:
   - The husband is calm and echoistic, responding with witty one-liners
   - The wife is narcissistic and argumentative, getting annoyed by humor

2. **Conversation Flow**:
   - Starts with greeting messages ("Hi Honey" / "Hi")
   - Alternates between husband and wife responses
   - Each iteration adds two messages (one from each character)
   - Messages are generated using the selected AI models

3. **Streaming Effect**: Messages appear character-by-character with a typing cursor for a natural feel

4. **Error Handling**: API errors are displayed in the chat bubbles for debugging

## Technology Stack

- **Streamlit**: Web application framework
- **OpenAI Python SDK**: For GPT model interactions
- **Anthropic API**: For Claude model interactions (via OpenAI-compatible interface)
- **python-dotenv**: Environment variable management

## Dependencies

- `streamlit >= 1.51.0`
- `openai >= 2.7.2`
- `dotenv >= 0.9.9`
- Python >= 3.12

## Tips

- Try different model combinations (e.g., GPT-4o for husband, Claude for wife) for varied conversation styles
- Experiment with different topics to see how the personalities react
- Adjust the number of iterations to control conversation length
- The app works in both light and dark themes with proper text visibility

## Troubleshooting

### API Key Errors

If you see errors like "The api_key client option must be set":
- Ensure your `.env` file exists in the project root
- Verify that your API keys are correctly set in the `.env` file
- Check that the environment variables are loaded (the app uses `load_dotenv()`)

### Model Not Responding

- Verify your API keys have sufficient credits/quota
- Check your internet connection
- Ensure the model name matches exactly (case-sensitive)

## License

This project is open source and available for personal and educational use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

**Note**: This application is for entertainment purposes and simulates fictional character interactions. The personality traits described are exaggerated for comedic effect and do not represent real psychological conditions.

