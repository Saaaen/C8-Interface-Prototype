import autogen
from typing import Any, Dict, List, Optional, Union
from .FunctionFinderAgent import FunctionFinderAgent

sys_msg_p = """
Suggest a plan. The plan should a set of functions needed to perform the task step-by-step described by the given Prompt. These functions should be expressed in a way that makes them applicable to a broad range of similar tasks,
not just the specific example provided. The response format should include a general description of the function, abstract inputs and outputs, and relevant keywords that cover a wide range of applications within the domain. Express your response as a series of JSON formatted as:
[{
"request" : "", //A native text description of the Function required
"inputs" : [""], //Inputs to be provided to the Function
"type": String. Data type of input (e.g., "str")
"description": String. Role of the input.
"outputs": List of objects with:
"type": String. Data type of output
"description": String. Meaning of the output.
}]
"""

def ask_to_find(message, availiable_functions, config):
  funcFinder = FunctionFinderAgent(availiable_functions, config)
  expert = autogen.UserProxyAgent(
        name="expert",
        system_message = 'You provide the other agent a request and the other agent will find a function for it. Once you recevie the function name, stop reply and end the chat',
        human_input_mode="AlWAYS",
        code_execution_config={"last_n_messages": 3, "work_dir": "expert", "use_docker": False,},

    )
  expert.initiate_chat(funcFinder, message=message)
  expert.stop_reply_at_receive(funcFinder)
  return None
class PlannerAgent(autogen.AssistantAgent):
  config: Dict
  def __init__(self, config, availiable_funcs):
    super().__init__(
            name="PlannerAgent",
            system_message=sys_msg_p,
            llm_config = config,
            max_consecutive_auto_reply=10,
        )
    self.register_reply(autogen.ConversableAgent, PlannerAgent._generate_pa_reply)
    self.config = config
    self.availiable_funcs = availiable_funcs
  def _generate_pa_reply(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[autogen.Agent] = None,
        config: Optional[Any] = None,
    ) -> Union[str, Dict, None]:
    message = messages[-1]
    #Ask for tools/instructions from GPT-4
    reply = self.generate_reply(
              messages, sender, exclude=[PlannerAgent._generate_pa_reply]
            )
    #Convert str to list
    local_vars = {"reply": reply}
    exec('reply_list='+reply, {}, local_vars)
    reply_list = local_vars["reply_list"]
    print(reply_list)
    #Loop through the tools
    for r in reply_list:
      ask_to_find(r['request'], self.availiable_funcs, self.config)
    return True, None