# PostgreSQL GraphQL MCP Server

A generic PostgreSQL GraphQL MCP (Model Context Protocol) Server that provides GraphQL access to PostgreSQL databases through HTTP RESTful APIs. This tool acts as a bridge between Claude Code and PostgreSQL databases, enabling database operations without writing specific SQL queries.

## Overview

This project serves as a universal PostgreSQL GraphQL client that exposes database query capabilities as MCP tools. It allows you to perform database exploration, data retrieval, and schema inspection through GraphQL interfaces.

## Key Features

🔗 **Generic GraphQL Queries** - Execute any GraphQL query against your PostgreSQL database
📊 **Table Structure Discovery** - Automatically explore database schemas
🗄️ **Collection Queries** - Query data with pagination support
🔍 **Schema Introspection** - Get complete GraphQL schema information
📋 **Table Listing** - List all available tables/collections
🛠️ **Dynamic Query Building** - Build queries programmatically
⚡ **High Performance** - Uses urllib for efficient HTTP requests
🛡️ **Error Handling** - Comprehensive error handling for network and GraphQL errors

## Architecture

### Core Components
- **GraphQLClient** (`pg_graphql_mcp.py:21`) - HTTP client for GraphQL API communication
- **FastMCP Server** (`pg_graphql_mcp.py:15`) - MCP server implementation
- **MCP Tools** - Multiple tools for different database operations

### Available MCP Tools
- `graphql_query()` - Execute custom GraphQL queries
- `introspection_query()` - Get database schema information
- `list_tables()` - List all available tables
- `get_table_info()` - Get detailed table structure
- `execute_collection_query()` - Generic collection queries with pagination

### Dependencies
- `fastmcp>=0.10.0` - MCP server framework
- `python-dotenv>=1.0.0` - Environment variable management

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pg-graphql-mcp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables (optional):
```bash
cp .env.example .env
# Edit .env file to modify configuration
```

## MCP Tools List

### 1. `graphql_query`
Execute custom GraphQL queries

**Parameters:**
- `query` (required): GraphQL query string
- `variables` (optional): JSON format variables string
- `operation_name` (optional): Operation name

**Example:**
```graphql
{
  tableNameCollection(first: 10) {
    edges {
      node {
        id
        field1
        field2
      }
    }
  }
}
```

### 2. `introspection_query`
Get GraphQL schema information

**Parameters:**
- None

### 3. `list_tables`
List all available tables/collections

**Parameters:**
- None

### 4. `get_table_info`
Get detailed information for a specific table

**Parameters:**
- `table_name` (required): Table name

### 5. `execute_collection_query`
Execute collection query (generic query method)

**Parameters:**
- `collection_name` (required): Collection/table name
- `first` (optional): Number of records to return, default 10
- `after` (optional): Cursor pagination parameter
- `where` (optional): GraphQL where condition
- `order_by` (optional): Sorting condition

## Usage

### Run as MCP Server

```bash
python3 pg_graphql_mcp.py
```

### Configure for Claude Code

Add to your Claude Code configuration file:

```json
{
  "mcpServers": {
    "pg-graphql": {
      "command": "python3",
      "args": ["/path/to/pg-graphql-mcp/pg_graphql_mcp.py"]
    }
  }
}
```

## API Endpoint

Default connection: `http://127.0.0.1:3001/rpc/graphql`

Can be overridden with the `GRAPHQL_ENDPOINT` environment variable.

## Example Queries

### Get Table Data

```graphql
{
  tableNameCollection(first: 10) {
    edges {
      node {
        id
        field1
        field2
        createdAt
      }
    }
    pageInfo {
      hasNextPage
      totalCount
    }
  }
}
```

### Query with Variables

```graphql
query GetTableData($first: Int!, $after: String) {
  tableNameCollection(first: $first, after: $after) {
    edges {
      node {
        id
        field1
        field2
      }
      cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

Variables:
```json
{
  "first": 10,
  "after": "cursor_value"
}
```

## Demo Examples

The project includes multiple demo examples:

- **`examples/news_demo.py`** - News data query demonstration
- **`examples/user_demo.py`** - User data query demonstration

Run demos:
```bash
# News query demo
python3 examples/news_demo.py

# User query demo
python3 examples/user_demo.py
```

## Error Handling

All tools include comprehensive error handling:
- HTTP errors
- GraphQL query errors
- JSON parsing errors
- Network connection errors

Error messages are returned in JSON format with detailed error descriptions.

## Development

### Project Structure

```
pg-graphql-mcp/
├── pg_graphql_mcp.py          # Main MCP server file
├── requirements.txt           # Python dependencies
├── claude_config.json         # Claude Code configuration
├── .env.example              # Environment variable example
├── README.md                 # Project documentation
├── examples/                 # Demo examples
│   ├── news_demo.py         # News data demo
│   └── user_demo.py         # User data demo
└── venv/                     # Virtual environment
```

### How It Works

1. The MCP server starts and registers tools with Claude Code
2. When you use a tool, it sends GraphQL queries to the configured endpoint
3. The GraphQL server (connected to PostgreSQL) processes the query
4. Results are returned as JSON and formatted for display

### Use Cases

This tool is particularly useful for:
- Database exploration and debugging
- Quick data retrieval without writing SQL
- Integration with Claude Code workflows
- Generic database operations across different PostgreSQL setups

### Extending with New Tools

Add new tool functions in `pg_graphql_mcp.py`:

```python
def your_new_tool(param1: str, param2: int) -> str:
    """Tool description"""
    # Implementation logic
    return result

# Register as MCP tool
your_new_tool = mcp.tool()(your_new_tool)
```

## License

MIT License