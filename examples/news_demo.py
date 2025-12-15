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
from pg_graphql_mcp import graphql_query, execute_collection_query, list_tables


def demo_news_mcp_tools():
    """Demo of news query functionality"""

    print("=== PostgreSQL GraphQL MCP - News Demo ===")

    # 1. Get latest news
    print("1. Get latest 3 news items:")

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
          }}
        }}
        """

    # Example: Build news query
    news_fields = ["id", "title", "url", "source", "time"]
    news_query = build_collection_query("news", news_fields, first=3)

    try:
        result = json.loads(graphql_query(query=news_query))
        if "error" in result:
            print(f"✗ graphql_query tool failed: {result['error']}")
        else:
            print("✓ graphql_query tool executed successfully")

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

    # 2. Use execute_collection_query tool for pagination query
    print("\n2. Use execute_collection_query tool:")

    try:
        result = json.loads(execute_collection_query("news", first=5))
        if "error" in result:
            error_msg = result["error"]
            print(f"✗ Error: {error_msg}")
        else:
            print("✓ execute_collection_query tool executed successfully")

        collection = result["data"]["newsCollection"]

        if not collection["edges"]:
            print("✓ No records found")
        else:
            print(f"✓ Current page has {len(collection['edges'])} records")
            print(f"✓ First Cursor: {collection['edges'][0]['cursor']}")
            print(f"✓ Last Cursor: {collection['edges'][-1]['cursor']}")

        if not collection["pageInfo"]:
            print("✓ Has no next page")
        else:
            print(f"✓ Has next page: {collection['pageInfo']['hasNextPage']}")

    except Exception as e:
        print(f"✗ Pagination query failed: {str(e)}")


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
                        if keyword.lower() in node["title"].lower():
                            filtered_news.append(node)

                    if filtered_news:
                        print(f"\nFound {len(filtered_news)} related news:")
                        for i, news in enumerate(
                            filtered_news[:10], 1
                        ):  # Show first 10
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
    demo_news_mcp_tools()

    # Ask whether to start interactive mode
    try:
        print("\n" + "=" * 50)
        print("📝 NOTE: The demos above show expected network errors")
        print("   because no GraphQL server is running at the endpoint.")
        print("   To test with actual data, start a GraphQL server")
        print("   at http://127.0.0.1:3001/rpc/graphql")
        print("=" * 50)

        response = input("\nStart interactive mode? (y/n): ").strip().lower()
        if response == "y":
            interactive_news_query()
        else:
            print("\nProgram ended")
    except (KeyboardInterrupt, EOFError):
        print("\nProgram ended")
