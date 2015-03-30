#!/usr/bin/env python

from hashlib import sha1
import hmac
import base64
import time
import urllib
from flask import current_app

request_format = (
    '%s\n'  # PUT
    '\n'
    '%s\n'  # image/jpeg
    '%d\n'  # 1234567890
    '%s\n'  # x-amz-acl:public-read
    '/%s/%s'  # /bucketname/file
)


def aws_signature(tosign, secret_key):
    """Generate an AWS signature.

    http://docs.aws.amazon.com/AmazonS3/latest/dev/RESTAuthentication.html
    """
    digest = hmac.new(secret_key, tosign.encode('utf-8'), sha1).digest()
    signature = base64.encodestring(digest).strip()
    return signature


def sign_s3(path, mimetype, method, expiry):
    access_key = current_app.config.get('AWS_ACCESS_KEY')
    secret_key = current_app.config.get('AWS_SECRET_KEY')
    bucket_name = current_app.config.get('AWS_S3_BUCKET')

    path = urllib.quote(path)

    expires = long(time.time() + expiry)
    amz_headers = [
        ('x-amz-acl', 'public-read',),
    ]

    amz_header_str = '\n'.join(['%s:%s' % h for h in amz_headers])

    request = request_format % (method, mimetype, expires, amz_header_str,
                                bucket_name, path)

    signature = aws_signature(request, secret_key)

    url_base = 'https://%s.s3.amazonaws.com/%s' % (bucket_name, path)

    params = {
        'AWSAccessKeyId': access_key,
        'Expires': expires,
        'Signature': signature,
    }
    params.update(dict(amz_headers))

    return {
        'signed_request': '%s?%s' % (url_base, urllib.urlencode(params)),
        'url': url_base,
    }
