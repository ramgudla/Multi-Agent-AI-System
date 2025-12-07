def get_model():
    """Get the model"""
    return llm

from langchain_ollama import ChatOllama
llm = ChatOllama(model="qwen2.5:14b",temperature=0)

# from langchain_community.chat_models.oci_generative_ai import ChatOCIGenAI
# llm = ChatOCIGenAI(
#             model_id="cohere.command-r-08-2024",
#             service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
#             compartment_id="ocid1.compartment.oc1..xxxxx",
#             auth_type="API_KEY",
#             auth_profile="xxxxx",
#             model_kwargs={"temperature": 0, "top_p": 0.75, "max_tokens": 512}
#         )
