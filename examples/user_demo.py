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
from pg_graphql_mcp import list_tables


def demo_available_tables():
    data = json.loads(list_tables())
    if "error" in data:
        print(f"✗ Error: {data['error']}")
        return []
    else:
        print("✓ list_tables tool executed successfully")
        tables = []
        for table in data["tables"]:
            print(f"   • {table['name']} - {table['description']}")
            tables.append(table["name"])
        return tables


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


if __name__ == "__main__":
    print("📝 NOTE: This demo expects a GraphQL server running at")
    print("         http://127.0.0.1:3001/rpc/graphql")
    print("         Network errors are normal if no server is running.")
    print()

    # 1. First discover available tables
    available_tables = demo_available_tables()

    # 2. Demo based on available tables
    if "account" in available_tables:
        demo_account_queries()

    if "blog" in available_tables or "blogPost" in available_tables:
        demo_blog_queries()

    print("\n=== Demo Complete ===")
    print("✅ Has shown actually available database tables and query functionality")
