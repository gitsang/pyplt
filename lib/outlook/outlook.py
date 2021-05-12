#!/usr/bin/python

import win32com.client
import os

path = 'E:\\outlook\\'
outlook = win32com.client.Dispatch('Outlook.Application')
mapi = outlook.GetNamespace('MAPI')
inbox = mapi.GetDefaultFolder(5)
msgs = inbox.Items

for msg in msgs:
    subject = msg.subject
    date = msg.senton.date()
    attachments = msg.Attachments
    print(subject, date)

# for attachement in attachements:
#	attachement.SaveASFile(os.path.join(save_path, attachement.FileName))
