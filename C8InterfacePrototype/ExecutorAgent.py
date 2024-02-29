from autogen import UserProxyAgent
import autogen
from typing import Any, Dict, List, Optional, Union
import shelve
from C8InterfacePrototype import validate_dna 

dna_sequence = validate_dna.DNASequenceModel(sequence="ATGCGA")
validator = validate_dna.ValidateDNASequenceFunction()
converter = validate_dna.ConvertDNAToRNAFunction()
# Store the instance in shelve
with shelve.open('translator_shelve') as db:
    db['dna_validator'] = validator
    db['dna_to_rna'] = converter
del validator
del converter

sys_msg_exec = """Read the function description and the request. Extract proper input value from the request.
                  Execute the function and report the result."""
class Executor(UserProxyAgent):
  def __init__(self):
    super().__init__(
            name="Executor",
            is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            code_execution_config={"last_n_messages": 3, "work_dir": "coding"},
            system_message=sys_msg_exec,
        )
    self.register_reply(autogen.ConversableAgent, Executor._generate_ua_reply)

  def _generate_ua_reply(
      self,
      messages: Optional[List[Dict]] = None,
      sender: Optional[autogen.Agent] = None,
      config: Optional[Any] = None,
  ) -> Union[str, Dict, None]:
    message = messages[-1]
    funcName = message['content']
    dna_sequence = validate_dna.DNASequenceModel(sequence = 'ATGCTAGCTAG')
    with shelve.open('translator_shelve') as db:
      func = db[funcName]
      result = func.run(dna_sequence)
      print('result: ' + str(result))
    return True, None