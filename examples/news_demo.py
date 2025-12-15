#!/usr/bin/env python3
"""
PostgreSQL GraphQL MCP Tool - News Demo Example
Shows how to use generic tools to query news data
"""

import json
import sys
import os

# Add parent directory to path to import main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pg_graphql_mcp import GraphQLClient

def demo_news_queries():
    """Demo of news query functionality"""
    client = GraphQLClient()

    print("=== PostgreSQL GraphQL MCP - News Demo ===")
    print("Use generic tools to query news data\n")

    # 1. Get latest news
    print("1. Get latest 3 news items:")
    query = """
    {
      newsCollection(first: 3) {
        edges {
          node {
            id
            title
            url
            source
            time
            createdAt
            updatedAt
          }
        }
      }
    }
    """

    try:
        result = client.execute_query(query=query)
        edges = result["data"]["newsCollection"]["edges"]

        print(f"✓ Successfully retrieved {len(edges)} news items:\n")

        for i, edge in enumerate(edges, 1):
            node = edge["node"]
            print(f"{i}. 📰 {node['title']}")
            print(f"   🔗 Link: {node['url']}")
            print(f"   📰 Source: {node['source']}")
            print(f"   ⏰ Time: {node['time']}")
            print()

    except Exception as e:
        print(f"✗ Query failed: {str(e)}")

    # 2. Get total news count
    print("2. Get total news count:")
    count_query = """
    {
      newsCollection {
        totalCount
      }
    }
    """

    try:
        result = client.execute_query(query=count_query)
        total = result["data"]["newsCollection"]["totalCount"]
        print(f"✓ Total {total} news items in database")

    except Exception as e:
        print(f"✗ Query failed: {str(e)}")

    # 3. Pagination query example
    print("\n3. Pagination query example:")
    pagination_query = """
    {
      newsCollection(first: 5) {
        edges {
          node {
            id
            title
            source
          }
        }
        pageInfo {
          hasNextPage
          hasPreviousPage
          startCursor
          endCursor
        }
        totalCount
      }
    }
    """

    try:
        result = client.execute_query(query=pagination_query)
        collection = result["data"]["newsCollection"]

        print(f"✓ Current page: {len(collection['edges'])} records")
        print(f"✓ Total: {collection['totalCount']}")
        print(f"✓ Has next page: {collection['pageInfo']['hasNextPage']}")

    except Exception as e:
        print(f"✗ Pagination query failed: {str(e)}")

    # 4. Demo client-side search
    print("\n4. Search functionality demo (client-side filtering):")
    search_keyword = "economy"
    search_query = """
    {
      newsCollection(first: 50) {
        edges {
          node {
            id
            title
            source
            time
          }
        }
      }
    }
    """

    try:
        result = client.execute_query(query=search_query)
        edges = result["data"]["newsCollection"]["edges"]

        # Client-side filtering
        filtered_news = []
        for edge in edges:
            node = edge["node"]
            if search_keyword.lower() in node['title'].lower():
                filtered_news.append(node)

        if filtered_news:
            print(f"✓ Found {len(filtered_news)} news items about '{search_keyword}':")
            for news in filtered_news[:5]:  # Show first 5
                print(f"   • {news['title']} ({news['source']})")
        else:
            print(f"✗ No news found about '{search_keyword}'")

    except Exception as e:
        print(f"✗ Search failed: {str(e)}")


def demo_custom_queries():
    """Demo of custom queries"""
    print("\n\n=== Custom Query Demo ===")

    # Custom query: Get specific fields
    print("1. Custom field selection:")
    custom_query = """
    {
      newsCollection(first: 5) {
        edges {
          node {
            id
            title
            source
          }
        }
      }
    }
    """

    try:
        client = GraphQLClient()
        result = client.execute_query(query=custom_query)

        print("✓ Custom query successful:")
        for edge in result["data"]["newsCollection"]["edges"]:
            node = edge["node"]
            print(f"   ID: {node['id']}, Title: {node['title']}, Source: {node['source']}")

    except Exception as e:
        print(f"✗ Custom query failed: {str(e)}")


def demo_mcp_tools():
    """Demo how to use MCP tool functions"""
    print("\n\n=== MCP Tool Functions Usage Demo ===")

    try:
        # Import MCP tool functions
        from pg_graphql_mcp import graphql_query, execute_collection_query, list_tables

        # 1. Use generic query tool
        print("1. Use graphql_query tool:")
        query = """
        {
          newsCollection(first: 3) {
            edges {
              node {
                id
                title
              }
            }
          }
        }
        """

        data = json.loads(graphql_query(query=query))
        if "error" in data:
            print(f"✗ Error: {data['error']}")
        else:
            print("✓ graphql_query tool executed successfully")

        # 2. Use collection query tool
        print("\n2. Use execute_collection_query tool:")
        data = json.loads(execute_collection_query("news", first=3))
        if "error" in data:
            print(f"✗ Error: {data['error']}")
        else:
            print("✓ execute_collection_query tool executed successfully")

        # 3. List all tables
        print("\n3. Use list_tables tool:")
        data = json.loads(list_tables())
        if "error" in data:
            print(f"✗ Error: {data['error']}")
        else:
            print("✓ list_tables tool executed successfully")

    except ImportError:
        print("⚠️ MCP tool functions not available, please ensure running in correct environment")
    except Exception as e:
        print(f"✗ MCP tool demo failed: {str(e)}")


def interactive_news_query():
    """Interactive news query"""
    print("\n\n=== Interactive News Query ===")
    print("Type 'quit' to exit")

    client = GraphQLClient()

    while True:
        try:
            print("\nPlease select an operation:")
            print("1. Get latest news")
            print("2. Get news by count")
            print("3. Search news")
            print("4. Exit")

            choice = input("\nPlease enter choice (1-4): ").strip()

            if choice == "1":
                print("\nGetting latest 5 news items...")
                query = """
                {
                  newsCollection(first: 5) {
                    edges {
                      node {
                        id
                        title
                        url
                        source
                        time
                      }
                    }
                  }
                }
                """

                result = client.execute_query(query=query)
                edges = result["data"]["newsCollection"]["edges"]

                print(f"\nRetrieved {len(edges)} news items:")
                for i, edge in enumerate(edges, 1):
                    node = edge["node"]
                    print(f"{i}. {node['title']}")
                    print(f"   Source: {node['source']} | Time: {node['time']}")
                    print()

            elif choice == "2":
                count = input("Please enter number of news items to get: ").strip()
                if count.isdigit():
                    count = int(count)
                    query = f"""
                    {{
                      newsCollection(first: {count}) {{
                        edges {{
                          node {{
                            id
                            title
                            url
                            source
                            time
                          }}
                        }}
                      }}
                    }}
                    """

                    result = client.execute_query(query=query)
                    edges = result["data"]["newsCollection"]["edges"]

                    print(f"\nRetrieved {len(edges)} news items:")
                    for i, edge in enumerate(edges, 1):
                        node = edge["node"]
                        print(f"{i}. {node['title']}")
                        print(f"   Source: {node['source']} | Time: {node['time']}")
                        print()
                else:
                    print("Please enter a valid number")

            elif choice == "3":
                keyword = input("Please enter search keyword: ").strip()
                if keyword:
                    print(f"\nSearching for news containing '{keyword}'...")
                    query = """
                    {
                      newsCollection(first: 100) {
                        edges {
                          node {
                            id
                            title
                            url
                            source
                            time
                          }
                        }
                      }
                    }
                    """

                    result = client.execute_query(query=query)
                    edges = result["data"]["newsCollection"]["edges"]

                    # Client-side filtering
                    filtered_news = []
                    for edge in edges:
                        node = edge["node"]
                        if keyword.lower() in node['title'].lower():
                            filtered_news.append(node)

                    if filtered_news:
                        print(f"\nFound {len(filtered_news)} related news:")
                        for i, news in enumerate(filtered_news[:10], 1):  # Show first 10
                            print(f"{i}. {news['title']}")
                            print(f"   Source: {news['source']} | Time: {news['time']}")
                            print()
                    else:
                        print(f"No news found containing '{keyword}'")

            elif choice == "4":
                print("Exit")
                break

            else:
                print("Invalid choice, please try again")

        except KeyboardInterrupt:
            print("\n\nExit")
            break
        except Exception as e:
            print(f"\nOperation failed: {str(e)}")


if __name__ == "__main__":
    # Run all demos
    demo_news_queries()
    demo_custom_queries()
    demo_mcp_tools()

    # Ask whether to start interactive mode
    try:
        response = input("\nStart interactive mode? (y/n): ").strip().lower()
        if response == 'y':
            interactive_news_query()
        else:
            print("\nProgram ended")
    except KeyboardInterrupt:
        print("\nProgram ended")