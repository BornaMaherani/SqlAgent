import os
from typing import Dict, Any

def load_prompt(prompt_name: str, variables: Dict[str, Any] | None = None) -> str:
    """
    Load a system prompt from individual .md files and apply variable substitution.
    
    Args:
        prompt_name: Name of the prompt to load (e.g., "query_chat", "analysis_chat")
        variables: Dictionary of variables to substitute in the prompt
        
    Returns:
        Formatted prompt string
    """
    # Map prompt names to file names
    prompt_files = {
        "query_chat": "query_chat_prompt.md",
        "analysis_chat": "analyse_chat_prompt.md"
    }
    
    if prompt_name not in prompt_files:
        return _get_default_prompt(prompt_name, variables)
    
    # Read the specific prompt file
    prompt_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), prompt_files[prompt_name])
    
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        # Fallback to default prompts if file doesn't exist
        return _get_default_prompt(prompt_name, variables)
    
    # Apply variable substitution
    if variables:
        for key, value in variables.items():
            placeholder = f"{{{key}}}"
            content = content.replace(placeholder, str(value))
    
    return content

def _get_default_prompt(prompt_name: str, variables: Dict[str, Any] | None = None) -> str:
    """
    Fallback default prompts if the prompt files are not available.
    """
    default_prompts = {
        "query_chat": (
            "You are an expert SQL Database Query Writer specializing in T-SQL format.\n"
            "Your task is to generate accurate and efficient SQL queries based on the user's natural language requests.\n\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. ONLY respond with the pure SQL query string - no explanations, no markdown formatting\n"
            "2. Use proper T-SQL syntax with appropriate joins, WHERE clauses, and aggregations\n"
            "3. Handle NULL values appropriately in your queries\n"
            "4. Consider performance implications - use proper indexing and avoid unnecessary operations\n"
            "5. Ensure query safety - avoid SQL injection vulnerabilities by using proper parameterization patterns\n"
            "6. If the request is ambiguous, make reasonable assumptions based on database schema\n\n"
            "DATABASE SCHEMA INFORMATION:\n"
            "AVAILABLE TABLES: {table_names}\n"
            "TABLE STRUCTURES: {table_infos}\n\n"
            "QUERY REQUIREMENTS:\n"
            "- Use proper T-SQL syntax with semicolon termination\n"
            "- Include appropriate error handling considerations\n"
            "- Optimize for read performance\n"
            "- Handle edge cases gracefully\n\n"
            "RESPONSE FORMAT: Pure SQL query only, no additional text"
        ),
        "analysis_chat": (
            "You are an expert Data Analyst specializing in database result analysis.\n\n"
            "TASK: Analyze the provided table data and provide a comprehensive structured analysis in JSON format.\n\n"
            "ANALYSIS REQUIREMENTS:\n"
            "1. Provide statistical summary (count, averages, min/max, unique values)\n"
            "2. Identify trends for time-based data (if available)\n"
            "3. Generate actionable insights and recommendations\n"
            "4. Include sample data preview\n"
            "5. All analysis must be returned as valid JSON only\n\n"
            "DATABASE CONTEXT:\n"
            "Query History: {query_history}\n"
            "Table Columns: {column_names}\n\n"
            "JSON RESPONSE FORMAT (MUST FOLLOW EXACTLY):\n"
            "{{\n"
            '  "analysis": {{\n'
            '    "summary": "comprehensive analysis summary",\n'
            '    "statistics": {{\n'
            '      "total_records": 100,\n'
            '      "average_value": 250.5,\n'
            '      "max_value": 1000,\n'
            '      "min_value": 10,\n'
            '      "unique_values": 25\n'
            '    }},\n'
            '    "trends": [\n'
            '      {{"period": "2024-01", "value": 1200, "change_percentage": 10.5}},\n'
            '      {{"period": "2024-02", "value": 1450, "change_percentage": 20.8}}\n'
            '    ],\n'
            '    "insights": ["insight 1", "insight 2"],\n'
            '    "recommendations": ["recommendation 1", "recommendation 2"]\n'
            '  }},\n'
            '  "table_schema": {{\n'
            '    "columns": ["col1", "col2"],\n'
            '    "sample_data": [{{"col1": "value1", "col2": "value2"}}],\n'
            '    "data_types": {{"col1": "string", "col2": "number"}}\n'
            '  },\n'
            '  "raw_data_preview": [{{"col1": "value1", "col2": "value2"}}],\n'
            '  "query_used": "SELECT * FROM table"\n'
            "}}\n\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. Return ONLY valid JSON - no additional text, no markdown, no code blocks\n"
            "2. Ensure all numerical values are properly calculated\n"
            "3. Handle missing or null values appropriately\n"
            "4. Provide meaningful insights based on the data patterns\n"
            "5. Make recommendations actionable and data-driven\n"
            "6. Include relevant statistics for all numerical columns\n"
            "7. Identify time-based trends when temporal data exists\n\n"
            "TABLE DATA TO ANALYZE:"
        )
    }
    
    prompt = default_prompts.get(prompt_name, "")
    if variables and prompt:
        for key, value in variables.items():
            placeholder = f"{{{key}}}"
            prompt = prompt.replace(placeholder, str(value))
    
    return prompt
