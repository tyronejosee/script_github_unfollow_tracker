import requests

import core.config as cfg


def get_followers(auth: dict) -> tuple:
    """
    Retrieve the list of followers for a GitHub user.

    Args:
        auth (dict): A dictionary containing username and access token.

    Returns:
        tuple: A tuple containing a list of followers.
    """
    followers: list[dict] = []
    page: int = 1
    while True:
        url = f"https://api.github.com/users/{auth['username']}/followers?page={page}&per_page=100"
        headers = {
            "Authorization": f"token {auth['token']}",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching followers: {e}")
            return [], 0

        data = response.json()
        if not data:
            break
        followers.extend(data)
        page += 1
    return followers, len(followers)


def get_following(auth: dict) -> tuple:
    """
    Retrieve the list of users that a GitHub user is following.

    Args:
        auth (dict): A dictionary containing username and access token.

    Returns:
        tuple: A tuple containing a list of users that the user is following.
    """
    following: list[dict] = []
    page: int = 1
    while True:
        url = f"https://api.github.com/users/{auth['username']}/following?page={page}&per_page=100"
        headers = {
            "Authorization": f"token {auth['token']}",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching following: {e}")
            return [], 0

        data = response.json()
        if not data:
            break
        following.extend(data)
        page += 1
    return following, len(following)


def sync_follow_relationships(
    auth: dict,
    followers: list,
    following: list,
) -> None:
    """
    Synchronize the follow relationships between a user and their followers and following.

    Args:
        auth (dict): A dictionary containing username and access token.
        followers (list): A list of followers.
        following (list): A list of following.
    
    Returns:
        None
    """
    followers_set = set(user["login"] for user in followers)
    following_set = set(user["login"] for user in following)

    # Unfollow users who don't follow you back
    to_unfollow = following_set - followers_set
    for user in to_unfollow:
        url = f"https://api.github.com/user/following/{user}"
        response = requests.delete(
            url,
            headers={"Authorization": f"token {auth['token']}"},
        )
        if response.status_code == 204:
            print(f"[UNFOLLOW] {user}")
        else:
            print(f"[ERROR UNFOLLOW] {user}: {response.status_code}")

    # Follow-back users who follow you but you don't follow back
    to_follow_back = followers_set - following_set
    for user in to_follow_back:
        url = f"https://api.github.com/user/following/{user}"
        response = requests.put(
            url,
            headers={"Authorization": f"token {auth['token']}"},
        )
        if response.status_code == 204:
            print(f"[FOLLOW BACK] {user}")
        else:
            print(f"[ERROR FOLLOW BACK] {user}: {response.status_code}")


def main() -> None:
    """
    Main function that interacts with the user to display
    information about their followers and following on GitHub.
    """
    auth = {
        "username": cfg.APP_USERNAME,
        "token": cfg.APP_TOKEN,
    }

    followers, total_followers = get_followers(auth)
    following, total_following = get_following(auth)

    followers_set = set(user["login"] for user in followers)
    following_set = set(user["login"] for user in following)
    unfollowers = following_set - followers_set

    print(f"\nTotal followers: {total_followers}")
    print(f"Total following: {total_following}")

    if unfollowers:
        print("\nPeople you follow who don't follow you back:")
        for user in sorted(unfollowers):
            print(f"- {user}")
    else:
        print("\nEveryone you follow follows you back.")

    sync_follow_relationships(auth, followers, following)


if __name__ == "__main__":
    main()
