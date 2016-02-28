
from __future__ import print_function
import httplib2
import os
import sys

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    """    
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
      print('Labels:')
      for label in labels:
        print(label['name'])
    """
    print('Retrieving Messages')
    results = service.users().messages().list(userId='me',labelIds='Label_1').execute()#Label_1 is is the LabelID for "Trigger" label in gmail
    messages = results.get('messages', [])

    if not messages:
        sys.exit("NO TRIGGER MESSAGES FOUND")
    else:
      print('Trigger Messages Found!:')
      for message in messages:
        print(message['id'])
        service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds':['Label_1']}).execute()
    
	'''vvv this code works but doesn't print right. needs a little debugging.
    print('Parsing Email...')
    for message in messages:
	results = service.users().messages().get(userId='me',id=message['id']).execute()
    	names = results.get('headers', [])
	if not messages:
	    sys.exit("NO MESSAGE CONTENT FOUND")
    	else:
            print('Message Data Found!:')
            for name in names:
              	print(name['name'])
    '''
    print('De-Label Here')
if __name__ == '__main__':
    main()
