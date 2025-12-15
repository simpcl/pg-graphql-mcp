#!/usr/bin/env python3
"""
PostgreSQL GraphQL MCP Tool - User Demo Example
Shows how to query user data (assuming users table exists)
"""

import json
import sys
import os

# Add parent directory to path to import main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pg_graphql_mcp import GraphQLClient

def demo_available_tables():
    """Demo of actually available table query functionality"""
    client = GraphQLClient()

    print("=== PostgreSQL GraphQL MCP - Available Tables Demo ===")
    print("Query actually existing tables in database\n")

    # 1. First check what tables are available
    print("1. Discover available tables:")
    introspection_query = """
    {
      __schema {
        queryType {
          fields {
            name
            type {
              name
              kind
              ofType {
                name
                kind
              }
            }
          }
        }
      }
    }
    """

    try:
        result = client.execute_query(query=introspection_query)

        if "data" in result and "__schema" in result["data"]:
            fields = result["data"]["__schema"]["queryType"]["fields"]
            collections = []

            for field in fields:
                field_name = field["name"]
                field_type = field["type"]

                # Check if field name ends with Collection
                if field_name.endswith("Collection"):
                    collections.append(field_name)
                # Or check if type name contains Connection
                elif field_type.get("name") and "Connection" in field_type["name"]:
                    collections.append(field_name)

            print(f"✓ Found {len(collections)} collections:")
            for collection in sorted(collections):
                print(f"   • {collection}")

            return collections

    except Exception as e:
        print(f"✗ Table check failed: {str(e)}")
        return []


def demo_account_queries():
    """Demo of account query functionality"""
    client = GraphQLClient()

    print("\n=== PostgreSQL GraphQL MCP - Account Demo ===")
    print("Use generic tools to query account data\n")

    # 1. Get all accounts
    print("1. Get account list:")
    query = """
    {
      accountCollection(first: 10) {
        edges {
          node {
            id
          }
        }
      }
    }
    """

    try:
        result = client.execute_query(query=query)

        # Check if accountCollection exists
        if "data" in result and "accountCollection" in result["data"]:
            collection = result["data"]["accountCollection"]
            edges = collection["edges"]

            print(f"✓ Successfully retrieved {len(edges)} accounts:")

            for i, edge in enumerate(edges, 1):
                node = edge["node"]
                print(f"{i}. Account ID: {node['id']}")
            print()
        else:
            print("ℹ️  account table does not exist or no access permission")

    except Exception as e:
        print(f"✗ Query failed: {str(e)}")


def demo_blog_queries():
    """Demo of blog query functionality"""
    client = GraphQLClient()

    print("\n=== PostgreSQL GraphQL MCP - Blog Demo ===")
    print("Use generic tools to query blog data\n")

    # 1. Get blog list
    print("1. Get blog list:")
    query = """
    {
      blogCollection(first: 5) {
        edges {
          node {
            id
          }
        }
      }
    }
    """

    try:
        result = client.execute_query(query=query)

        if "data" in result and "blogCollection" in result["data"]:
            collection = result["data"]["blogCollection"]
            edges = collection["edges"]

            print(f"✓ Successfully retrieved {len(edges)} blogs:")

            for i, edge in enumerate(edges, 1):
                node = edge["node"]
                print(f"{i}. Blog ID: {node['id']}")
            print()
        else:
            print("ℹ️  blog table does not exist or no access permission")

    except Exception as e:
        print(f"✗ Query failed: {str(e)}")

    # 2. Get blog posts
    print("2. Get blog posts:")
    query = """
    {
      blogPostCollection(first: 5) {
        edges {
          node {
            id
          }
        }
      }
    }
    """

    try:
        result = client.execute_query(query=query)

        if "data" in result and "blogPostCollection" in result["data"]:
            collection = result["data"]["blogPostCollection"]
            edges = collection["edges"]

            print(f"✓ Successfully retrieved {len(edges)} blog posts:")

            for i, edge in enumerate(edges, 1):
                node = edge["node"]
                print(f"{i}. Post ID: {node['id']}")
            print()
        else:
            print("ℹ️  blogPost table does not exist or no access permission")

    except Exception as e:
        print(f"✗ Query failed: {str(e)}")


def demo_query_builder():
    """Demo of query builder functionality"""
    print("\n\n=== Query Builder Demo ===")

    # Demo how to dynamically build queries
    def build_collection_query(collection_name, fields, first=10):
        """Dynamically build collection query"""
        fields_str = "\n        ".join(fields)
        return f"""
        query Get{collection_name.capitalize()} {{
          {collection_name}Collection(first: {first}) {{
            edges {{
              node {{
                {fields_str}
              }}
            }}
            totalCount
          }}
        }}
        """

    client = GraphQLClient()

    # Example: Build news query
    news_fields = ["id", "title", "source", "time"]
    news_query = build_collection_query("news", news_fields, first=3)

    print("1. Dynamically built news query:")
    try:
        result = client.execute_query(query=news_query)
        if "data" in result and "newsCollection" in result["data"]:
            edges = result["data"]["newsCollection"]["edges"]
            print(f"✓ Query successful, got {len(edges)} records")

            for edge in edges:
                node = edge["node"]
                title = node.get('title', 'N/A')
                source = node.get('source', 'N/A')
                print(f"   • {title} ({source})")
        else:
            print("✗ Query did not return expected results")

    except Exception as e:
        print(f"✗ Query failed: {str(e)}")


def demo_error_handling():
    """Demo of error handling"""
    print("\n\n=== Error Handling Demo ===")

    client = GraphQLClient()

    # 1. Invalid GraphQL query
    print("1. Test invalid query:")
    invalid_query = """
    {
      invalidTableCollection {
        edges {
          node {
            id
          }
        }
      }
    }
    """

    try:
        result = client.execute_query(query=invalid_query)
        print("✗ Unexpected success")
    except Exception as e:
        print(f"✓ Correctly caught error: {str(e)[:100]}...")

    # 2. Network error test (using invalid endpoint)
    print("\n2. Test network error:")
    invalid_client = GraphQLClient("http://127.0.0.1:9999/invalid")

    try:
        result = invalid_client.execute_query(query="{ __typename }")
        print("✗ Unexpected success")
    except Exception as e:
        print(f"✓ Correctly caught network error: {str(e)[:100]}...")


if __name__ == "__main__":
    # 1. First discover available tables
    available_tables = demo_available_tables()

    # 2. Demo based on available tables
    if "accountCollection" in available_tables:
        demo_account_queries()

    if "blogCollection" in available_tables or "blogPostCollection" in available_tables:
        demo_blog_queries()

    # 3. Other demos
    demo_query_builder()
    demo_error_handling()

    print("\n=== Demo Complete ===")
    print("✅ Has shown actually available database tables and query functionality")