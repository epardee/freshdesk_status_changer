## freshdesk_status_changer
Utility for changing ticket statuses in freshdesk. Useful for scheduled routine operations.
This script will take in a freshdesk view, search for any tickets with a start status, then change them to the final status.
Can be run to revert the changes made on these tickets.


###Use case:
1) Change all 'pending' tickets to 'on hold' on Friday at 9:00pm

2) Change all these tickets back to 'pending' on Monday at 6:00am

3) No more angry customers emailing in Monday asking why the ticket was closed


###How to run:
**Required Arguments:**

-a : Freshdesk API key. Ex: 1a2b3c4d5e6f

-c : Company freshdesk domain. Ex: https://contoso.freshdesk.com

-n : View number. This is a view you need to create that holds the tickets to be changing. Ex : https://contoso.freshdesk.com/helpdesk/tickets/view/123456789

-f : Ticket status to change from. Ex: 3 for 'pending'

-t : Ticket status to change to. Ex: 7 for 'on hold'


**Optional Arguments:**

-r : Revert flag. Add this if you are reverting changes made from the previous run. This causes the script to only change tickets that were modified in the last run.

-v : Enable verbose logging.

-vv : Enable very verbose logging. Beware of log file size!

## This script requires "requests": http://docs.python-requests.org/, 
## "logging": https://pypi.io/project/logging and "argparse": https://pypi.io/project/argparse
## To install: pip install requests logging argparse

###Example usage:

**Friday evening** - change all 'Pending' tickets in view to 'On Hold' so they do not close over the weekend:

*python preserve_pending_tickets.py -a 1a2b3c4d5e6f -c contoso -n 123456789 -f 3 -t 7*


Change all 'Open' tickets in view to 'Closed' because they didn't close on Zendesk import:

*python preserve_pending_tickets.py -a 1a2b3c4d5e6f -c contoso -n 123456789 -f 2 -t 5*


**Monday Morning** - change those tickets we altered back to 'Pending' to reset the autoclose timer

*python preserve_pending_tickets.py -a 1a2b3c4d5e6f -c contoso -n 123456789 -f 7 -t 3 -r*
