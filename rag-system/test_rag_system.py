import requests
import json

def test_rag_system():
    """Test the RAG system with various questions"""
    
    base_url = "http://localhost:8000"
    
    test_questions = [
        "What are the fees for Computer Science Engineering at JECRC College?",
        "Which departments are available at JECRC College?", 
        "Tell me about JECRC College facilities",
        "What is the admission process for B.Tech at JECRC?",
        "What are the placement statistics for JECRC College?"
    ]
    
    print("🧪 Testing JECRC College RAG System")
    print("=" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n❓ Question {i}: {question}")
        print("-" * 40)
        
        try:
            response = requests.post(
                f"{base_url}/chat", 
                json={"query": question},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('response', 'No response')
                print(f"🤖 Answer: {answer}")
                
                # Check if the answer contains relevant keywords
                relevant_keywords = ['JECRC', 'college', 'engineering', 'fee', 'department', 'admission']
                found_keywords = [kw for kw in relevant_keywords if kw.lower() in answer.lower()]
                print(f"✅ Found keywords: {found_keywords}")
                
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
        
        print("-" * 40)
    
    print("\n🎯 RAG System Test Complete!")

if __name__ == "__main__":
    test_rag_system()