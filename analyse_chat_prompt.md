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
{
  "analysis": {
    "summary": "comprehensive analysis summary",
    "statistics": {
      "total_records": 100,
      "average_value": 250.5,
      "max_value": 1000,
      "min_value": 10,
      "unique_values": 25
    },
    "trends": [
      {"period": "2024-01", "value": 1200, "change_percentage": 10.5},
      {"period": "2024-02", "value": 1450, "change_percentage": 20.8}
    ],
    "insights": ["insight 1", "insight 2"],
    "recommendations": ["recommendation 1", "recommendation 2"]
  },
  "table_schema": {
    "columns": ["col1", "col2"],
    "sample_data": [{"col1": "value1", "col2": "value2"}],
    "data_types": {"col1": "string", "col2": "number"}
  },
  "raw_data_preview": [{"col1": "value1", "col2": "value2"}],
  "query_used": "SELECT * FROM table"
}

<!-- ##7. Few-shot examples

Example 1:
Input Data: [{"ProductID": 1, "ProductName": "Widget", "Price": 10.99, "Category": "Tools", "Stock": 50}]
Output: {
  "analysis": {
    "summary": "Analyzed product inventory data showing pricing and stock levels",
    "statistics": {
      "total_records": 1,
      "average_value": 10.99,
      "max_value": 10.99,
      "min_value": 10.99,
      "unique_values": 1
    },
    "trends": [],
    "insights": ["Single product in inventory with moderate stock level", "Product priced competitively at $10.99"],
    "recommendations": ["Consider expanding product range in Tools category", "Monitor stock levels to avoid shortages"]
  },
  "table_schema": {
    "columns": ["ProductID", "ProductName", "Price", "Category", "Stock"],
    "sample_data": [{"ProductID": 1, "ProductName": "Widget", "Price": 10.99, "Category": "Tools", "Stock": 50}],
    "data_types": {"ProductID": "integer", "ProductName": "string", "Price": "float", "Category": "string", "Stock": "integer"}
  },
  "raw_data_preview": [{"ProductID": 1, "ProductName": "Widget", "Price": 10.99, "Category": "Tools", "Stock": 50}],
  "query_used": "SELECT * FROM Products WHERE ProductID = 1"
}

Example 2:
Input Data: [{"OrderID": 101, "Customer": "John Doe", "Amount": 150.75, "OrderDate": "2024-01-15"}, {"OrderID": 102, "Customer": "Jane Smith", "Amount": 89.99, "OrderDate": "2024-01-16"}]
Output: {
  "analysis": {
    "summary": "Analyzed order data showing customer purchasing patterns",
    "statistics": {
      "total_records": 2,
      "average_value": 120.37,
      "max_value": 150.75,
      "min_value": 89.99,
      "unique_values": 2
    },
    "trends": [
      {"period": "2024-01-15", "value": 150.75, "change_percentage": 0},
      {"period": "2024-01-16", "value": 89.99, "change_percentage": -40.3}
    ],
    "insights": ["Two orders processed with average value of $120.37", "Significant drop in order value from day 1 to day 2"],
    "recommendations": ["Investigate reasons for value drop between orders", "Consider promotional offers to increase average order value"]
  },
  "table_schema": {
    "columns": ["OrderID", "Customer", "Amount", "OrderDate"],
    "sample_data": [{"OrderID": 101, "Customer": "John Doe", "Amount": 150.75, "OrderDate": "2024-01-15"}],
    "data_types": {"OrderID": "integer", "Customer": "string", "Amount": "float", "OrderDate": "date"}
  },
  "raw_data_preview": [{"OrderID": 101, "Customer": "John Doe", "Amount": 150.75, "OrderDate": "2024-01-15"}, {"OrderID": 102, "Customer": "Jane Smith", "Amount": 89.99, "OrderDate": "2024-01-16"}],
  "query_used": "SELECT OrderID, Customer, Amount, OrderDate FROM Orders WHERE OrderDate >= '2024-01-15'"
} -->

DATABASE CONTEXT:
Query History: {query_history}
Table Columns: {column_names}
