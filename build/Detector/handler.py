import boto3
from botocore.vendored import requests

rek = boto3.client('rekognition', region_name='eu-west-1')

def lambda_handler(event, context):
    print(event)
    
    url = event['url']
    bytes = requests.get(url).content
    image = {'Bytes': bytes }
    
    results = []
    try:
        
      response = rek.detect_labels( Image = image )

      for label in response['Labels']:
        if label['Name'] == 'Airplane':
          for instance in label['Instances']:

            results.append( { 
                'label' : label['Name'],
                'score' : instance['Confidence'],
                'left'  : instance['BoundingBox']['Left'],
                'top'  : instance['BoundingBox']['Top'],
                'width'  : instance['BoundingBox']['Width'],
                'height'  : instance['BoundingBox']['Height']
            })

    except Exception as e:
      print(e)

    print(results)
    return results
