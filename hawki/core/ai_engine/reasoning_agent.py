# --------------------
# File: hawki/core/ai_engine/reasoning_agent.py
# --------------------
"""
AI reasoning agent that uses the orchestrator to analyse contracts.
Produces findings in the same format as static rules.
"""

import json
import logging
from typing import List, Dict, Any, Optional

from .llm_orchestrator import LLMOrchestrator

logger = logging.getLogger(__name__)

class ReasoningAgent:
    """Applies AI analysis to contract data."""

    def __init__(self, orchestrator: Optional[LLMOrchestrator] = None):
        self.orchestrator = orchestrator or LLMOrchestrator()

    def analyse_contracts(
        self, contract_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Run AI analysis on each contract and collect findings.
        Uses the 'vuln_analysis_prompt' template.
        """
        findings = []
        for contract in contract_data:
            # Prepare context: contract name, source, functions, etc.
            context = {
                "contract_name": contract.get("name", "unknown"),
                "source_code": contract.get("source", ""),
                "functions": contract.get("functions", []),
                "state_variables": contract.get("state_variables", []),
            }
            result = self.orchestrator.analyze(
                template_name="vuln_analysis_prompt",
                **context,
            )
            if result:
                # Expect result to contain a list of findings under a "findings" key
                ai_findings = result.get("findings", [])
                for f in ai_findings:
                    f["rule"] = "AI_Reasoning"
                    f["source"] = "ai"
                    findings.append(f)
            else:
                logger.debug(f"No AI result for contract {contract.get('name')}")

        return findings

    def score_contract(self, contract: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate a risk score for a single contract.
        Uses 'risk_scoring_prompt' template.
        """
        context = {
            "contract_name": contract.get("name", "unknown"),
            "source_code": contract.get("source", ""),
        }
        return self.orchestrator.analyze(
            template_name="risk_scoring_prompt",
            **context,
        )

    def general_query(self, query: str, contract_context: Optional[Dict] = None) -> Optional[str]:
        """
        General purpose query using 'general_contract_prompt'.
        Returns raw text response.
        """
        context = {
            "user_query": query,
            "contract_context": json.dumps(contract_context) if contract_context else "None",
        }
        result = self.orchestrator.analyze(
            template_name="general_contract_prompt",
            **context,
        )
        if result and "raw_response" in result:
            return result["raw_response"]
        return None

# EOF: hawki/core/ai_engine/reasoning_agent.py