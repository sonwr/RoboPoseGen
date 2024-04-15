import json
import os
from PIL import Image, ImageDraw, ImageFont
from glob import glob

def create_output_directory():
    # Check if the output directory exists, if not, create it
    output_dir = 'out_annotation'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def annotate_image(image_path, json_path, output_dir):
    # Define the output image path
    base_name = os.path.basename(image_path)
    output_image_path = os.path.join(output_dir, f'{os.path.splitext(base_name)[0]}_out.jpg')

    # Specify the joints to be annotated
    joints_to_annotate = [
        "nose", "pelvis", "upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r",
        "hand_l", "hand_r", "neck_01", "thigh_l", "thigh_r", "calf_l",
        "calf_r", "foot_l", "foot_r", "head"
    ]

    # Load the JSON data
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    try:
        # Try to use a default font
        font = ImageFont.truetype("arial.ttf", size=12)
    except IOError:
        # Fallback to a simple font bundled with PIL
        font = ImageFont.load_default()

    # Iterate through each joint and annotate it on the image if it's in the list
    for joint in data['jointStruct']:
        if joint['jointName'] in joints_to_annotate:
            x, y = joint['x'], joint['y']
            joint_name = joint['jointName']
            # Draw a small circle around the joint
            draw.ellipse((x-5, y-5, x+5, y+5), fill=(255, 0, 0), outline=None)
            # Annotate the joint name next to the circle
            draw.text((x+10, y-10), joint_name, fill=(255, 255, 255), font=font)

    # Save the annotated image
    image.save(output_image_path)

output_dir = create_output_directory()
input_dir = 'saved'

# Find all jpg files in the input directory
image_files = glob(os.path.join(input_dir, '*.jpg'))

# Loop through each image file and find its corresponding json file
for image_file in image_files:
    json_file = os.path.splitext(image_file)[0] + '.json'
    if os.path.exists(json_file):
        try:
            annotate_image(image_file, json_file, output_dir)
            print(f'{os.path.basename(image_file)} annotated successfully.')
        except Exception as e:
            print(f'Failed to annotate {os.path.basename(image_file)} due to error: {e}')
    else:
        print(f'Corresponding JSON file for {os.path.basename(image_file)} not found.')
