# example of IMAP protocol
# from TutorialsPoint.com and others
# Google requires security for unsafe apps to be turned off
# or it requires oauth authentication


import imaplib
import email
import pprint

imap_host = 'imap.gmail.com'
imap_user = 'jamiew056@gmail.com'
imap_pass = ''

# connect to host using SSL
with imaplib.IMAP4_SSL(imap_host) as imap:
    imap.login(imap_user, imap_pass)
    imap.select('INBOX')
    status, response = imap.search('utf-8', 'UNSEEN')
    print(response[0].decode("utf-8"))
    if False:
        unreadcount = int(response[0].decode("utf-8").split()[2].strip(').,]'))
        print(unreadcount)
        tmp, data = imap.search(None, '(UNSEEN)')
        for num in data[0].split():
            #tmp, data = imap.fetch(num, '(RFC822)')
            tmp, data = imap.fetch(num, '(UID BODY[TEXT])')
            print('Message: {0}\n'.format(num))
            msg = email.message_from_string(data[0][1].decode("utf-8"))
            print(msg)
            break
