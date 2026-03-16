import json
import boto3

def lambda_handler(event, context):
    # Initialize the IoT client
    iot_client = boto3.client('iot-data', region_name='us-east-2') 
    THING_NAME = 'Sukhraj_920857647_CC3200'
    
    try:
        # 1. Parse the JSON sent by your HTML file
        body = json.loads(event.get('body', '{}'))
        lat = body.get('lat')
        lon = body.get('lon')
        
        if lat is None or lon is None:
            return {
                'statusCode': 400, 
                'body': json.dumps('Missing lat or lon in request body')
            }
        
        # 2. Format the payload for your CC3200 Shadow
        shadow_payload = {
            "state": {
                "desired": {
                    "longitude": lon,
                    "latitude": lat
                }
            }
        }
        
        # 3. Push to AWS IoT Core
        iot_client.update_thing_shadow(
            thingName=THING_NAME,
            payload=json.dumps(shadow_payload)
        )
        
        # 4. Return success
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Success!', 'lat': lat, 'lon': lon})
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Server Error: {str(e)}")
        }