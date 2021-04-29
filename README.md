# Freedemy

![Freedemy Logo](freedemy-logo.png)

Freedemy is a service written in Python to scrap and deliver **free couponed courses** from [Udemy](https://udemy.com).

## Workflow

1. Check [comidoc](https://twitter.com/comidoc) for new couponed tweets.
2. Extract comidoc url of course tracker from chosen tweet.
3. Retrieve course information at [Udemy](https://udemy.com) from comidoc url.
4. Deliver course link and details to some backend (e.g. [Slack](https://slack.com)).

## Usage

1. Clone repo.
2. Create a virtualenv with **Python3**.
3. Set, at least, the following values in `.env` file:
   - `TWITTER_API_KEY`
   - `TWITTER_SECRET_KEY`
   - `SLACK_API_TOKEN`
   - `SLACK_CHANNEL`
4. Include **search terms** in `data/search-terms.txt`.
5. Install **requirements**: `pip install -r requirements.txt`
6. Launch **main script**: `run.sh`

🎉 &nbsp; If everything goes fine you'll get desired discount courses on your Slack channel.
