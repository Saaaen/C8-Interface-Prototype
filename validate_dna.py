from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class DNASequenceModel:
    sequence: str

class ValidateDNASequenceFunction:
    def init(self):
        # Initialization phase if needed
        pass
    
    def run(self, model: DNASequenceModel) -> bool:
        # Execution phase: Validate DNA sequence
        valid_nucleotides = {'A', 'C', 'G', 'T'}
        return all(nucleotide in valid_nucleotides for nucleotide in model.sequence)

class ConvertDNAToRNAFunction:
    def init(self):
        # Initialization phase if needed
        pass
    
    def run(self, input_model: DNASequenceModel) -> str:
        # Execution phase: Convert DNA sequence to RNA sequence
        rna_sequence = input_model.sequence.replace('T', 'U')
        return rna_sequence