import requests
from tqdm import tqdm
from tabulate import tabulate
from textwrap import fill
from summarizer import summarize
import sys


BASE_URL = "https://hacker-news.firebaseio.com/v0/{section}.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"
SECTIONS = {1: "topstories", 2: "newstories", 3: "beststories"}


def format_error(message):  # Print error messages in red.
    print(f"\033[91m{message}\033[0m")


def validate_input(prompt, choices):
    """Prompts user for input and validates against allowed choices."""
    while True:
        try:
            choice = int(input(prompt))
            if choice in choices:
                return choice
            else:
                format_error("Please enter a valid input.")
        except ValueError:
            format_error("Invalid input.")


def fetch_data(url):
    """Fetch data from the given API URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        sys.exit(format_error(e))


def fetch_article_ids(section_choice):
    """Retrieve article IDs for the selected section."""
    url = BASE_URL.format(section=SECTIONS[section_choice])
    article_ids = fetch_data(url)
    if not article_ids:
        sys.exit(format_error("No articles found."))
    return article_ids


def fetch_articles(article_ids, max_articles=5):
    """Fetch article details using the article IDs."""
    articles = []

    # Progress bar while articles are fetched and appended to list
    with tqdm(total=max_articles, desc="Fetching Articles") as pbar:
        for article_id in article_ids:
            url = ITEM_URL.format(id=article_id)
            try:
                article = fetch_data(url)
                if article and "title" in article and "url" in article:
                    articles.append(
                        [len(articles) + 1, article["title"], article["url"]]
                    )
                    pbar.update(1)
            except (
                requests.exceptions.RequestException
            ):  # Skip articles with HTTP errors
                pass

            # Stop fetching once 5 article(s) have been appended to the list.
            if len(articles) == max_articles:
                break
    return articles


def display_sections():
    """Displays the available sections for browsing."""
    print("\nWELCOME TO HACKER NEWS!")
    sections = [
        [1, "Top Stories"],
        [2, "New Stories"],
        [3, "Best Stories"],
        [None, None],
        [0, "Exit"],
    ]
    print("\n" + tabulate(sections, headers=["No.", "Sections"], tablefmt="presto"))


def display_articles(section_choice):
    """Fetches and displays articles from the chosen section."""
    article_ids = fetch_article_ids(section_choice)
    articles = fetch_articles(article_ids)

    # Add an empty row and a "Previous Menu" option.
    articles.append([None, None, None])
    articles.append([0, "Previous Menu", None])
    print(
        "\n"
        + tabulate(articles, headers=["No.", "Articles", "URLs"], tablefmt="presto")
    )
    read_article(section_choice, articles)


def read_article(section_choice, articles):
    """Allows user to select and read an article."""
    article_choice = validate_input(
        # Total length of articles is 7 including empty line and "Previous Menu" option
        "\nPlease choose an article to read (1-5) or 0 to return to the previous menu: ",
        range(0, len(articles) - 1),
    )
    if article_choice == 0:
        main()
        return
    title = articles[article_choice - 1][1]
    summary = fill(summarize(articles[article_choice - 1][2]), width=80)
    url = articles[article_choice - 1][2]
    print(
        f"\nTitle: {title}\n\nArticle Summary:\n{summary} \n\nCtrl + Click to read full article:\n{url}\n"
    )
    read_another_article(section_choice, articles)


def read_another_article(section_choice, articles):
    """Prompt user to read another article or exit."""
    choose_new_article = validate_input(
        "Enter 1 to choose another article to read or 0 to exit: ", range(0, 2)
    )
    if choose_new_article == 0:
        sys.exit("END")
    print(
        "\n"
        + tabulate(articles, headers=["No.", "Articles", "URLs"], tablefmt="presto")
    )
    read_article(section_choice, articles)


def main():
    """Main function to start the Hacker News CLI."""
    display_sections()
    section_choice = validate_input(
        "\nPlease choose a section to browse (1-3) or 0 to exit: ", range(0, 4)
    )
    if section_choice == 0:
        sys.exit("END")
    display_articles(section_choice)
    read_article()


if __name__ == "__main__":
    main()
