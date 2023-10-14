import base64
import json
import time
import binascii
import os
from hashlib import sha1
import urllib.parse
import hmac


def to_ascii(s):
    if isinstance(s, str):
        return s
    elif isinstance(s, bytes):
        return "".join(map(chr, map(ord, s.decode(encoding='UTF-8'))))
    return s


class URL:
    def __init__(self, host, secret, user,embed_url, session_length=3600, looker=None, force_logout_login=True):
        self.looker = looker
        self.host = host
        self.secret = secret
        self.user = user
        self.path = '/login/embed/' + urllib.parse.quote_plus(embed_url)
        self.session_length = json.dumps(session_length)
        self.force_logout_login = json.dumps(force_logout_login)

    def set_time(self):
        self.time = json.dumps(int(time.time()))

    def set_nonce(self):
        self.nonce = json.dumps(to_ascii(binascii.hexlify(os.urandom(16))))

    def sign(self):
        #  Do not change the order of these
        string_to_sign = "\n".join([self.host,
                                    self.path,
                                    self.nonce,
                                    self.time,
                                    self.session_length,
                                    self.user.looker_fields.get('external_user_id'),
                                    self.user.looker_fields.get('permissions'),
                                    self.user.looker_fields.get('models'),
                                    self.user.looker_fields.get('group_ids'),
                                    self.user.looker_fields.get('external_group_id'),
                                    self.user.looker_fields.get('user_attributes'),
                                    self.user.looker_fields.get('access_filters'),
                                ])

        signer = hmac.new(bytearray(self.secret, 'UTF-8'),
                          string_to_sign.encode('UTF-8'), sha1)
        self.signature = base64.b64encode(signer.digest())

    def to_string(self):
        self.set_time()
        self.set_nonce()
        self.sign()

        params = {'nonce':               self.nonce,
                  'time':                self.time,
                  'session_length':      self.session_length,
                  'external_user_id':    self.user.looker_fields.get('external_user_id'),
                  'permissions':         self.user.looker_fields.get('permissions'),
                  'models':              self.user.looker_fields.get('models'),
                  'group_ids':           self.user.looker_fields.get('group_ids'),
                  'external_group_id':   self.user.looker_fields.get('external_group_id'),
                  'user_attributes':     self.user.looker_fields.get('user_attributes'),
                  'access_filters':      self.user.looker_fields.get('access_filters'),
                  'signature':           self.signature,
                  'first_name':          self.user.first_name,
                  'last_name':           self.user.last_name,
                  'force_logout_login':  self.force_logout_login}
      
        query_string = '&'.join(
            ["%s=%s" % (key, urllib.parse.quote_plus(val)) for key, val in params.items()])

        return "%s%s?%s" % (self.host, self.path, query_string)


def create_signed_url(embed_url, user, host, secret):
  
    url = URL(host=host, 
                secret=secret,
                user=user,
                embed_url=embed_url,
            )

    return "https://" + url.to_string()        