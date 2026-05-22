from typing import Annotated, List, TypedDict, Union
from typing_extensions import TypedDict

class AgentState(TypedDict):
    # The current message history
    messages: List[str]
    # The current focus of the swarm
    focus: str
    # Research findings collected so far
    findings: List[str]
    # Strategic insights generated
    insights: List[str]
    # Final report draft
    report: str
    # Next step in the process
    next_step: str
