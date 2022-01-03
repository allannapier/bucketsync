# Bucketsync

This tool is designed to sync files between a bucket in Google Cloud and a bucket in Amazon S3.

This is a two way sync, so any files not found in either bucket will be copied to the other bucket.

At the moment I have not added a way to detect file changes but will do so in a future version but I didn't need it at this stage for this tool.

To run it just update the settings file with your bucket name and GC secrets file location. You need to have your AWS credentials installed on your 
machine as it will use the os settings.

To run it once downloaded and settings updated just do something like 'python3 -m cloudsync" when you have the terminal in the correct directory.
