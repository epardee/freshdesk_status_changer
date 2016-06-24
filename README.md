# freshdesk_status_changer
Utility for changing certain ticket statuses in frreshdesk. Used for timed weekly operations.
This script will take in a freshdesk view, search for any tickets with a start status, then change them to the final status.
Can be run to revert the changes made on these tickets.

#Use case:
1) Change all 'pending' tickets to 'on hold' on Friday at 9:00pm
2) Change all these tickets back to 'pending' on Monday at 6:00am
3) No more angry customers emailing in Monday asking why the ticket was closed

#How to run:
Required Arguments:
-a : Freshdesk API key. Ex: 1a2b3c4d5e6f
-c : Company freshdesk domain. Ex: https://contoso.freshdesk.com
-n : View number. Ex : https://contoso.freshdesk.com/helpdesk/tickets/view/123456789
-f : Ticket status to change from. Ex: 3 for 'pending'
-t : Ticket status to change to. Ex: 7 for 'on hold'
-r : Revert flag. Add this if you are reverting changes made from the previous run. This causes the script to only change tickets that were modified in the last run.
-v : Enable verbose logging.
-vv : Enable very verbose logging. Beware of log file size!

#Example usage:
Friday evening - change all 'Pending' tickets in view to 'On Hold':
python preserve_pending_tickets.py -a 1a2b3c4d5e6f -c contoso -v 123456789 -f 3 -t 7

Monday Morning - change those tickets we altered back to 'Pending' to reset the autoclose timer
python preserve_pending_tickets.py -a 1a2b3c4d5e6f -c contoso -v 123456789 -f 7 -t 3 -r
