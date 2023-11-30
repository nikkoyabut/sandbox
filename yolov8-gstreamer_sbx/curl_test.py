import requests
import json
import base64

# URL of your PyTriton server endpoint
url = '202.92.159.242:8003/v2/models/Yolov8x/infer'

# Image file you want to send for object detection
image_file_path = 'dog_bike_car.jpg'

# Read the image file and encode it in base64
with open(image_file_path, 'rb') as file:
    image_data = base64.b64encode(file.read()).decode('utf-8')

# Prepare the payload with the base64 encoded image
payload = {
    "inputs": [
        {
            "name": "input",
            "shape": [1, len(image_data)],  # adjust the shape based on your model requirements
            "datatype": "BYTES",
            "data": [image_data]
        }
    ]
}

# Convert payload to JSON
json_payload = json.dumps(payload)

# Send POST request to the PyTriton server
headers = {'content-type': 'application/json'}
response = requests.post(url, data=json_payload, headers=headers)

# Get the inference results
if response.status_code == 200:
    inference_results = response.json()
    # Process inference results as needed
    print(inference_results)
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
