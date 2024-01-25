import streamlit as st
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import os

os.environ["CLARIFAI_PAT"] = "7a721760203b47449d49d281dd2f3c9c"

PAT = '7a721760203b47449d49d281dd2f3c9c'

# Specify the correct user_id/app_id pairings
USER_ID = 'openai'
APP_ID = 'chat-completion'

# Change these to the appropriate model details
MODEL_ID = 'GPT-4'
MODEL_VERSION_ID = '5d7a50b44aec4a01a9c492c5a5fcf387'

def is_medical_question(question):
    medical_keywords = [
        'medical', 'health', 'doctor', 'hospital', 'treatment',
        'disease', 'condition', 'symptoms', 'diagnosis', 'prescription',
        'medicine', 'vaccine', 'therapy', 'fever', 'surgery', 'nutrition',
        'wellness', 'exercise', 'rehabilitation', 'mental health',
        'cardiology', 'oncology', 'neurology', 'pediatrics', 'geriatrics',
        'infection', 'allergy', 'immunization', 'screening', 'preventive care',
        'chronic', 'acute', 'palliative care', 'genetics', 'radiology',
        'pharmacy', 'laboratory tests', 'emergency', 'ambulance', 'paramedic',
        'physical therapy', 'occupational therapy', 'speech therapy',
        'blood pressure', 'cholesterol', 'diabetes', 'asthma', 'arthritis',
        'cancer', 'heart disease', 'stroke', 'Alzheimer\'s', 'mental illness',
        'flu', 'COVID-19', 'pandemic', 'virus', 'bacteria', 'inflammation',
        'vaccination', 'public health', 'epidemiology', 'healthcare system',
        'pregnancy', 'obstetrics', 'gynecology', 'dermatology', 'orthopedics',
        'urology', 'gastroenterology', 'ophthalmology', 'otolaryngology',
        'endocrinology', 'rheumatology', 'hematology', 'pulmonology',
        'allergies', 'nutritional supplements', 'sleep disorders',
        'sports medicine', 'alternative medicine', 'telemedicine',
        'insurance', 'medication side effects', 'clinical trials',
        'health research', 'medical history', 'family medical history',
        'health screening', 'blood tests', 'vaccination schedule',
        'travel medicine', 'occupational health', 'public health campaigns',
        'counseling', 'therapy options', 'substance abuse', 'addiction treatment',
        'weight management', 'dietary guidelines', 'fitness routines',
        'holistic health', 'alternative therapies', 'yoga', 'meditation',
        'stress management', 'workplace health', 'ergonomics',
        'health education', 'patient advocacy', 'healthcare policy',
        'medical ethics', 'end-of-life care', 'living will', 'organ donation', 'tired','neurolinguistic'
    ]

    return any(keyword in question.lower() for keyword in medical_keywords)

def main():
    # Set page title and favicon
    st.set_page_config(page_title="Medical and Health Care BOT", page_icon="💊")

    # Page layout
    st.title("Medical and Health Care BOT")
    st.markdown("### Ask me a Medical and Health related question")
    
    # Get user input
    user_input = st.text_input("**Your Question:**")

    # Check if the question is medical-related
    if is_medical_question(user_input):
        RAW_TEXT = 'Provide relevant medical information and dont extend the answer: ' + str(user_input)
        # Set up Clarifai gRPC channel and stub
        channel = ClarifaiChannel.get_grpc_channel()
        stub = service_pb2_grpc.V2Stub(channel)

        metadata = (('authorization', 'Key ' + PAT),)

        userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

        # Make a request to Clarifai API
        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,
                model_id=MODEL_ID,
                version_id=MODEL_VERSION_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=RAW_TEXT
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )

        # Check the response status
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            st.error(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")
        else:
            # Retrieve and display the output
            output = post_model_outputs_response.outputs[0].data.text.raw
            st.text_area("**OUTPUT**", value=output, height=150)
            st.warning("Disclaimer: This BOT is not an alternative to a health professional. It is for awareness purposes only. In case of emergency, consult your medical doctor.")
    else:
        st.warning("I apologize, My knowledge is limited so I can't assist you in this regard.")

if __name__ == "__main__":
    main()
