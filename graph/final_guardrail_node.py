from guardrails.advice_guardrails import guard_advice
from guardrails.output_safety_guardrail import sanitize_output
from guardrails.nism_grounding_guardrail import apply_nism_grounding


def final_guardrail_node(state):

    response = state.get("final_response", "")
    context = state.get("financial_context", {})
    rag_results = state.get("rag_results", [])

    # ---------------------------------------------------------
    # 1. Advice safety
    # ---------------------------------------------------------
    advice_check = guard_advice(
        response,
        context
    )

    # ---------------------------------------------------------
    # 2. Output safety
    # ---------------------------------------------------------
    output_check = sanitize_output(response)

    if not output_check.get("allowed", False):

        unsafe = output_check.get(
            "unsafe_phrases",
            []
        )

        return {
            "final_response": (
                "I cannot provide that recommendation safely "
                "with the available information. "
                "Please provide the required financial details "
                "so the analysis can be completed."
            ),
            "errors": [
                f"Unsafe output detected: {unsafe}"
            ],
        }

    final_response = response

    # ---------------------------------------------------------
    # 3. Advice warnings
    # ---------------------------------------------------------
    warnings = advice_check.get("warnings", [])

    if warnings:
        final_response += (
            "\n\nNote: This analysis is based on the "
            "financial information currently available."
        )

    # ---------------------------------------------------------
    # 4. NISM grounding
    # ---------------------------------------------------------
    grounding = apply_nism_grounding(
        final_response,
        rag_results
    )

    # ---------------------------------------------------------
    # 5. Use grounded response
    # ---------------------------------------------------------
    final_response = grounding["response"]

    # ---------------------------------------------------------
    # 6. Add NISM citations
    # ---------------------------------------------------------
    if grounding["grounded"]:

        citations = grounding.get(
            "citations",
            []
        )

        if citations:

            final_response += "\n\nNISM references:\n"

            for citation in citations:
                final_response += f"- {citation}\n"

    else:

        warning = grounding.get("warning")

        if warning:
            final_response += (
                f"\n\nNISM grounding note: {warning}"
            )

    return {
        "final_response": final_response
    }