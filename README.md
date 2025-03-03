# Hacker News Reader

## Description

This is a command-line news reader that fetches articles from the Hacker News API and summarizes them using the Sumy library. The application provides an intuitive user interface for browsing top, new, and best stories, as well as reading article summaries.

## Features

- Fetches up to 5 articles per section
- Provides a summary of each article
- Allows users to choose another article to read or exit the program
- Displays available sections with their corresponding numbers

## Project Structure

### `news-reader.py`

This file contains the main application code, organized into separate functions for clarity and maintainability. The code uses libraries such as `requests`, `tqdm`, `tabulate`, and `textwrap` to enhance user experience.

### `summarizer.py`

This is a modified version of the Sumy summarizer library, which I used to generate summaries for article text. I made adjustments to ensure correct formatting after summarization and limited the summary length to 5 sentences.

### `requirements.txt`

This file lists the dependencies required to run the application, including the Sumy summarizer library.

## Future Development

If given more time, I would like to develop this project into a full-fledged mobile application with additional features, such as:

- Bookmarking articles for later reading
- Increasing the number of article titles displayed per section
- Enhancing user interface and experience

## Code Organization

The code is organized into separate functions, each performing a specific task. This structure makes it easier to maintain and modify the application.
