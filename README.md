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
4. Include **search terms** in `search-terms.dat`.
5. Include **valid locales** for your courses in `valid-course-locales.dat`. Use the format `xx_XX` as in the [Posix Locales](https://docs.oracle.com/cd/E23824_01/html/E26033/glset.html). If this file does not exist all locales are admitted.
6. Install **requirements**: `pip install -r requirements.txt`
7. Launch **main script**: `run.sh`

🎉 &nbsp; If everthing goes fine you'll get desired discount courses on your Slack channel.
