# About
This is the frontend to the [Newspeak House project twitter-list-follower](https://github.com/nwspk/twitter-list-follower). 
The backend uses some very cool AWS technology to enable the queueing and backing off required 
by the Twitter API. However, we need a little frontend to enable users to see things. 

This repo has a ProcessInterface class. I've implemented it solely for AWS, but you could extend it to use Redis or 
[Azure's queuing software](https://azure.microsoft.com/en-gb/services/storage/queues/). 

The frontend is in Flask and is as basic as it gets. Pull requests are welcome, particularly if you like things to look nice.