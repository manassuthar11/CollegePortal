import os
from simple_rag import load_documents, simple_search, documents

# Test the document loading
print("Testing document loading...")
result = load_documents()
print(f"Load result: {result}")

print(f"\nDocuments loaded: {len(documents)}")
for doc_name, content in documents.items():
    print(f"- {doc_name}: {len(content)} characters")
    print(f"  Preview: {content[:100]}...")

# Test search functionality
print("\n" + "="*50)
print("Testing search...")

test_queries = [
    "what is the fee of first year",
    "name of the college", 
    "how many departments",
    "what facilities are available"
]

for query in test_queries:
    print(f"\nQuery: {query}")
    results = simple_search(query, documents)
    if results:
        for result in results:
            print(f"Answer: {result}")
    else:
        print("No results found")