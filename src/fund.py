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
        print(scraper.entries()[:20])
    elif command == "last":
        print(scraper.entries()[-1].time)
    elif command == "del":
        scraper.delallerrors()
    elif command == "plot":
        scraper.showplot()
    elif command == "reg":
        scraper.regression(x=scraper.x_time(scraper.get_data(treat=True)[0]), y=scraper.get_data(treat=True)[1], log="x")
    elif command == "nextpt":
        print(scraper.time_to_check(log="x"))
    elif command == "fin":
        print(scraper.end_fund(log="x"))
    elif command == "ddelta":
        scraper.delta_tbl()
    # elif command == "addarch":
    #     scraper.add_entry()
    elif command == "acheck":
        scraper.check_archive()
    elif command == "afix":
        scraper.treat_data(scraper.entries())
    elif command == "csv":
        scraper.to_csv()
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