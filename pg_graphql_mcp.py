#!/usr/bin/env python3
"""
PostgreSQL GraphQL MCP Tool
Generic PostgreSQL GraphQL API client that accesses database through HTTP RESTful API + GraphQL protocol
"""

import json
import urllib.request
import urllib.error
import os
from typing import Dict, Any, Optional
from fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP("PostgreSQL GraphQL Client")

# GraphQL API Configuration
GRAPHQL_ENDPOINT = os.getenv("GRAPHQL_ENDPOINT", "http://127.0.0.1:3001/rpc/graphql")


class GraphQLClient:
    """PostgreSQL GraphQL API Client"""

    def __init__(self, endpoint: str = GRAPHQL_ENDPOINT):
        self.endpoint = endpoint

    def execute_query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute GraphQL query

        Args:
            query: GraphQL query string
            variables: Query variables
            operation_name: Operation name

        Returns:
            Query result dictionary
        """
        payload = {
            "query": query,
            "variables": variables or {},
            "operationName": operation_name,
        }

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        try:
            # Prepare request data
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.endpoint, data=data, headers=headers, method="POST"
            )

            # Send request
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status != 200:
                    error_data = response.read().decode("utf-8")
                    raise Exception(f"HTTP Error: {response.status} - {error_data}")

                # Parse response
                response_data = response.read().decode("utf-8")
                result = json.loads(response_data)

                # Check GraphQL errors
                if "errors" in result:
                    error_msg = "; ".join(
                        [
                            err.get("message", "Unknown Error")
                            for err in result["errors"]
                        ]
                    )
                    raise Exception(f"GraphQL Error: {error_msg}")

                return result

        except urllib.error.URLError as e:
            raise Exception(f"Network request error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON parsing error: {str(e)}")


# Common MCP Tool Functions


def graphql_query(
    query: str, variables: Optional[str] = None, operation_name: Optional[str] = None
) -> str:
    """
    Execute generic GraphQL query

    Args:
        query: GraphQL query string
        variables: JSON format variables string (optional)
        operation_name: Operation name (optional)

    Returns:
        JSON format query result
    """
    try:
        # Parse variables string
        parsed_variables = None
        if variables and variables.strip():
            try:
                parsed_variables = json.loads(variables)
            except json.JSONDecodeError:
                return json.dumps(
                    {"error": "Variables JSON format error"},
                    ensure_ascii=False,
                    indent=2,
                )

        # Execute query
        client = GraphQLClient()
        result = client.execute_query(
            query=query, variables=parsed_variables, operation_name=operation_name
        )

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)


def introspection_query() -> str:
    """
    Execute GraphQL introspection query to get database schema information

    Returns:
        JSON format GraphQL schema
    """
    query = """
    query IntrospectionQuery {
      __schema {
        queryType { name }
        mutationType { name }
        subscriptionType { name }
        types {
          kind
          name
          description
          fields {
            name
            type {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
    """

    try:
        client = GraphQLClient()
        result = client.execute_query(query=query)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)


def list_tables() -> str:
    """
    List all available tables/collections

    Returns:
        JSON format table list
    """
    query = """
    query ListTables {
      __schema {
        queryType {
          fields {
            name
            description
            type {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
    """

    try:
        client = GraphQLClient()
        result = client.execute_query(query=query)

        # Extract query field names (usually correspond to database tables)
        if "data" in result and "__schema" in result["data"]:
            query_fields = result["data"]["__schema"]["queryType"]["fields"]
            tables = []

            for field in query_fields:
                # Filter out GraphQL built-in fields
                field_name = field["name"]
                if not field_name.startswith("__"):
                    table_name = ""
                    if field_name.endswith("Collection"):
                        table_name = field_name[:-10]
                        tables.append(
                            {
                                "name": table_name,
                                "type": "collection",
                                "description": field.get("description", ""),
                            }
                        )

            return json.dumps(
                {"tables": tables, "total": len(tables)}, ensure_ascii=False, indent=2
            )

        return result

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)


def get_table_info(table_name: str) -> str:
    """
    Get detailed information for a specified table

    Args:
        table_name: Table name

    Returns:
        JSON format table structure information
    """
    # Get field information through introspection query first
    introspection_query_str = f"""
    query GetTableInfo {{
      __type(name: "{table_name}") {{
        kind
        name
        description
        fields {{
          name
          type {{
            kind
            name
            ofType {{
              kind
              name
              ofType {{
                kind
                name
              }}
            }}
          }}
        }}
      }}
    }}
    """

    try:
        client = GraphQLClient()
        result = client.execute_query(query=introspection_query_str)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)


def execute_collection_query(
    collection_name: str,
    first: int = 10,
    after: Optional[str] = None,
    where: Optional[str] = None,
    order_by: Optional[str] = None,
) -> str:
    """
    Execute collection query (generic query method)

    Args:
        collection_name: Collection/table name
        first: Number of records to return (default 10)
        after: Cursor pagination parameter (optional)
        where: GraphQL where condition (optional)
        order_by: Sorting condition (optional)

    Returns:
        JSON format query result
    """
    # Build basic query
    # Note: totalCount may not be supported by all GraphQL schemas
    query = f"""
    query Get{collection_name.capitalize()}Collection($first: Int, $after: String) {{
      {collection_name}Collection(first: $first, after: $after) {{
        edges {{
          node {{
            id
          }}
          cursor
        }}
        pageInfo {{
          hasNextPage
          hasPreviousPage
          endCursor
          startCursor
        }}
      }}
    }}
    """

    variables = {"first": first}
    if after:
        variables["after"] = after

    try:
        client = GraphQLClient()
        result = client.execute_query(query=query, variables=variables)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)


# Register as MCP tools - these will be wrapped but original functions remain available
_mcp_graphql_query = mcp.tool()(graphql_query)
_mcp_introspection_query = mcp.tool()(introspection_query)
_mcp_list_tables = mcp.tool()(list_tables)
_mcp_get_table_info = mcp.tool()(get_table_info)
_mcp_execute_collection_query = mcp.tool()(execute_collection_query)


if __name__ == "__main__":
    # Run MCP server
    mcp.run()
