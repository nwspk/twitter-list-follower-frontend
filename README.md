# About
This is the frontend to the [Newspeak House project twitter-list-follower](https://github.com/nwspk/twitter-list-follower).
The backend uses some very cool AWS technology to enable the queueing and backing off required
by the Twitter API. However, we need a little frontend to enable users to see things.

It needs a twitter application to work. You can create one in the [Twitter developer portal](https://developer.twitter.com/en/portal/dashboard)

This repo has a ProcessInterface class. I've implemented it solely for AWS, but you could extend it to use Redis or
[Azure's queuing software](https://azure.microsoft.com/en-gb/services/storage/queues/).

The frontend is in Flask and is as basic as it gets. Pull requests are welcome, particularly if you like things to look nice.

You can deploy this directly into Digital Ocean:

[![Deploy to DO](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/nwspk/twitter-list-follower-frontend/tree/main)

In order to set this up, you'll need to set some environment variables:

- TWITTER_CALLBACK_URL: when we send users to Twitter to authorise the application, Twitter needs to know where to
 redirect them afterwards. This should be "domain.com/redirect" - for example, if you're hositng this at
"www.elegant-elephant.com", this variable should be "www.elegant-elephant.com/redirect". You'll also need to register
 this url with Twitter
- QUEUE_TOOL: if you want to use AWS, set this variable to 'AWS'. Otherwise, you'll need to write a new interface in the
  [process interface](./process_interface.py) file, including updating the enumerator and ProcessInterfaceFactory

if you are using AWS, you'll also need to set:

- AWS_ACCESS_KEY
- AWS_SECRET_ACCESS_KEY

these can be collected from your AWS console
