import numpy as np

# Stack ARN:
# arn:aws:cloudformation:ap-southeast-1:618733377538:stack/PixcdkStack/4f951e30-d9fd-11ee-ae0c-023903a07bd1
def handler(event, context):
    arr = np.random.randint(0, 10, (3, 3))
    return {"statusCode": 200,
           "body": "Hello world",
           "array": arr.tolist()
}