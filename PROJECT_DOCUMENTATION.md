# Langchain Database Chatbot API - Project Documentation

## 📖 Overview

This project is a FastAPI-based application that provides a conversational interface for database query generation and analysis using Langchain. The system allows users to interact with databases using natural language, generating SQL queries and providing structured analysis of the results.

## 🏗️ Architecture

### Project Structure
```
langchain-database-chatbot/
├── api/                    # API package with versioning support
│   ├── __init__.py
│   └── v1/                 # API version 1
│       ├── __init__.py
│       ├── schemas.py      # API request/response schemas
│       ├── dependencies.py # Service factory dependencies
│       └── routers/        # Endpoint routers
│           ├── __init__.py
│           ├── sessions.py # Session management endpoints
│           ├── messages.py # Message retrieval endpoints
│           └── chat.py     # Chat processing endpoints
├── services/               # Business logic services
│   ├── __init__.py
│   ├── schemas.py          # Analysis output schemas
│   ├── db_service.py       # Database service
│   ├── session_service.py  # Session management
│   ├── message_service.py  # Message handling
│   └── chat_service.py     # Chat processing logic
├── util/                   # Utility functions
│   ├── __init__.py
│   ├── helper.py           # Helper functions
│   └── prompt_loader.py    # Prompt loading system
├── templates/              # Frontend templates
│   └── index.html          # Main interface
├── tests/                  # Test files
│   └── test_main.py        # Main test suite
├── main.py                 # FastAPI application entry point
├── run.py                  # Application runner script
├── database.py             # Database configuration
├── models.py               # SQLAlchemy models
├── config.py               # Application configuration
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables
```

## 🔧 API Endpoints

### Version 1 (v1) API

#### Session Management
- `POST /sessions` - Create a new session
- `GET /sessions/{sess_id}/info` - Get session information
- `PUT /sessions/{sess_id}` - Update a session
- `DELETE /sessions/{sess_id}` - Delete a session

#### Message Management
- `GET /sessions/{sess_id}/messages` - Get all messages for a session

#### Chat Processing
- `POST /sessions/{sess_id}` - Process chat message and return analysis

#### Frontend
- `GET /` - Serve the frontend interface

## 📊 Data Models

### API Schemas (api/v1/schemas.py)
- `SessionCreate` - Request schema for creating sessions
- `SessionUpdate` - Request schema for updating sessions  
- `ChatRequest` - Request schema for chat messages
- `SessionResponse` - Response schema for sessions
- `MessageResponse` - Response schema for messages
- `ErrorResponse` - Error response schema

### Service Schemas (services/schemas.py)
- `AnalysisStatistics` - Statistical analysis results
- `TrendPoint` - Time-based trend data points
- `AnalysisResult` - Comprehensive analysis results
- `TableSchema` - Table structure information
- `AnalysisResponse` - Complete analysis response

### Database Models (models.py)
- `Sessions` - Session table model
- `Messages` - Message table model

## 🚀 Services

### DBService
- Handles database operations
- Provides CRUD functionality
- Manages database sessions

### SessionService
- Creates, updates, and deletes sessions
- Manages session lifecycle

### MessageService  
- Stores and retrieves messages
- Handles message formatting

### ChatService
- Generates SQL queries from natural language
- Analyzes query results
- Provides structured JSON analysis output

## 🎯 Prompt System

### Prompt Files
- `query_chat_prompt.md` - SQL query generation prompt
- `analyse_chat_prompt.md` - Data analysis prompt

### Prompt Structure
Each prompt follows this format:
1. **Main Goal** - Primary objective
2. **Input** - Required input parameters
3. **Output** - Expected output format
4. **Step-by-step Instruction** - Processing steps
5. **Constraints** - Limitations and rules
6. **Output Format** - Specific format requirements
7. **Few-shot Examples** - Example inputs and outputs

### Prompt Loading
The `prompt_loader.py` handles:
- Loading entire prompt files
- Variable substitution
- Fallback to default prompts
- Error handling

## ⚙️ Configuration

### Environment Variables (.env)
- `API_KEY` - OpenAI API key for LLM access
- Database connection settings
- Application configuration

### Application Settings (config.py)
- Loads environment variables
- Provides settings object
- Configures application behavior

## 🗄️ Database

### SQLite Database
- Uses SQLAlchemy ORM
- Automatic table creation
- Session-based connection management
- Proper relationship handling

### Models
- **Sessions**: session_id, name, date_created
- **Messages**: message_id, session_id, role, content, timestamp

## 🧪 Testing

### Test Structure
- Uses pytest framework
- In-memory SQLite database for testing
- TestClient for API endpoint testing
- Comprehensive coverage of all components

### Running Tests
```bash
python -m pytest tests/ -v
```

## 🏃‍♂️ Running the Application

### Using run.py (Recommended)
```bash
python run.py
```
- Starts uvicorn server with hot reload
- Listens on http://0.0.0.0:8000
- Automatic reload on code changes

### Using main.py
```bash
python main.py
```
- Direct execution
- Requires manual server management

## 🔄 API Versioning

The project is designed with versioning in mind:
- Current version: v1
- Easy to add v2, v3, etc.
- Each version in separate directory
- Maintains backward compatibility

## 📦 Dependencies

### Core Dependencies
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM database access
- **Langchain** - LLM integration
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### Development Dependencies
- **pytest** - Testing framework
- **python-dotenv** - Environment variable management

## 🛠️ Development

### Code Organization
- Clean separation of concerns
- Modular architecture
- Easy to maintain and extend
- Proper error handling

### Best Practices
- Type hints throughout
- Proper documentation
- Error handling and logging
- Input validation
- Security considerations

## 📈 Future Enhancements

### Planned Features
1. **API Versioning**: Add v2 with enhanced features
2. **Authentication**: User authentication and authorization
3. **Rate Limiting**: API rate limiting
4. **Monitoring**: Application performance monitoring
5. **Deployment**: Docker containerization
6. **CI/CD**: Automated testing and deployment

### Technical Improvements
1. **Caching**: Query result caching
2. **Async Operations**: Async database operations
3. **WebSockets**: Real-time communication
4. **Background Tasks**: Async task processing
5. **API Documentation**: Enhanced OpenAPI documentation

## 🆘 Troubleshooting

### Common Issues
1. **Database Connection**: Check database file permissions
2. **API Key**: Ensure OpenAI API key is set in .env
3. **Import Errors**: Check Python path and imports
4. **Port Conflicts**: Change port in run.py if 8000 is busy

### Logging
- Application logs to console
- Error logging implemented
- Debug information available

## 📝 License

This project is designed for educational and development purposes. Please ensure proper licensing for production use.

---

*Last Updated: 2025-09-23*
*Version: 1.0.0*
