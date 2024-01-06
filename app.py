"""
I'm making a streamlit website with chat gpt.
"""

from openai import OpenAI
import streamlit as st


headers = {
    "openai-api-key":st.secrets["openai_api_key"]
}


API_KEY = headers["openai-api-key"]

client = OpenAI(
    api_key = API_KEY
)

     
def get_chatgpt_response(client, user_input):

    prompt = (
       """
       I am submitting a research publication abstract. Please grade each sentence 
       with the knowledge required to understand the sentence. 
       Here are the levels:
       Undergraduate Research, Graduate Research, Doctoral Research,
       Postdoctoral Research.
       Please return an html table. Each row is an individual sentence. 
       There are five columns in the table: 1) Index, 2) The level required to understand the sentence, 3)The Orginal Sentence, 
       4) An brief explanation to the grade of the sentence. 5) If the sentence is Doctoral level or above, explain the sentence as if you were talking to an undergraduate student.
       Your response text should only contain the html table. The five column headers of the table should be:
       Index, Level, Original Sentence, Level Explanation, Undergraduate Explanation. \n\n 
       Abstract:\n
        """ + user_input
       )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or another model you prefer
            messages=[
                {"role": "system", "content": "You helpful technical assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response
    except Exception as e:
        return str(e)

defaultText = "Three billion years of evolution has produced a tremendous diversity of protein molecules, but the full potential of proteins is likely to be much greater. Accessing this potential has been challenging for both computation and experiments because the space of possible protein molecules is much larger than the space of those likely to have functions. Here we introduce Chroma, a generative model for proteins and protein complexes that can directly sample novel protein structures and sequences, and that can be conditioned to steer the generative process towards desired properties and functions. To enable this, we introduce a diffusion process that respects the conformational statistics of polymer ensembles, an efficient neural architecture for molecular systems that enables long-range reasoning with sub-quadratic scaling, layers for efficiently synthesizing three-dimensional structures of proteins from predicted inter-residue geometries and a general low-temperature sampling algorithm for diffusion models. Chroma achieves protein design as Bayesian inference under external constraints, which can involve symmetries, substructure, shape, semantics and even natural-language prompts. The experimental characterization of 310 proteins shows that sampling from Chroma results in proteins that are highly expressed, fold and have favourable biophysical properties. The crystal structures of two designed proteins exhibit atomistic agreement with Chroma samples (a backbone root-mean-square deviation of around 1.0 Å). With this unified approach to protein design, we hope to accelerate the programming of protein matter to benefit human health, materials science and synthetic biology."

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")



# ---- HEADER SECTION ----
with st.container():
    st.subheader("Hello Robot. 🤖")
    st.title("Publication Abstract Analysis")
    user_input = st.text_area("Enter your publication abstract here", 
                                value=defaultText, height=300)
    if st.button("Analyze"):
        if user_input:
            with st.spinner("Analyzing..."):
                chatgpt_response = get_chatgpt_response(client, user_input)
                newParagraph = chatgpt_response.choices[0].message.content
                st.markdown(newParagraph, unsafe_allow_html=True)
        else:
            st.error("Please enter an abstract to analyze.")





