from autogen import AssistantAgent, ConversableAgent, Agent
from openai.embeddings_utils import get_embedding, cosine_similarity
from typing import Any, Dict, List, Optional, Union
import pandas as pd
import openai
from . import ExecutorAgent

sys_msg = """You suggest the best option for a given request from a list. Reply None if you think none of the availiabe functions work. You don't write code.
You should only reply with a function name."""

class FunctionFinderAgent(AssistantAgent):
  availiable_functions: pd.DataFrame
  def __init__(self, availiable_functions: pd.DataFrame, config):
    super().__init__(
            name="FuncFinder",
            system_message=sys_msg,
            llm_config=config,
            max_consecutive_auto_reply=10,
        )
    self.register_reply(ConversableAgent, FunctionFinderAgent._generate_ffa_reply)
    self.availiable_functions = availiable_functions

  def _generate_ffa_reply(
      self,
      messages: Optional[List[Dict]] = None,
      sender: Optional[Agent] = None,
      config: Optional[Any] = None,
  ) -> Union[str, Dict, None]:
    message = messages[-1]
    #query the top 4: //Todo
    req = message['content'].split('\n')[0].strip()
    request_embedding = get_embedding(
        req,
        engine="text-embedding-ada-002"
    )
    df = self.availiable_functions
    df["similarity"] = df.embedding.apply(lambda x: cosine_similarity(x, request_embedding))
    results = (
        df.sort_values("similarity", ascending=False)
        .head(4)
        .Name
    )
    results = results.tolist()
    result_dict = {'content': 'avaliable functions: ' + str(results), 'role': 'assistant'}
    reply = self.generate_reply([result_dict] + [message], sender, exclude=[FunctionFinderAgent._generate_ffa_reply])
    func_reply = reply if isinstance(reply, str) else str(reply["content"])
    print('suggest function: ' + func_reply)
    executor = ExecutorAgent.Executor()
    self.initiate_chat(executor, message=func_reply)
    return True, None