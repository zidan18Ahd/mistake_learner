from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from data_models import (
    CodePair, MistakeEval, ReasoningHypothesis,
    CorrectReasoning, DivergencePoint, MemoryNode
)

class PipelineState(TypedDict):
    code_pair: CodePair
    is_real_mistake: bool
    reason: str
    wrong_reasoning: str
    correct_reasoning: str
    divergence: str
    memory_node: MemoryNode | None

base_model = ChatGroq(model="llama-3.3-70b-versatile")

eval_model    = base_model.with_structured_output(MistakeEval)
infer_model   = base_model.with_structured_output(ReasoningHypothesis)
correct_model = base_model.with_structured_output(CorrectReasoning)
diverge_model = base_model.with_structured_output(DivergencePoint)

def evaluate_mistake(state: PipelineState) -> dict:
    """Stage 2: Is the change a real logic error?"""
    pair = state["code_pair"]
    prompt = (
        "You are reviewing two versions of code.\n\n"
        f"OLD (wrong):\n```{pair.language}\n{pair.wrong_code}\n```\n\n"
        f"NEW (fixed):\n```{pair.language}\n{pair.fixed_code}\n```\n\n"
        "Is the change a real logic mistake (not renaming, reformatting, or trivial style)? Explain why."
    )
    result: MistakeEval = eval_model.invoke(prompt)
    return {
        "is_real_mistake": result.is_real_mistake,
        "reason": result.reason,
    }

def infer_wrong_reasoning(state: PipelineState) -> dict:
    """Stage 3: Hypothesise the wrong reasoning path."""
    if not state["is_real_mistake"]:
        return {}
    pair = state["code_pair"]
    prompt = (
        f"Wrong code:\n```{pair.language}\n{pair.wrong_code}\n```\n\n"
        f"Corrected code:\n```{pair.language}\n{pair.fixed_code}\n```\n\n"
        "Don't describe the diff. Hypothesise the reasoning path the developer followed when they wrote the WRONG code. "
        "What were they probably trying to do, and where did their thinking go wrong?"
    )
    result: ReasoningHypothesis = infer_model.invoke(prompt)
    return {"wrong_reasoning": result.hypothesized_reasoning}

def infer_correct_reasoning(state: PipelineState) -> dict:
    """Stage 4: Explain why the corrected code is right."""
    if not state["is_real_mistake"]:
        return {}
    pair = state["code_pair"]
    prompt = (
        f"Correct code:\n```{pair.language}\n{pair.fixed_code}\n```\n\n"
        "Explain the correct reasoning. Why is this code written the right way?"
    )
    result: CorrectReasoning = correct_model.invoke(prompt)
    return {"correct_reasoning": result.correct_reasoning}

def compare_routes(state: PipelineState) -> dict:
    """Stage 5: Find the exact decision point where the two reasoning paths split."""
    if not state["is_real_mistake"]:
        return {}
    prompt = (
        f"Wrong reasoning:\n{state['wrong_reasoning']}\n\n"
        f"Correct reasoning:\n{state['correct_reasoning']}\n\n"
        "Identify the single decision point or assumption where the two reasoning paths diverge. "
        "That is: what was the crucial wrong assumption or choice that led to the mistake? "
        "Be specific and concise (1–2 sentences)."
    )
    result: DivergencePoint = diverge_model.invoke(prompt)
    return {"divergence": result.divergence_point}

def build_memory_node(state: PipelineState) -> dict:
    """Stage 6: Package everything into a MemoryNode."""
    if not state["is_real_mistake"]:
        return {"memory_node": None}
    node = MemoryNode(
        divergence_point=state["divergence"],
        language=state["code_pair"].language,
    )
    return {"memory_node": node}

def create_pipeline():
    builder = StateGraph(PipelineState)
    builder.add_node("evaluate", evaluate_mistake)
    builder.add_node("infer_wrong", infer_wrong_reasoning)
    builder.add_node("infer_correct", infer_correct_reasoning)
    builder.add_node("compare", compare_routes)
    builder.add_node("build_memory", build_memory_node)
    builder.set_entry_point("evaluate")
    builder.add_edge("evaluate", "infer_wrong")
    builder.add_edge("infer_wrong", "infer_correct")
    builder.add_edge("infer_correct", "compare")
    builder.add_edge("compare", "build_memory")
    builder.add_edge("build_memory", END)
    return builder.compile()

pipeline = create_pipeline()