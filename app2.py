import streamlit as st
import openai
from PIL import Image
import io
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image

# Set your OpenAI API key
openai.api_key = 'sk-proj-eUCM3NI5rNjPgBMOtLcUT3BlbkFJxdGDErpnEv5182Oad7Cf'

# Azure Computer Vision credentials
subscription_key = "35e4fd3f14354da0bc4b57347c213332"
endpoint = "https://azurecomputervizual.cognitiveservices.azure.com/"










st.title("Indian Wedding Outfit Generation")
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def get_image_caption(image_stream):
    # Call API
    description_results = computervision_client.describe_image_in_stream(image_stream)
    
    # Get the caption of the image
    if len(description_results.captions) == 0:
        return "No description detected."
    else:
        for caption in description_results.captions:
            return caption.text


uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
function = ['Marriage', 'Reception', 'Haldi', 'Mehndi','Sangeet']


checkbox_state = st.checkbox('Sketch Mode')

# Display different content based on the checkbox state
if checkbox_state:
    sketch_value='generate the image as if it is a fashion designers sketch'
else:
    sketch_value=''



selected_function = st.selectbox('Choose an option:', function)

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    
    st.image(image, caption="Uploaded Image.", width=200)

    # Convert uploaded file to a stream
    uploaded_file.seek(0)  # Reset the stream position to the beginning
    image_stream = io.BytesIO(uploaded_file.read())

    # Get and display image caption
    try:
        caption = get_image_caption(image_stream)
        
        st.write("Caption: ", caption)
    except Exception as e:
        st.error(f"Error: {e}")










def generate_caption(description):
    # Create a prompt for GPT-4
    prompt = (
        f"You are a detailed image captioning assistant. Describe the following image in great detail. "
        f"Include information about the objects, actions, scenery, colors, and anything else of note in the image.\n\n"
        f"Image description: {description}"
    )

    # Call the OpenAI API to generate the caption
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a detailed image captioning assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    # Extract the caption from the response
    caption = response.choices[0].message['content'].strip()

    return caption


st.write("Upload an image to get a detailed caption generated by GPT-4.")

# Upload image file
#uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    #st.image(image, caption='Uploaded Image', use_column_width=True)

    # Manually input the image description
    description = "Caption:" + caption+ "It is not a shirt, coat or Suit as said in the caption it is an indian wedding outfit a kurta with the colours and details mentioned in the caption (keep it less than 900 characters)"

    if description:
        # Generate and display the caption
        detailed_caption = generate_caption(description)
        
        st.write("Detailed Caption:", detailed_caption)
        st.title("Generated Outfits")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Groom's Outfit")
            response = openai.Image.create(
                model="dall-e-3",
                prompt=detailed_caption+'Given is the description of the groom. give a full body image of the groom for a '+selected_function+' ceremony. '+sketch_value,
                n=1,
                size="1024x1024"
            )
            st.image(response['data'][0]['url'])
        with col2:
            st.subheader("Bride's Outfit")
            response = openai.Image.create(
                model="dall-e-3",
                prompt=detailed_caption+'Given is the description of the groom. generate the full body image of a bride in an outfit with similar colours for a '+selected_function+' ceremony. '+sketch_value,
                n=1,
                size="1024x1024"
            )
            st.image(response['data'][0]['url'])

