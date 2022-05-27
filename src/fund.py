# CLI
import sys
import scraper as scraper
from scraper import FundEntry

def cmd_input(args):
    command = args[0]
    match command:
        case "--help":
            print("You're not a cron job; don't ask for help.")
        case "cron":
            scraper.get_entry()
            scraper.visualize()
        case "reset":
            scraper.reset()
        case _:
            print(f"No match found for given argument. {exception_text}")
            return

exception_text = "Try 'python fund.py --help' to search for a given command."

args = sys.argv[1:]
if len(args) == 0:
    print(f"No arguments given. {exception_text}")
else:
    cmd_input(args)