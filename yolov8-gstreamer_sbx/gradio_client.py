import gradio as gr
import requests
import numpy as np
from PIL import Image

# Define the function to send requests to the PyTriton YOLO server
def predict_yolo(image):
    url = "http://202.92.159.242:8003/"  # Replace with your server's URL
    files = {'image': image}
    response = requests.post(url, files=files)
    
    # Process the response
    data = response.json()
    bboxes = data['bboxes'][0]
    probs = data['probs'][0]
    names = data['names'][0]
    
    # Prepare the output for visualization
    output = []
    for i in range(len(bboxes)):
        bbox = tuple(map(int, bboxes[i]))
        prob = round(float(probs[i]), 2)
        name = names[i].decode('utf-32').rstrip('\x00')
        output.append((bbox, prob, name))
    
    return output

# Create the Gradio interface
inputs = gr.inputs.Image()
outputs = gr.outputs.ObjectDetection(draw_bbox=True)

title = "YOLOv8x Object Detection"
description = "Upload an image to detect objects using YOLOv8x."
examples = [['path_to_image.jpg']]  # Replace with example image paths

gr.Interface(fn=predict_yolo, inputs=inputs, outputs=outputs, title=title, description=description, examples=examples).launch()
