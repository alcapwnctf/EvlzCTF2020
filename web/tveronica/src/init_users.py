#!/usr/bin/env python3
import os
from search import KeyClient
from main import COOKIE_PREFIX, USER_PREFIX, new_user, User, serialize_user, new_sessid, USER_TYPE_USER, USER_TYPE_ADMIN

ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'asdasfsagsasalsanlflaskd')

client = KeyClient()

with open('/opt/scripts/usernames.txt') as f:
    usernames = f.readlines()

if __name__ == "__main__":
    def create_user(username, password, sess_id, type):    
        user = new_user(
            username,
            password,
            type
        )
        
        client.write_prefix(
            USER_PREFIX,
            username,
            serialize_user(user)
        )

        client.write_prefix(
            COOKIE_PREFIX,
            username,
            sess_id
        )

    create_user('admin', ADMIN_PASSWORD, new_sessid(), USER_TYPE_ADMIN)
    print('[+] Created admin.')
    for username in usernames:
        create_user(username.strip(), new_sessid(), new_sessid(), USER_TYPE_USER)
    print(f'[+] Created {len(usernames)} users.')
