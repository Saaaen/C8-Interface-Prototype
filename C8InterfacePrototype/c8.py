from .Planner import PlannerAgent
from autogen import UserProxyAgent
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
import openai


data = [['dna_to_protein', 'Translate the DNA sequence into a protein sequence, based on the codon table'], ['reverse complement', 'Generate the reverse complement of the DNA sequence'],['getPlasmidSequence', 'Generate the reverse complement of the DNA sequence'],
        ['dna_validator', 'Validates if the given sequence is a valid DNA sequence.'], ['dna_to_rna', 'Converts a DNA sequence to an RNA sequence'], ['rna_to_protein', 'Converts a RNA sequence to an protein sequence'], ['cloneExperimentDesign', 'Frist retrieve the sequence of plasmid, then identify the location of amilGFp']]
dummies = [[f'dummy{i}', f'dummy{i}'] for i in range(50)]
data += dummies
df = pd.DataFrame(data, columns=['Name', 'Description'])
df["combined"] = (
    "Name: " + df.Name.str.strip() + "; Description: " + df.Description.str.strip()
)

def run(key, prompt):
    config_list_4 = [
        {
            'model': 'gpt-4',
            'api_key': key,
        },
    ]
    gpt4_config = {
        "temperature": 0,
        "config_list": config_list_4,
        "timeout": 120,
    }
    openai.api_key = key
    if "embedding" not in df:
        df["embedding"] = df.combined.apply(lambda x: get_embedding(x, engine="text-embedding-ada-002"))
    plannerAgent = PlannerAgent(gpt4_config, df)
    #User Proxy
    user_proxy = UserProxyAgent(
        name="Admin",
        system_message="Admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
        human_input_mode="NEVER",
        code_execution_config=False,
    )
    user_proxy.initiate_chat(plannerAgent, message=prompt,
)
    
def load_function(func_name, func_description):
    pass