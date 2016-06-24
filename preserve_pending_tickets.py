import json
import requests
import logging
import os
import argparse
import time

"""
3: pending
4: resolved
7: on hold
"""


class Freshdesk_Request_Maker():

    def __init__(self, freshdesk_info, sleep_time=1):
        logger.debug("Freshdesk_Request_Maker initialized with freshdesk info {} and sleep time {}".format(str(freshdesk_info), str(sleep_time)))
        self.freshdesk_info = freshdesk_info
        self.sleep_time = sleep_time
        self.ticket_list = []

    def get_tickets_in_view(self):
        """ Creates self.ticket_list with all tickets seen in a given view """
        logger.info("Entered get_tickets_in_view")
        try:
            page_num = 1
            while True:
                url_to_request = self.freshdesk_info['url'] + self.freshdesk_info['view_url'].format(self.freshdesk_info['view_number']) + str(page_num)
                logger.debug("Requesting {}".format(url_to_request))
                r = requests.get(url_to_request, auth=(self.freshdesk_info['api_key'], "X"))
                returned_json = json.loads(r.text)
                logger.debug("We received json back: {}".format(returned_json))
                # if we received no tickets, we break and stop requesting more
                if not returned_json:
                    logger.debug("We broke out because no json was returned")
                    break
                page_num += 1
                self.ticket_list.extend(returned_json)
                time.sleep(self.sleep_time)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logger.warning("Error in get_tickets_in_view: {}".format(str(e)))
            raise

    def change_ticket_statuses(self, original_status, new_status, revert):
        """ Finds all tickets with original_status and changes to new_status
            If the revert argument is true, it will only change tickets found in the changed.txt file in the script directory. This is so we don't clobber views and only undo what we last did """

        def make_request(ticket_number):
            url_to_request = ticket_update_url + str(ticket_number)
            logger.debug("Sending request: {} with data: {}".format(url_to_request, send_data))
            r = requests.put(url_to_request, auth=(self.freshdesk_info['api_key'], "X"), data=send_data, headers=headers)
            logger.info('Updated ticket {} with request {}'.format(ticket_number, url_to_request))

        logger.info("Entered change_ticket_statuses")
        headers = {'Content-Type': 'application/json'}
        ticket_update_url = self.freshdesk_info['url'] + self.freshdesk_info['ticket_view']
        send_data = json.dumps({'status': int(new_status)})
        logger.debug("We have ticket list to check: {}".format(self.ticket_list))

        if(revert):
            with open(path_to_changed_file, 'r') as changed_file:
                for ticket_number in changed_file:
                    try:
                        make_request(ticket_number)
                    except requests.exceptions.RequestException as e:
                        logger.warning("Requests exception when changing ticket status: {}".format(str(e)))
                        pass

                    except Exception as e:
                        logger.error("Unhandled exception when reverting ticket status! {}".format(str(e)))
                        print("Unhandled exception when changing ticket status! {}".format(str(e)))
                        pass
        else:
            with open(path_to_changed_file, 'w') as changed_file:
                for ticket in self.ticket_list:
                    try:
                        make_request(ticket['display_id'])
                    except requests.exceptions.RequestException as e:
                        logger.warning("Requests exception when changing ticket status: {}".format(str(e)))
                        pass

                    except Exception as e:
                        logger.error("Unhandled exception when changing ticket status! {}".format(str(e)))
                        print("Unhandled exception when changing ticket status! {}".format(str(e)))
                        pass

                    else:
                        # write ticket number to changed file
                        changed_file.write(str(ticket['display_id']) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="\nChanges tickets from one status to another in a specific Freshdesk view.", usage="python preserve_pending_tickets.py -a freshdesk_api_key -v view_number\nRun with -h flag for help.", formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '-a', '--api_key', help='API key for user profile in Freshdesk. This is a required argument.', required=True)

    parser.add_argument(
        '-c', '--company', help='Company subdomain in Freshdesk. For contoso.freshdesk.com run as -c contoso. This is a required argument.', required=True)

    parser.add_argument(
        '-n', '--view_number', help='View to search for tickets in. If the view URL is "https://contoso.freshdesk.com/helpdesk/tickets/view/123456789", use -n 123456789 . This is a required argument.', required=True)

    parser.add_argument('-f', '--from', help='Ticket status to change from. 3 is pending and 7 is on hold', required=True)

    parser.add_argument('-t', '--to', help='Ticket status to change to. 3 is pending and 7 is on hold', required=True)

    parser.add_argument('-r', '--revert', help='Means we are reverting changes made in a prior run. This means we only change tickets from-->to if they were changed last time.', required=False, action='store_true')

    parser.add_argument('-s', '--sleep_time', help='Sleep time (in seconds) between successive API requests. This is an optional argument with a default value of 1', required=False, default=1)

    parser.add_argument('-v', '--verbose', help='Enable verbose logging', required=False, action='store_true')

    parser.add_argument('-vv', '--very_verbose', help='Enable very verbose logging. Beware of log file size!!', required=False, action='store_true')

    # Set log file to save in the same directory as the script file
    base_folder = os.path.dirname(os.path.realpath(__file__))
    path_to_changed_file = base_folder + '\\' + 'changed.txt'
    args = vars(parser.parse_args())

    # Set appropriate verbosity of logging
    if args['very_verbose']:
        log_level = logging.DEBUG
        request_log_level = logging.DEBUG
    elif args['verbose']:
        log_level = logging.INFO
        request_log_level = logging.WARNING
    else:
        log_level = logging.WARNING
        request_log_level = logging.WARNING

    # initialize the logger
    logging.basicConfig(filename=base_folder + '\\' + 'log.txt', level=log_level,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logging.getLogger("requests").setLevel(request_log_level)
    logger.info("-----New Run-----")

    # construct variable to pass from the arguments received
    freshdesk_info = {'url': "https://" + args['company'] + ".freshdesk.com",
                      'view_number': args['view_number'],
                      'view_url': "/helpdesk/tickets/view/{}?format=json&page=",
                      'api_key': args['api_key'],
                      'ticket_view': '/api/v2/tickets/'}

    request_maker = Freshdesk_Request_Maker(freshdesk_info, sleep_time=args['sleep_time'])

    # get the relevant tickets and change their statuses
    request_maker.get_tickets_in_view()
    request_maker.change_ticket_statuses(args['from'], args['to'], args['revert'])
