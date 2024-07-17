#pylint: disable=  unused-import,trailing-whitespace,line-too-long
import base64
default_image_path = r"C:\Users\Rishin Prageet\OneDrive\Desktop\intern\sports_aggregator\images\default-image.jpg"
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
    return f"data:image/jpeg;base64,{encoded_string}"