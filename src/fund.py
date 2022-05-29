# CLI
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import scraper as scraper
from scraper import FundEntry

def cmd_input(args):
    command = args[0]
    if command == "cron":
        scraper.get_entry()
    elif command == "check":
        print(scraper.entries()[-10:])
    elif command == "last":
        print(scraper.entries()[-1].time)
    elif command == "zero":
        scraper.addzero()
    elif command == "del":
        scraper.delallerrors()
    elif command == "plot":
        scraper.showplot()
    elif command == "reg":
        scraper.regression(x=scraper.x_time(scraper.get_data()[0]), y=scraper.get_data()[1], log="x")
    elif command == "nextpt":
        scraper.next_checkpoint()
    elif command == "fin":
        scraper.end_fund()
    elif command == "ddelta":
        scraper.delta_tbl()
    else:
        print("Imposter Alert")
    # match command:
    #     case "--help":
    #         print("You're not a cron job; don't ask for help.")
    #     case "cron":
    #         scraper.get_entry()
    #     case "reset":
    #         scraper.reset()
    #     case _:
    #         print(f"No match found for given argument. {exception_text}")
    #         return

exception_text = "Try 'python fund.py --help' to search for a given command."

args = sys.argv[1:]
if len(args) == 0:
    print(f"No arguments given. {exception_text}")
else:
    cmd_input(args)