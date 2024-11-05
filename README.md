
# Tourist Chatbot for Northern Caucasus Resort Cities

This project is a multilingual Telegram chatbot designed to help users explore popular attractions in resort cities of the Northern Caucasus. The bot supports Russian and Chinese languages, providing up-to-date information about various cities and landmarks in the region. Administrators have access to special commands for managing users and viewing popular search queries.

## Features

- **Multilingual Support**: Users can interact with the bot in Russian and Chinese.
- **City and Attraction Listings**: Users can browse cities and attractions with inline keyboard navigation.
- **Popular Searches**: Displays a list of the top 10 most popular attractions requested by users.
- **Voice Command Support**: Users can send voice messages to search for cities and attractions, which the bot converts to text and processes.
- **Admin Commands**: Special commands allow admins to view the user list, send messages, and monitor popular search trends.
- **Modular Structure**: Easily scalable and adaptable for adding new locations or additional languages.

## Setup and Installation

### Prerequisites
- Python 3.6+
- Telegram Bot API token (place in a `TOKEN.txt` file)
- Required libraries (install via `pip`):
  ```bash
  pip install pyTelegramBotAPI speechrecognition transliterate pypinyin
  ```

### Directory Structure
- `DB/`: Contains the main database of city and attraction information, organized by language.
- `Messege/`: Stores user messages to analyze popular search trends.
- `Users/`: Stores user information for admin management.
- `UaP/`: Tracks language preferences for each user.

### Running the Bot
1. Clone the repository and navigate to the project folder.
   ```bash
   git clone https://github.com/yourusername/tourist-chatbot.git
   cd tourist-chatbot
   ```
2. Place your Telegram Bot token in a file named `TOKEN.txt`.
3. Run the bot:
   ```bash
   python main.py
   ```

## Commands

### User Commands
- `/start`: Start the bot, select language, and view initial options.
- `/help`: View available commands and their descriptions.
- `/popular`: Display the 10 most popular attractions.

### Admin Commands
- `/users`: Display the list of all bot users.
- `/sendyorescode`: Sends the current bot code in parts to the admin.
- `/message`: Allows admins to send a message to any user by specifying the user’s ID.
  
### Additional Features
- **Voice Recognition**: Users can send voice messages with attraction names to receive information.
- **Dynamic Search with Pagination**: Users can navigate through cities and attractions using interactive buttons.

## Code Structure

### Key Functions
- **`updDB()`**: Updates city and attraction data from the `DB/` directory.
- **`updpopular()`**: Analyzes messages to identify the top 10 popular searches.
- **`mesegereply()`**: Processes text commands from users, determining whether the input is a city, attraction, or other query.
- **`voice_processing()`**: Converts voice messages to text and processes them as a search query.

### Inline Keyboard
The bot dynamically generates inline keyboard buttons for navigating through lists of cities and attractions, with pages limited by the `On_page` and `Max_page` variables.

### Logging and User Profiles
User profiles are stored in the `Users/` directory, and logs of their interactions are saved in `Messege/` for analysis of popular searches.

## Future Improvements
- Expand language support to include English and other languages.
- Implement additional admin tools for better analytics and user management.
- Optimize search for more efficient voice and text processing.


