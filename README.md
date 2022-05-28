# Tanki Fund Visualizer

Small Flask app to visualize the Tanki Fund and provide analytics on the fund's status.

## Features
- CLI for dev testing.
- Basic Analytics: Currently shows the current funds and changes as well as reached and new checkpoints.
- Site status page: fetches backups if site is not working.

## Coming Soon
- UI update: Will attempt to add React to make the site neater.
- More Analytics: Regressions, Predictions, time to next milestone.
- Code Cleanup: clearing out unused functions/making the codebase easier to read and understand.

## CLI Usage
Test most functions using the CLI. (Make sure to cd into `/src` as well!)

### Functions
Append `python(3) fund.py` to all functions.
- `cron`: gets an entry and serializes it.
- `check`: gets the last 10 entries. Used to see if entries are properly serializing.
- `last`: get the time of the last entry.
- Anything else not mentioned will run into a surprise.

Find the application deployed on Heroku ![here](https://fund-vis.herokuapp.com/).
