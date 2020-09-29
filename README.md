# Freedemy

![Freedemy Logo](freedemy-logo.png)

Freedemy is a service written in Python to scrap and deliver **free couponed courses** from [Udemy](https://udemy.com).

## Workflow

1. Check [comidoc](https://twitter.com/comidoc) for new couponed tweets.
2. Extract comidoc url of course tracker from chosen tweet.
3. Retrieve course information from comidoc url.
4. Deliver course link and details to some backend (e.g. Slack).

## Usage

1. Clone repo.
2. Create a virtualenv with **Python3**.
3. Set the appropiate values in `.env` file.
4. Install requirements: `pip install -r requirements.txt`
5. Launch main script: `python main.py`
