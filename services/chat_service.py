from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import ChatMessage
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from typing import Any, Dict, List, Tuple, Optional
import json
from services.db_service import DBService
from util.helper import print_table
from util.prompt_loader import load_prompt
from services.schemas import AnalysisResponse, AnalysisResult, AnalysisStatistics, TrendPoint, TableSchema


class ChatService:
    def __init__(self, db_service: DBService, api_key: str) -> None:
        self.db_service = db_service
        self.api_key = api_key

    def query_chat(self, llm: ChatOpenAI, db: SQLDatabase, mem_from_db: List[Dict[str, str]], new_message: str) -> Tuple[Any, ConversationBufferMemory, List[str], Dict[str, Any]]:
        """
        Conversation chain to generate SQL queries based on user input.
        Returns the last generated table, conversation memory, and column names.
        """
        # System role prompt (Query Writer mode)
        table_names = db.get_usable_table_names()
        table_infos = db.get_table_info(table_names)
        
        # Load prompt from external file
        query_prompt = load_prompt("query_chat", {
            "table_names": table_names,
            "table_infos": table_infos
        })
        
        system_prompt = SystemMessagePromptTemplate.from_template(query_prompt)
        user_prompt = HumanMessagePromptTemplate.from_template("User Request: {input}")

        # Setup conversation memory
        memory_buffer = ConversationBufferMemory()
        for message in mem_from_db:
            memory_buffer.chat_memory.add_message(ChatMessage(role=message["role"], content=message["content"]))

        # Conversation chain for query writing
        query_chain = SQLDatabaseChain.from_llm(
            llm=llm, db=db,
            prompt=ChatPromptTemplate.from_messages([
                system_prompt,
                user_prompt
            ]),
            memory=memory_buffer,
            verbose=False
        )

        query_string = query_chain.invoke(input=new_message)
        query_results = db._execute(query_string["result"])
        print(query_results)
        first_row = next(iter(query_results))
        column_names = list(first_row.keys())
        return query_results, memory_buffer, column_names, query_string

    def analyse_chat(self, llm: ChatOpenAI, table_data: Any, conversation_history: ConversationBufferMemory, column_names: List[str]) -> AnalysisResponse:
        """
        Conversation chain to analyse database results based on previous query history.
        Returns structured JSON analysis with statistics, trends, and insights.
        """
        # Convert table data to list of dictionaries for processing
        table_data_list = list(table_data)
        
        # Load analysis prompt from external file
        query_history = [msg.content for msg in conversation_history.chat_memory.messages]
        analysis_prompt_text = load_prompt("analysis_chat", {
            "query_history": query_history,
            "column_names": column_names
        })

        # Analysis chain prompt
        analysis_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(analysis_prompt_text),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("TABLE_DATA: {input}")
        ])

        # Independent conversation memory for analysis phase
        analysis_memory = ConversationBufferMemory(memory_key="history", return_messages=True)

        # Create analysis conversation chain
        analysis_chain = ConversationChain(
            llm=llm,
            prompt=analysis_prompt,
            memory=analysis_memory,
            verbose=False
        )

        # Get JSON response from LLM
        json_response = analysis_chain.predict(input=str(table_data_list))
        
        try:
            # First try to parse as clean JSON
            analysis_data = json.loads(json_response.strip())
        except json.JSONDecodeError:
            try:
                # If clean JSON fails, try to extract JSON from text response
                # Look for JSON pattern within the response
                import re
                json_match = re.search(r'\{.*\}', json_response, re.DOTALL)
                if json_match:
                    analysis_data = json.loads(json_match.group())
                else:
                    raise ValueError("No JSON found in response")
            except (json.JSONDecodeError, ValueError):
                # If both methods fail, perform basic analysis locally
                return self._perform_basic_analysis(table_data_list, column_names)
        
        # Handle trend data format mismatch - convert from various formats to period/value format
        if "analysis" in analysis_data and "trends" in analysis_data["analysis"]:
            trends = analysis_data["analysis"]["trends"]
            if trends and isinstance(trends, list) and len(trends) > 0:
                # Check if trends are in the wrong format (missing period/value fields)
                first_trend = trends[0]
                if ("period" not in first_trend or "value" not in first_trend):
                    # Convert from various alternative formats to trend format
                    converted_trends = []
                    for trend in trends:
                        converted_trend = {
                            "period": str(trend.get('rank', trend.get('time_period', trend.get('product', 'N/A')))),
                            "value": float(trend.get('count', trend.get('sales', trend.get('performance_score', 0)))),
                            "change_percentage": trend.get('change_percentage', trend.get('growth', None))
                        }
                        converted_trends.append(converted_trend)
                    analysis_data["analysis"]["trends"] = converted_trends
                # If trends array exists but is empty or malformed, remove it
                elif not isinstance(first_trend, dict):
                    analysis_data["analysis"]["trends"] = None
        
        # Convert to Pydantic model for validation
        return AnalysisResponse(**analysis_data)

    def _perform_basic_analysis(self, table_data: List[Dict[str, Any]], column_names: List[str]) -> AnalysisResponse:
        """Perform basic analysis locally when LLM JSON parsing fails"""
        # Basic statistical analysis
        numeric_columns = []
        for col in column_names:
            if all(isinstance(row.get(col), (int, float)) for row in table_data if row.get(col) is not None):
                numeric_columns.append(col)
        
        statistics = {}
        if numeric_columns:
            for col in numeric_columns:
                values = [row[col] for row in table_data if row.get(col) is not None]
                if values:
                    statistics[col] = {
                        "average": sum(values) / len(values),
                        "min": min(values),
                        "max": max(values),
                        "count": len(values)
                    }
        
        # Create basic analysis
        summary = f"Analyzed {len(table_data)} records with {len(column_names)} columns"
        
        insights = []
        if numeric_columns:
            insights.append(f"Found {len(numeric_columns)} numeric columns suitable for statistical analysis")
        if len(table_data) > 100:
            insights.append("Large dataset detected - consider sampling for better performance")
        
        recommendations = [
            "Review data quality and completeness",
            "Consider additional analysis based on specific business questions"
        ]
        
        return AnalysisResponse(
            analysis=AnalysisResult(
                summary=summary,
                statistics=AnalysisStatistics(
                    total_records=len(table_data),
                    average_value=None,
                    max_value=None,
                    min_value=None,
                    unique_values=None
                ),
                insights=insights,
                recommendations=recommendations
            ),
            table_schema=TableSchema(
                columns=column_names,
                sample_data=table_data[:3] if table_data else [],
                data_types={col: "unknown" for col in column_names}
            ),
            raw_data_preview=table_data[:5] if table_data else [],
            query_used="Basic local analysis (LLM JSON format issue)"
        )
