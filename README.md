# Trillium Pet Products API

## Requirements:

* [Python 2.7](https://www.python.org/download/releases/2.7/)
* [Virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html#installation)

## Running Style Checkers
The following python checkers are available:

* `pep8`: [PEP8](http://legacy.python.org/dev/peps/pep-0008/) style checker
* `pep257` [PEP257](http://legacy.python.org/dev/peps/pep-0257/) docstring checker
* `flake8`: Combines PEP8 with [PyFlakes](https://pypi.python.org/pypi/pyflakes), a static analysis tool
* `pylint`: Python code analyzer

To run all checkers required to pass a build:

    $ make check

To run a specific check:

    $ make <checker-name>

## Development
You can then run a development server as follows:

    $ make serve

The `serve` command starts _only_ the Flask dev server. The Celery worker is
_not_ started with this command. The Celery worker can be started with:

    $ make celery

To simulate the production environment, both the Flask server and the Celery
worker can be started simultaneously using `honcho`:

    $ make run

By default, port 5000 is used unless the `$PORT` environment variable is set.
Also note that `foreman` will not show detailed stack traces as it runs using
the production environment config.

The virtualenv will be created automatically with the required dependencies. If
the requirements file (`requirements/dev.txt`) changes, running any command will
automatically cause the dependencies in the virtualenv to be updated.

Compiled python files and pytest cache files can be cleaned with:

    $ make clean

If you need to rebuild the virtualenv from scratch:

    $ make clean-all

## Dokku Setup
Initialize a git remote for the application deploy target:

    $ git remote add prod dokku@host:tpp-api

Add a redis container for the app

    $ ssh dokku@host redis:create tpp-api

Set the `FLASK_ENV` variable:

    $ ssh dokku@host config:set tpp-api FLASK_ENV=production

Deploy!

    $ git push prod

## AWS Setup
The `/sign_s3` API endpoint generates signed urls for uploading files to the
app's S3 bucket. Some configuration in the AWS Console is required to get this
working.

### S3 Bucket Setup
Open the [S3 Console][s3-console] and click "Create Bucket". Choose a name for
the new bucket that matches the [rules listed here][bucket-rules].

Next, configure the Dokku app to use the bucket you created:

    $ ssh dokku@host config:set tpp-api AWS_S3_BUCKET=buckename-here

Add a new CORS Configuration under bucket Properties -> Permissions:

    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
        <CORSRule>
            <AllowedOrigin>example.com</AllowedOrigin>
            <AllowedMethod>GET</AllowedMethod>
            <AllowedMethod>PUT</AllowedMethod>
            <AllowedHeader>*</AllowedHeader>
        </CORSRule>
    </CORSConfiguration>

### AWS User Setup
In the AWS IAM console, open the [Groups][iam-groups] page, pick a group name,
and click "Next Step".

Select "Custom Policy" and use the following ACL:

    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "s3:PutObject",
            "s3:PutObjectAcl"
          ],
          "Resource": [
            "arn:aws:s3:::bucketname-here/*"
          ]
        }
      ]
    }

Next, open the [Users][iam-users] page and create a new user. Click on "Show
User Security Credentials" and copy the access key and secret key into the
Dokku config variables:

    $ ssh dokku@host config:set tpp-api AWS_ACCESS_KEY=access-key-here
    $ ssh dokku@host config:set tpp-api AWS_SECRET_KEY=secret-key-here

On the Users page, select the new user and select "Add User to Groups" from the
"User Actions" menu. Select the group created previously.

### Other Setup
Set the timout of the signed URLs using the `AWS_URL_EXPIRY` environment
variable on dokku:

    $ ssh dokku@host config:set tpp-api AWS_URL_EXPIRY=30

[s3-console]: https://console.aws.amazon.com/s3/home?region=us-west-2
[bucket-rules]: https://devcenter.heroku.com/articles/s3#naming-buckets
[iam-groups]: https://console.aws.amazon.com/iam/home?region=us-west-2#groups
[iam-users]: https://console.aws.amazon.com/iam/home?region=us-west-2#users
