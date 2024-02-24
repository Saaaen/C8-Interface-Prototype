from Planner import PlannerAgent
from autogen import UserProxyAgent
key_dept = ''




def func(key, prompt):
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
    plannerAgent = PlannerAgent(gpt4_config)
    #User Proxy
    user_proxy = UserProxyAgent(
        name="Admin",
        system_message="Admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
        human_input_mode="NEVER",
        code_execution_config=False,
    )
    user_proxy.initiate_chat(plannerAgent, message=prompt,
)
    
func(key_dept, """
Design an indicator plasmid for a CRISPR-based deletion system..  It should have a pUC origin, and amilGFP under a constitutive promoter.  There should be a cassette inserted into the amilGFP CDS encoding the sequences T2 and T3.  This cassette is exactly:  'GGATCCACTAGTCTCTAGCTCGAGAAATTTTACTCTAGAAAGAGGAGAAAGGATCC'.  The editing system behaves essentially like BamHI and ligase -- the two GGATCC sites on the ends of this fragment become one sequence, excising the ~40 bp in between.  So, the sequence GGATCC must be silently inserted into the amilGFP gene such that upon editing a functional amilGFP is restored.  You should use plasmid p20N31 as the starting point and construct the indicator plasmid in as few steps as possible with minimal cost.
""")
