from .Planner import PlannerAgent
from autogen import UserProxyAgent



def func(key, prompt, availiable_funcs):
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
    plannerAgent = PlannerAgent(gpt4_config, availiable_funcs)
    #User Proxy
    user_proxy = UserProxyAgent(
        name="Admin",
        system_message="Admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
        human_input_mode="NEVER",
        code_execution_config=False,
    )
    user_proxy.initiate_chat(plannerAgent, message=prompt,
)