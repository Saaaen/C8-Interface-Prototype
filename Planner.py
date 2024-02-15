import autogen
from typing import Any, Dict, List, Optional, Union
from FunctionFinderAgent import FunctionFinderAgent
import pandas as pd
from openai.embeddings_utils import get_embedding

sys_msg_p = """
Suggest a plan. The plan should a set of functions needed to perform the task step-by-step described by the given Prompt. These functions should be expressed in a way that makes them applicable to a broad range of similar tasks,
not just the specific example provided. The response format should include a general description of the function, abstract inputs and outputs, and relevant keywords that cover a wide range of applications within the domain. Express your response as a series of JSON formatted as:
[{
"request" : "", //A native text description of the Function required
"inputs" : [""], //Inputs to be provided to the Function
"outputs" : [""], //Outputs to be returned by the Function
"keywords" : [""], //keywords, specific algorithms or other names
}]
"""

data = [['translate', 'Translate the DNA sequence into a protein sequence, based on the codon table'], ['reverse complement 1', 'Generate the reverse complement of the DNA sequence'],['getPlasmidSequence', 'Generate the reverse complement of the DNA sequence']]
dummies = [[f'dummy{i}', f'dummy{i}'] for i in range(50)]
data += dummies
df = pd.DataFrame(data, columns=['Name', 'Description'])
df["combined"] = (
    "Name: " + df.Name.str.strip() + "; Description: " + df.Description.str.strip()
)
df["embedding"] = df.combined.apply(lambda x: get_embedding(x, engine='text-embedding-ada-002'))


def ask_to_find(message, availiable_functions, config):
  funcFinder = FunctionFinderAgent(availiable_functions, config)
  expert = autogen.UserProxyAgent(
        name="expert",
        human_input_mode="NEVER",
        code_execution_config={"last_n_messages": 3, "work_dir": "expert", "use_docker": False,},

    )
  expert.initiate_chat(funcFinder, message=message)
  #expert.stop_reply_at_receive(funcFinder)
  #expert.send("summarize the suggestions", funcFinder)
  return None
class PlannerAgent(autogen.AssistantAgent):
  config: Dict
  def __init__(self, config):
    super().__init__(
            name="PlannerAgent",
            system_message=sys_msg_p,
            llm_config = config,
            max_consecutive_auto_reply=10,
        )
    self.register_reply(autogen.ConversableAgent, PlannerAgent._generate_pa_reply)
    self.config = config
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
    #Loop through the tools
    for r in reply_list:
      ask_to_find(r['request'], df, self.config)
    return True, None