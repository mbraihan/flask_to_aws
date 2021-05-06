import boto3

s3_ob = boto3.resource('s3', aws_access_key_id='AKIA4AF7WLIDLM2QHOUL', aws_secret_access_key='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')

for each_b in s3_ob.buckets.all():
    print(each_b.name)