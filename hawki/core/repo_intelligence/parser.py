# --------------------
# File: hawki/core/repo_intelligence/parser.py
# --------------------
"""
Solidity parser using tree‑sitter.
Extracts contracts, functions, state variables, modifiers, and inheritance.
Produces a structured representation for further analysis.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

import tree_sitter
import tree_sitter_solidity

logger = logging.getLogger(__name__)

class SolidityParser:
    """Parses Solidity source files and builds an AST index."""

    def __init__(self):
        self._language = tree_sitter.Language(tree_sitter_solidity.language())
        self._parser = tree_sitter.Parser(self._language)

    def parse_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Parse a single Solidity file and return a structured representation.
        Returns None if parsing fails.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            return None

        tree = self._parser.parse(bytes(source_code, "utf8"))
        if not tree:
            logger.error(f"Failed to parse {file_path}")
            return None

        # Walk the tree and extract contracts, functions, etc.
        contracts = self._extract_contracts(tree.root_node, source_code)
        return {
            "path": str(file_path),
            "source": source_code,
            "contracts": contracts,
        }

    def _extract_contracts(self, node: tree_sitter.Node, source: str) -> List[Dict]:
        """Recursively extract contract definitions."""
        contracts = []
        if node.type == "contract_declaration":
            name_node = node.child_by_field_name("name")
            name = self._node_text(name_node, source) if name_node else "<anonymous>"
            functions = self._extract_functions(node, source)
            state_vars = self._extract_state_variables(node, source)
            modifiers = self._extract_modifiers(node, source)
            inheritance = self._extract_inheritance(node, source)
            contracts.append({
                "name": name,
                "functions": functions,
                "state_variables": state_vars,
                "modifiers": modifiers,
                "inheritance": inheritance,
            })
        # Recursively process children (to find nested contracts)
        for child in node.children:
            contracts.extend(self._extract_contracts(child, source))
        return contracts

    def _extract_functions(self, contract_node: tree_sitter.Node, source: str) -> List[Dict]:
        """Extract function definitions inside a contract."""
        functions = []
        for child in contract_node.children:
            if child.type == "function_declaration":
                name_node = child.child_by_field_name("name")
                name = self._node_text(name_node, source) if name_node else "fallback"
                params = self._extract_parameters(child, source)
                modifiers = self._extract_modifier_names(child, source)
                visibility = self._extract_visibility(child, source)
                state_mutability = self._extract_state_mutability(child, source)
                returns = self._extract_returns(child, source)
                functions.append({
                    "name": name,
                    "parameters": params,
                    "modifiers": modifiers,
                    "visibility": visibility,
                    "state_mutability": state_mutability,
                    "returns": returns,
                })
        return functions

    def _extract_state_variables(self, contract_node: tree_sitter.Node, source: str) -> List[Dict]:
        """Extract state variable declarations."""
        variables = []
        for child in contract_node.children:
            if child.type == "state_variable_declaration":
                name_node = child.child_by_field_name("name")
                name = self._node_text(name_node, source) if name_node else "unknown"
                type_node = child.child_by_field_name("type")
                var_type = self._node_text(type_node, source) if type_node else "unknown"
                visibility = self._extract_visibility(child, source)
                variables.append({
                    "name": name,
                    "type": var_type,
                    "visibility": visibility,
                })
        return variables

    def _extract_modifiers(self, contract_node: tree_sitter.Node, source: str) -> List[Dict]:
        """Extract modifier definitions."""
        modifiers = []
        for child in contract_node.children:
            if child.type == "modifier_declaration":
                name_node = child.child_by_field_name("name")
                name = self._node_text(name_node, source) if name_node else "unknown"
                params = self._extract_parameters(child, source)
                modifiers.append({
                    "name": name,
                    "parameters": params,
                })
        return modifiers

    def _extract_inheritance(self, contract_node: tree_sitter.Node, source: str) -> List[str]:
        """Extract base contracts from inheritance specifiers."""
        bases = []
        for child in contract_node.children:
            if child.type == "inheritance_specifier":
                name_node = child.child_by_field_name("name")
                if name_node:
                    bases.append(self._node_text(name_node, source))
        return bases

    def _extract_parameters(self, node: tree_sitter.Node, source: str) -> List[Dict]:
        """Extract function/modifier parameters."""
        params = []
        for child in node.children:
            if child.type == "parameter":
                name_node = child.child_by_field_name("name")
                type_node = child.child_by_field_name("type")
                name = self._node_text(name_node, source) if name_node else ""
                param_type = self._node_text(type_node, source) if type_node else ""
                params.append({"name": name, "type": param_type})
        return params

    def _extract_modifier_names(self, node: tree_sitter.Node, source: str) -> List[str]:
        """Extract names of modifiers applied to a function."""
        modifiers = []
        for child in node.children:
            if child.type == "modifier_invocation":
                name_node = child.child_by_field_name("name")
                if name_node:
                    modifiers.append(self._node_text(name_node, source))
        return modifiers

    def _extract_visibility(self, node: tree_sitter.Node, source: str) -> str:
        """Extract visibility specifier (public, internal, external, private)."""
        for child in node.children:
            if child.type in ["public", "internal", "external", "private"]:
                return child.type
        return "internal"  # default in Solidity

    def _extract_state_mutability(self, node: tree_sitter.Node, source: str) -> str:
        """Extract state mutability (pure, view, payable, nonpayable)."""
        for child in node.children:
            if child.type in ["pure", "view", "payable"]:
                return child.type
        return "nonpayable"

    def _extract_returns(self, node: tree_sitter.Node, source: str) -> List[Dict]:
        """Extract return parameters."""
        returns = []
        for child in node.children:
            if child.type == "returns":
                for param in child.children:
                    if param.type == "parameter":
                        name_node = param.child_by_field_name("name")
                        type_node = param.child_by_field_name("type")
                        name = self._node_text(name_node, source) if name_node else ""
                        param_type = self._node_text(type_node, source) if type_node else ""
                        returns.append({"name": name, "type": param_type})
        return returns

    def _node_text(self, node: Optional[tree_sitter.Node], source: str) -> str:
        """Safely extract text from a node."""
        if not node:
            return ""
        return source[node.start_byte:node.end_byte]

# EOF: hawki/core/repo_intelligence/parser.py