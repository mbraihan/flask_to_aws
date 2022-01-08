import boto3

s3_ob = boto3.resource('s3', aws_access_key_id='', aws_secret_access_key='')

for each_b in s3_ob.buckets.all():
    print(each_b.name)
