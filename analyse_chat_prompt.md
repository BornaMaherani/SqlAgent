##1. Main Goal
Analyze database query results and provide structured JSON output with statistics, trends, and insights.

##2. Input
- Table data from SQL query results
- Query conversation history
- Column names from the result set

##3. Output
Structured JSON analysis containing statistics, trends, insights, and recommendations

##4. Step-by-step Instruction
1. Examine the provided table data to understand its structure and content
2. Calculate statistical summaries for numerical data (count, averages, min/max, unique values)
3. Identify trends for time-based data if temporal columns exist
4. Generate meaningful insights based on data patterns and relationships
5. Create actionable recommendations based on the analysis
6. Extract sample data for preview purposes
7. Format all analysis results into the specified JSON structure
8. Return only valid JSON without any additional text or formatting

##5. Constraints
- Return ONLY valid JSON - no additional text, no markdown, no code blocks
- Ensure all numerical values are properly calculated
- Handle missing or null values appropriately
- Provide meaningful insights based on the data patterns
- Make recommendations actionable and data-driven
- Include relevant statistics for all numerical columns
- Identify time-based trends when temporal data exists
- Follow the exact JSON response format specified

##6. Output Format
Valid JSON following this exact structure:
{{
  "analysis": {{
    "summary": "comprehensive analysis summary",
    "statistics": {{
      "total_records": 100,
      "average_value": 250.5,
      "max_value": 1000,
      "min_value": 10,
      "unique_values": 25
    }},
    "trends": [
      {{"period": "2024-01", "value": 1200, "change_percentage": 10.5}},
      {{"period": "2024-02", "value": 1450, "change_percentage": 20.8}}
    ],
    "insights": ["insight 1", "insight 2"],
    "recommendations": ["recommendation 1", "recommendation 2"]
  }},
  "table_schema": {{
    "columns": ["col1", "col2"],
    "sample_data": [{{"col1": "value1", "col2": "value2"}}],
    "data_types": {{"col1": "string", "col2": "number"}}
  }},
  "raw_data_preview": [{{"col1": "value1", "col2": "value2"}}],
  "query_used": "SELECT * FROM table"
}}



DATABASE CONTEXT:
Query History: {query_history}
Table Columns: {column_names}
