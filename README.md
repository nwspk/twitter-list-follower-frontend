# About
This is the frontend to the [Newspeak House project twitter-list-follower](https://github.com/nwspk/twitter-list-follower).
The backend uses some very cool AWS technology to enable the queueing and backing off required
by the Twitter API. However, we need a little frontend to enable users to see things.

It needs a twitter application to work. You can create one in the [Twitter developer portal](https://developer.twitter.com/en/portal/dashboard)

This repo has a ProcessInterface class. I've implemented it solely for AWS, but you could extend it to use Redis or
[Azure's queuing software](https://azure.microsoft.com/en-gb/services/storage/queues/).

The frontend is in Flask and is as basic as it gets. Pull requests are welcome, particularly if you like things to look nice.

In order to set this up, you'll need to set some environment variables:

- QUEUE_TOOL: if you want to use AWS, set this variable to 'AWS'. Otherwise, you'll need to write a new interface in the
  [process interface](./process_interface.py) file, including updating the enumerator and ProcessInterfaceFactory

- CONSUMER_KEY: the twitter key for your application
- CONSUMER_SECRET: the secret key for your twitter application
