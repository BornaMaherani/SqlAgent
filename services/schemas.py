from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AnalysisStatistics(BaseModel):
    total_records: Optional[int] = None
    average_value: Optional[float] = None
    max_value: Optional[float] = None
    min_value: Optional[float] = None
    unique_values: Optional[int] = None

class TrendPoint(BaseModel):
    period: str
    value: float
    change_percentage: Optional[float] = None

class AnalysisResult(BaseModel):
    summary: str
    statistics: Optional[AnalysisStatistics] = None
    trends: Optional[List[TrendPoint]] = None
    insights: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None

class TableSchema(BaseModel):
    columns: List[str]
    sample_data: List[Dict[str, Any]]
    data_types: Optional[Dict[str, str]] = None

class AnalysisResponse(BaseModel):
    analysis: AnalysisResult
    table_schema: TableSchema
    raw_data_preview: Optional[List[Dict[str, Any]]] = None
    query_used: Optional[str] = None
