from langgraph.graph import StateGraph, START, END

from graph.state import FinancialState

from graph.nodes import (
    load_financial_context,
    supervisor_node,
    extract_loan_node,
    cashflow_analysis_node,
    goal_analysis_node,
    investment_analysis_node,
    protection_analysis_node,
    retirement_analysis_node,
    tax_analysis_node,
    scenario_analysis_node,
)

from graph.audit_nodes import (
    audit_request_node,
    audit_intent_node,
    audit_context_node,
    audit_agent_node,
    audit_response_node,
)

from graph.final_guardrail_node import final_guardrail_node

from graph.financial_health_nodes import (
    collect_financial_health_data,
    financial_health_analysis_node,
)

from agents.debt_agent import analyze_debt

from graph.memory_nodes import (
    load_conversation_memory,
    save_conversation_memory,
)


# ============================================================
# SUPERVISOR ROUTING
# ============================================================

def route_after_supervisor(state):

    intent = state["intent"]

    if intent == "DEBT":
        return "extract_loan"

    elif intent == "CASHFLOW":
        return "cashflow_analysis"
    
    elif intent == "EMERGENCY_FUND":
        return "cashflow_analysis"

    elif intent == "GOAL":
        return "goal_analysis"

    elif intent == "INVESTMENT":
        return "investment_analysis"

    elif intent == "INSURANCE":
        return "protection_analysis"

    elif intent == "RETIREMENT":
        return "retirement_analysis"

    elif intent == "TAX":
        return "tax_analysis"

    elif intent == "SCENARIO":
        return "scenario_analysis"

    elif intent == "FINANCIAL_HEALTH":
        return "collect_financial_health_data"

    return END


def route_after_loan_extraction(state):

    missing_information = state.get(
        "missing_information",
        []
    )

    if missing_information:
        return "missing_loan_information"

    return "debt_analysis"


# ============================================================
# DEBT ANALYSIS NODE
# ============================================================

def debt_analysis_node(state):

    user_id = state["user_id"]

    user_message = state["user_message"]
    session_id = state.get("session_id")

    loan = state["loan_request"]

    result = analyze_debt(
        user_id=user_id,
        user_message=user_message,
        loan_amount=loan["loan_amount"],
        interest_rate=loan["interest_rate"],
        tenure_months=loan["tenure_months"],
        session_id=session_id,
    )

    return {
        "analysis": result["analysis"],
        "final_response": result["response"],
    }


# ============================================================
# BUILD GRAPH
# ============================================================

def build_workflow():

    graph = StateGraph(FinancialState)

    # ========================================================
    # NODES
    # ========================================================

    # -------------------------
    # Memory
    # -------------------------

    graph.add_node(
        "load_conversation_memory",
        load_conversation_memory,
    )

    graph.add_node(
        "save_conversation_memory",
        save_conversation_memory,
    )

    # -------------------------
    # Financial Context
    # -------------------------

    graph.add_node(
        "load_financial_context",
        load_financial_context,
    )

    # -------------------------
    # Supervisor
    # -------------------------

    graph.add_node(
        "supervisor",
        supervisor_node,
    )

    # -------------------------
    # Debt
    # -------------------------

    graph.add_node(
        "extract_loan",
        extract_loan_node,
    )

    graph.add_node(
        "debt_analysis",
        debt_analysis_node,
    )

    # -------------------------
    # Cash Flow
    # -------------------------

    graph.add_node(
        "cashflow_analysis",
        cashflow_analysis_node,
    )

    # -------------------------
    # Goal
    # -------------------------

    graph.add_node(
        "goal_analysis",
        goal_analysis_node,
    )

    # -------------------------
    # Investment
    # -------------------------

    graph.add_node(
        "investment_analysis",
        investment_analysis_node,
    )

    # -------------------------
    # Protection / Insurance
    # -------------------------

    graph.add_node(
        "protection_analysis",
        protection_analysis_node,
    )

    # -------------------------
    # Retirement
    # -------------------------

    graph.add_node(
        "retirement_analysis",
        retirement_analysis_node,
    )

    # -------------------------
    # Tax
    # -------------------------

    graph.add_node(
        "tax_analysis",
        tax_analysis_node,
    )

    # -------------------------
    # Scenario
    # -------------------------

    graph.add_node(
        "scenario_analysis",
        scenario_analysis_node,
    )

    # -------------------------
    # Financial Health
    # -------------------------

    graph.add_node(
        "collect_financial_health_data",
        collect_financial_health_data,
    )

    graph.add_node(
        "financial_health_analysis",
        financial_health_analysis_node,
    )

    # -------------------------
    # Audit
    # -------------------------

    graph.add_node(
        "audit_request",
        audit_request_node,
    )

    graph.add_node(
        "audit_intent",
        audit_intent_node,
    )

    graph.add_node(
        "audit_context",
        audit_context_node,
    )

    graph.add_node(
        "audit_agent",
        audit_agent_node,
    )

    graph.add_node(
        "audit_response",
        audit_response_node,
    )

    graph.add_node(
        "final_guardrail",
        final_guardrail_node,
    )

    # ========================================================
    # START
    # ========================================================

    graph.add_edge(
        START,
        "audit_request",
    )

    # ========================================================
    # AUDIT REQUEST → MEMORY
    # ========================================================

    graph.add_edge(
        "audit_request",
        "load_conversation_memory",
    )

    # ========================================================
    # MEMORY → FINANCIAL CONTEXT
    # ========================================================

    graph.add_edge(
        "load_conversation_memory",
        "load_financial_context",
    )

    # ========================================================
    # FINANCIAL CONTEXT → SUPERVISOR
    # ========================================================

    graph.add_edge(
        "load_financial_context",
        "supervisor",
    )

    # ========================================================
    # SUPERVISOR → AUDIT CHAIN
    # ========================================================

    graph.add_edge(
        "supervisor",
        "audit_intent",
    )

    graph.add_edge(
        "audit_intent",
        "audit_context",
    )

    graph.add_edge(
        "audit_context",
        "audit_agent",
    )

    # ========================================================
    # AUDIT AGENT → SPECIALIST ROUTING
    # ========================================================

    graph.add_conditional_edges(
        "audit_agent",
        route_after_supervisor,
        {
            "extract_loan": "extract_loan",

            "cashflow_analysis": "cashflow_analysis",

            "goal_analysis": "goal_analysis",

            "investment_analysis": "investment_analysis",

            "protection_analysis": "protection_analysis",

            "retirement_analysis": "retirement_analysis",

            "tax_analysis": "tax_analysis",

            "scenario_analysis": "scenario_analysis",

            "collect_financial_health_data":
                "collect_financial_health_data",

            END: END,
        },
    )

    # ========================================================
    # DEBT FLOW
    # ========================================================

    graph.add_conditional_edges(
        "extract_loan",
        route_after_loan_extraction,
        {
            "missing_loan_information":
                "save_conversation_memory",

            "debt_analysis":
                "debt_analysis",
        },
    )

    graph.add_edge(
        "debt_analysis",
        "save_conversation_memory",
    )

    # ========================================================
    # CASH FLOW
    # ========================================================

    graph.add_edge(
        "cashflow_analysis",
        "save_conversation_memory",
    )

    # ========================================================
    # GOAL
    # ========================================================

    graph.add_edge(
        "goal_analysis",
        "save_conversation_memory",
    )

    # ========================================================
    # INVESTMENT
    # ========================================================

    graph.add_edge(
        "investment_analysis",
        "save_conversation_memory",
    )

    # ========================================================
    # PROTECTION / INSURANCE
    # ========================================================

    graph.add_edge(
        "protection_analysis",
        "save_conversation_memory",
    )

    # ========================================================
    # RETIREMENT
    # ========================================================

    graph.add_edge(
        "retirement_analysis",
        "save_conversation_memory",
    )

    # ========================================================
    # TAX
    # ========================================================

    graph.add_edge(
        "tax_analysis",
        "save_conversation_memory",
    )

    # ========================================================
    # SCENARIO
    # ========================================================

    graph.add_edge(
        "scenario_analysis",
        "save_conversation_memory",
    )

    # ========================================================
    # FINANCIAL HEALTH
    # ========================================================

    graph.add_edge(
        "collect_financial_health_data",
        "financial_health_analysis",
    )

    graph.add_edge(
        "financial_health_analysis",
        "save_conversation_memory",
    )

    # ========================================================
    # SAVE MEMORY → FINAL GUARDRAIL
    # ========================================================

    graph.add_edge(
        "save_conversation_memory",
        "final_guardrail",
    )

    # ========================================================
    # FINAL GUARDRAIL → RESPONSE AUDIT
    # ========================================================

    graph.add_edge(
        "final_guardrail",
        "audit_response",
    )

    # ========================================================
    # RESPONSE AUDIT → END
    # ========================================================

    graph.add_edge(
        "audit_response",
        END,
    )

    # ========================================================
    # COMPILE
    # ========================================================

    return graph.compile()


# ============================================================
# APPLICATION
# ============================================================

app = build_workflow()
graph = app