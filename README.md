# Script GitHub Unfollow Tracker

A script that allows users to manage their follows on GitHub by identifying who has unfollowed them. Using the GitHub API and a personal access token (`GITHUB_TOKEN`), the script provides an easy way to track changes in followers through a command-line interface.

## 🔐 Generate `GITHUB_TOKEN`

1. Log in to your [GitHub](https://github.com/) account.
2. In the top right corner, click on your **profile picture** and select `Settings`.
3. In the left sidebar, scroll down and select `Developer settings`.
4. On the next page, in the left sidebar, select `Personal access tokens`.
5. If you're using the new token flow, you might also find `Tokens (classic)` since GitHub offers two types of tokens (it is recommended to use the new `fine-grained tokens` method).
6. In the top right corner, click `Generate new token`.
7. If you choose the classic option, select `Generate new token (classic)`.
8. **Choose a name:** Give your token a descriptive name to identify it later, for example, `"My GitHub Token for Project X"`.
9. **Choose duration (expiration):** You can select how long you want your token to be valid (30 days, 60 days, or indefinitely). It is recommended to set an expiration date for better security.
10. **Choose permissions (Scopes):** Here you can select the permissions you want to grant to the token. If the token is for cloning or pushing repositories, select `repo`, which allows read and write access to repositories. If you need access to more resources like packages or additional settings, check the necessary permissions.
11. After selecting the permissions and duration, click `Generate token`.
12. Copy the token immediately after generating it. This is the only time you'll be able to see it. If you lose it, you will have to generate a new one.

## ⚙️ Installation

1. Clone the repository

```bash
git clone git@github.com:tyronejosee/script_github_unfollow_tracker.git
```

2. Create a virtual environment for the dependencies

```bash
python -m venv env
```

2. Activate the virtual environment

```bash
# Windows
env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

3. Install all the necessary dependencies

```bash
pip install -r requirements.txt
```

4. Rename the `.env.example` file to `.env` and add your `GITHUB_TOKEN`

```bash
cp .env.example .env
```

5. Done! Now run the script

```bash
python main.py
```

Enjoy! 🎉
