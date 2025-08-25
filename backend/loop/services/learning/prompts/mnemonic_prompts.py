"""Mnemonic generation prompts."""
from typing import List

from loop.db.models.learning import Subtopic


def build_mnemonic_prompt(subtopic: Subtopic, concepts: List[str]) -> str:
    """Build prompt for mnemonic generation."""
    concepts_list = "\n".join([f"- {concept}" for concept in concepts])
    
    return f"""
Create memorable mnemonics for these complex concepts in "{subtopic.name}":

{concepts_list}

Requirements:
1. Create vivid, memorable mental images
2. Use acronyms, stories, or visual associations
3. Make them relevant to backend engineering context
4. Include explanation of how the mnemonic connects to the concept
5. Ensure they're professional and appropriate

Return as JSON in this exact format:
{{
    "mnemonics": [
        {{
            "concept": "Concept name",
            "mnemonic": "The mnemonic device",
            "explanation": "How this helps remember the concept",
            "type": "acronym|story|visual|rhyme"
        }}
    ]
}}

Make them stick in a senior engineer's memory.
"""


MNEMONIC_SYSTEM_PROMPT = """
You are an expert at creating memorable mnemonics and memory aids for technical concepts. 
Create vivid, professional memory devices that help senior backend engineers remember 
complex technical information. Focus on creating strong mental associations that will 
last and be practically useful in day-to-day work.
"""