import os
import time

import requests
from dotenv import load_dotenv
from typing import List, Tuple

load_dotenv()

GITHUB_TOKEN: str = os.environ.get("GITHUB_TOKEN")

if GITHUB_TOKEN is None:
    raise ValueError("GITHUB_TOKEN environment variable is not set.")


def get_followers(
    username: str,
    auth: Tuple[str, str],
) -> Tuple[List[dict], int]:
    """
    Retrieve the list of followers for a GitHub user.

    Args:
        username (str): The GitHub username.
        auth (Tuple[str, str]): A tuple containing username and access token.

    Returns:
        Tuple[List[dict], int]: A tuple containing a list of followers
        (each represented as a dictionary) and the total number of followers.
    """
    followers: List[dict] = []
    page: int = 1
    while True:
        url: str = (
            f"https://api.github.com/users/{username}/followers?page={page}&per_page=100"
        )
        headers: dict[str, str] = {
            "Cache-Control": "no-cache",
            "Authorization": f"token {auth[1]}",
        }

        try:
            response: requests.Response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching followers: {e}")
            return [], 0

        data: List[dict] = response.json()
        if not data:
            break
        followers.extend(data)
        page += 1
    total_followers: int = len(followers)
    return followers, total_followers


def get_following(
    username: str,
    auth: Tuple[str, str],
) -> Tuple[List[dict], int]:
    """
    Retrieve the list of users that a GitHub user is following.

    Args:
        username (str): The GitHub username.
        auth (Tuple[str, str]): A tuple containing username and access token.

    Returns:
        Tuple[List[dict], int]: A tuple containing a list of users that the user is following
        (each represented as a dictionary) and the total number of users they are following.
    """
    following: List[dict] = []
    page: int = 1
    while True:
        url: str = (
            f"https://api.github.com/users/{username}/following?page={page}&per_page=100"
        )
        headers: dict[str, str] = {
            "Cache-Control": "no-cache",
            "Authorization": f"token {auth[1]}",
        }
        try:
            response: requests.Response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching following: {e}")
            return [], 0

        data: List[dict] = response.json()
        if not data:
            break
        following.extend(data)
        page += 1
    total_following: int = len(following)
    return following, total_following


def main() -> None:
    """
    Main function that interacts with the user to display
    information about their followers and following on GitHub.
    """
    username: str = input("Enter your GitHub username: ")
    auth: Tuple[str, str] = (username, GITHUB_TOKEN)

    while True:
        followers, total_followers = get_followers(username, auth)
        following, total_following = get_following(username, auth)

        followers_set: set[str] = set(user["login"] for user in followers)
        following_set: set[str] = set(user["login"] for user in following)

        unfollowers: set[str] = following_set - followers_set

        print(f"\nTotal followers: {total_followers}")
        print(f"Total following: {total_following}")

        if unfollowers:
            print("\nPeople you are following who don't follow you back:")
            for user in unfollowers:
                print(user)
        else:
            print("\nEveryone you are following follows you back.")

        user_choice: str = input("\n[Enter] Refresh, [0] Exit: ")

        if user_choice.lower() == "0":
            break

        time.sleep(10)  # Delay to avoid overwhelming API


if __name__ == "__main__":
    main()
