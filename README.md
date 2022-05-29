# Tanki Fund Visualizer

Small Flask app to visualize the Tanki Fund and provide analytics on the fund's status.

## Features
- CLI for dev testing.
- Analytics: Currently shows the following:
    - Current values in the fund; reached and new checkpoints.
    - Basic Linear regression and prediction model.
    - Daily TK increase and percentage change from the day before.
- Site status page: fetches backups from local saved file if site is not responding. `cron.sh` creates local backups every 15 minutes; `update.sh` automatically re-deploys to GitHub every hour.

## In Progress/Coming Soon
- UI update: Neaten everything out and choose a nice font. Right now, everything looks fine, but with new features come new challenges to make the site more compact.
- Even More Analytics: Better predictions, more regression models, select menu to view each method.
- Code Cleanup: clearing out unused functions/making the codebase easier to read and understand.

## CLI Usage
Test most functions using the CLI. (Make sure to cd into `/src` as well!)

### Functions
Append `python(3) fund.py` to all functions.
- `cron`: gets an entry and serializes it.
- `check`: gets the last 10 entries. Used to see if entries are properly serializing.
- `last`: get the time of the last entry.
- Anything else not mentioned will run into a surprise.

Find the application deployed on Heroku [here](https://fund-vis.herokuapp.com/).
