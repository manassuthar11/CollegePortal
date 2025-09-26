"""
JECRC Foundation College Portal - Smart RAG Chatbot
Advanced Retrieval-Augmented Generation System

This is the main Flask application for the RAG chatbot system that provides
intelligent responses about college information using document-based knowledge.

Architecture:
- Vector Database (ChromaDB) for semantic search
- Hybrid Search (Semantic + Keyword matching)
- Multi-Model AI Pipeline with Hugging Face
- Context-Aware Response Generation
- Document Processing Pipeline

Author: College Portal Team
Version: 1.0.0
"""

import os
import re
import pickle
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import warnings
warnings.filterwarnings("ignore")

# Core Flask and web libraries
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

# AI and ML libraries
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Document processing libraries
import PyPDF2
from docx import Document as DocxDocument
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rag_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SmartRAGChatbot:
    """
    Advanced RAG Chatbot System for JECRC Foundation
    
    Features:
    - Document ingestion and preprocessing
    - Vector embeddings with SentenceTransformers
    - Hybrid search (semantic + keyword)
    - Context-aware response generation
    - Multi-document synthesis
    """
    
    def __init__(self, documents_path: str = "documents", cache_file: str = "document_cache.pkl"):
        """Initialize the RAG chatbot system"""
        self.documents_path = documents_path
        self.cache_file = cache_file
        self.vector_db_path = "advanced_jecrc_vectordb"
        
        # Initialize AI models
        logger.info("🤖 Initializing AI models...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize QA pipeline with DistilBERT
        self.qa_pipeline = pipeline(
            "question-answering",
            model="distilbert-base-cased-distilled-squad",
            tokenizer="distilbert-base-cased-distilled-squad"
        )
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=self.vector_db_path)
        try:
            self.collection = self.chroma_client.get_collection("jecrc_knowledge_base")
            logger.info("📚 Loaded existing knowledge base")
        except:
            self.collection = self.chroma_client.create_collection("jecrc_knowledge_base")
            logger.info("🆕 Created new knowledge base")
        
        # Initialize TF-IDF for keyword search
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 3)
        )
        
        # Document storage
        self.documents = []
        self.document_metadata = []
        self.tfidf_matrix = None
        
        # Load or process documents
        self.load_or_process_documents()
        
        logger.info("✅ RAG Chatbot initialized successfully!")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF files"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return self.clean_text(text)
        except Exception as e:
            logger.error(f"❌ Error extracting PDF {pdf_path}: {e}")
            return ""
    
    def extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text from Word documents"""
        try:
            doc = DocxDocument(docx_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return self.clean_text(text)
        except Exception as e:
            logger.error(f"❌ Error extracting DOCX {docx_path}: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        
        # Remove special characters and artifacts from PDF extraction
        text = re.sub(r'[^\w\s\.,!?;:()\-\n]', '', text)
        
        return text.strip()
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Smart text chunking with sentence awareness"""
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = ""
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence.split())
            
            if current_size + sentence_size <= chunk_size:
                current_chunk += " " + sentence if current_chunk else sentence
                current_size += sentence_size
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                # Handle overlap
                if overlap > 0 and chunks:
                    overlap_text = " ".join(chunks[-1].split()[-overlap:])
                    current_chunk = overlap_text + " " + sentence
                    current_size = len(current_chunk.split())
                else:
                    current_chunk = sentence
                    current_size = sentence_size
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return [chunk for chunk in chunks if len(chunk.strip()) > 20]
    
    def process_documents(self) -> None:
        """Process all documents in the documents folder"""
        logger.info("📁 Processing documents...")
        
        if not os.path.exists(self.documents_path):
            os.makedirs(self.documents_path)
            logger.info(f"📂 Created documents directory: {self.documents_path}")
            return
        
        all_documents = []
        all_metadata = []
        
        # Process documents by category
        categories = ['admissions', 'courses', 'fees', 'general', 'hostel', 'placement', 'forms']
        
        for category in categories:
            category_path = os.path.join(self.documents_path, category)
            if os.path.exists(category_path):
                for filename in os.listdir(category_path):
                    if filename.lower().endswith(('.pdf', '.docx', '.txt')):
                        file_path = os.path.join(category_path, filename)
                        logger.info(f"📖 Processing: {filename}")
                        
                        # Extract text based on file type
                        if filename.lower().endswith('.pdf'):
                            text = self.extract_text_from_pdf(file_path)
                        elif filename.lower().endswith('.docx'):
                            text = self.extract_text_from_docx(file_path)
                        else:  # .txt files
                            with open(file_path, 'r', encoding='utf-8') as f:
                                text = self.clean_text(f.read())
                        
                        if text.strip():
                            # Chunk the document
                            chunks = self.chunk_text(text)
                            
                            for i, chunk in enumerate(chunks):
                                all_documents.append(chunk)
                                all_metadata.append({
                                    'filename': filename,
                                    'category': category,
                                    'chunk_id': i,
                                    'file_path': file_path,
                                    'processed_date': datetime.now().isoformat()
                                })
        
        self.documents = all_documents
        self.document_metadata = all_metadata
        
        logger.info(f"📊 Processed {len(self.documents)} document chunks from {len(set(m['filename'] for m in self.document_metadata))} files")
        
        # Generate embeddings and store in vector database
        if self.documents:
            self.update_vector_database()
            self.update_tfidf_index()
            self.save_cache()
    
    def update_vector_database(self) -> None:
        """Update ChromaDB with document embeddings"""
        logger.info("🧠 Generating embeddings...")
        
        # Clear existing collection
        try:
            self.chroma_client.delete_collection("jecrc_knowledge_base")
            self.collection = self.chroma_client.create_collection("jecrc_knowledge_base")
        except:
            pass
        
        # Generate embeddings in batches
        batch_size = 50
        for i in range(0, len(self.documents), batch_size):
            batch_docs = self.documents[i:i+batch_size]
            batch_metadata = self.document_metadata[i:i+batch_size]
            batch_ids = [f"doc_{j}" for j in range(i, min(i+batch_size, len(self.documents)))]
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(batch_docs).tolist()
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=batch_docs,
                metadatas=batch_metadata,
                ids=batch_ids
            )
            
            logger.info(f"📝 Added batch {i//batch_size + 1}/{(len(self.documents)-1)//batch_size + 1}")
    
    def update_tfidf_index(self) -> None:
        """Update TF-IDF index for keyword search"""
        logger.info("🔍 Building keyword search index...")
        if self.documents:
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.documents)
    
    def save_cache(self) -> None:
        """Save processed documents to cache"""
        cache_data = {
            'documents': self.documents,
            'document_metadata': self.document_metadata,
            'tfidf_vectorizer': self.tfidf_vectorizer,
            'processed_date': datetime.now().isoformat()
        }
        
        with open(self.cache_file, 'wb') as f:
            pickle.dump(cache_data, f)
        
        logger.info(f"💾 Saved cache to {self.cache_file}")
    
    def load_cache(self) -> bool:
        """Load processed documents from cache"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                
                self.documents = cache_data['documents']
                self.document_metadata = cache_data['document_metadata']
                self.tfidf_vectorizer = cache_data['tfidf_vectorizer']
                
                if self.documents:
                    self.tfidf_matrix = self.tfidf_vectorizer.transform(self.documents)
                
                logger.info(f"📁 Loaded {len(self.documents)} documents from cache")
                return True
            except Exception as e:
                logger.error(f"❌ Error loading cache: {e}")
                return False
        return False
    
    def load_or_process_documents(self) -> None:
        """Load from cache or process documents if cache doesn't exist"""
        if not self.load_cache():
            self.process_documents()
    
    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Perform semantic search using vector embeddings"""
        if not self.documents:
            return []
        
        # Query the vector database
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        search_results = []
        if results['documents'][0]:
            for i, (doc, metadata, distance) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )):
                search_results.append({
                    'content': doc,
                    'metadata': metadata,
                    'semantic_score': 1 - distance,  # Convert distance to similarity
                    'search_type': 'semantic'
                })
        
        return search_results
    
    def keyword_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Perform keyword search using TF-IDF"""
        if not self.documents or self.tfidf_matrix is None:
            return []
        
        # Vectorize query
        query_vector = self.tfidf_vectorizer.transform([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Get top results
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        search_results = []
        for idx in top_indices:
            if similarities[idx] > 0:
                search_results.append({
                    'content': self.documents[idx],
                    'metadata': self.document_metadata[idx],
                    'keyword_score': float(similarities[idx]),
                    'search_type': 'keyword'
                })
        
        return search_results
    
    def hybrid_search(self, query: str, top_k: int = 10) -> List[Dict]:
        """Combine semantic and keyword search with hybrid scoring"""
        semantic_results = self.semantic_search(query, top_k)
        keyword_results = self.keyword_search(query, top_k)
        
        # Combine results
        all_results = {}
        
        # Add semantic results
        for result in semantic_results:
            doc_key = result['content'][:100]  # Use first 100 chars as key
            all_results[doc_key] = result
            all_results[doc_key]['hybrid_score'] = result['semantic_score'] * 0.7
        
        # Add keyword results and boost hybrid score
        for result in keyword_results:
            doc_key = result['content'][:100]
            if doc_key in all_results:
                # Boost score for documents found in both searches
                all_results[doc_key]['hybrid_score'] += result['keyword_score'] * 0.3
                all_results[doc_key]['search_type'] = 'hybrid'
            else:
                all_results[doc_key] = result
                all_results[doc_key]['hybrid_score'] = result['keyword_score'] * 0.3
        
        # Sort by hybrid score
        sorted_results = sorted(
            all_results.values(), 
            key=lambda x: x.get('hybrid_score', 0), 
            reverse=True
        )
        
        return sorted_results[:top_k//2]  # Return top half for response generation
    
    def generate_response(self, query: str, context_docs: List[Dict]) -> Dict:
        """Generate context-aware response using retrieved documents"""
        if not context_docs:
            return {
                'answer': "I don't have specific information about that topic in my knowledge base. Could you please rephrase your question or ask about admissions, courses, fees, hostel, or placement information?",
                'confidence': 0.0,
                'sources': []
            }
        
        # Prepare context from top documents
        context_text = " ".join([doc['content'] for doc in context_docs[:3]])
        
        # Limit context length for the model
        max_context_length = 1000
        if len(context_text) > max_context_length:
            context_text = context_text[:max_context_length] + "..."
        
        try:
            # Generate answer using QA pipeline
            qa_result = self.qa_pipeline(question=query, context=context_text)
            
            answer = qa_result['answer']
            confidence = qa_result['score']
            
            # Enhance answer with additional context if confidence is low
            if confidence < 0.5:
                # Provide more comprehensive response
                categories = set(doc['metadata']['category'] for doc in context_docs)
                if categories:
                    category_info = ", ".join(categories)
                    answer += f"\n\nThis information is related to: {category_info}"
            
            # Collect source information
            sources = []
            seen_files = set()
            for doc in context_docs[:3]:
                filename = doc['metadata']['filename']
                if filename not in seen_files:
                    sources.append({
                        'filename': filename,
                        'category': doc['metadata']['category'],
                        'relevance_score': doc.get('hybrid_score', 0)
                    })
                    seen_files.add(filename)
            
            return {
                'answer': answer,
                'confidence': confidence,
                'sources': sources,
                'context_used': len(context_docs)
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            return {
                'answer': f"I found some relevant information, but I'm having trouble processing it right now. The information seems to be related to {context_docs[0]['metadata']['category']} from {context_docs[0]['metadata']['filename']}.",
                'confidence': 0.3,
                'sources': [{'filename': doc['metadata']['filename'], 'category': doc['metadata']['category']} for doc in context_docs[:2]]
            }
    
    def chat(self, query: str) -> Dict:
        """Main chat interface"""
        logger.info(f"💬 Query: {query}")
        
        # Perform hybrid search
        relevant_docs = self.hybrid_search(query)
        
        # Generate response
        response = self.generate_response(query, relevant_docs)
        
        logger.info(f"🎯 Response confidence: {response['confidence']:.2f}")
        
        return response
    
    def get_stats(self) -> Dict:
        """Get system statistics"""
        return {
            'total_documents': len(set(m['filename'] for m in self.document_metadata)),
            'total_chunks': len(self.documents),
            'categories': len(set(m['category'] for m in self.document_metadata)),
            'vector_db_size': self.collection.count() if self.collection else 0,
            'last_processed': max([m['processed_date'] for m in self.document_metadata]) if self.document_metadata else None
        }

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Enable CORS for all routes

# Initialize RAG chatbot
rag_chatbot = SmartRAGChatbot()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'JECRC RAG Chatbot',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing message in request',
                'status': 'error'
            }), 400
        
        query = data['message'].strip()
        if not query:
            return jsonify({
                'error': 'Empty message',
                'status': 'error'
            }), 400
        
        # Generate response
        response = rag_chatbot.chat(query)
        
        return jsonify({
            'response': response['answer'],
            'confidence': response['confidence'],
            'sources': response['sources'],
            'context_used': response.get('context_used', 0),
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"❌ Chat endpoint error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error'
        }), 500

@app.route('/stats', methods=['GET'])
def stats_endpoint():
    """Get system statistics"""
    try:
        stats = rag_chatbot.get_stats()
        return jsonify({
            'stats': stats,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"❌ Stats endpoint error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error'
        }), 500

@app.route('/reprocess', methods=['POST'])
def reprocess_documents():
    """Reprocess all documents"""
    try:
        logger.info("🔄 Reprocessing documents...")
        rag_chatbot.process_documents()
        stats = rag_chatbot.get_stats()
        
        return jsonify({
            'message': 'Documents reprocessed successfully',
            'stats': stats,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"❌ Reprocess error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error'
        }), 500

@app.route('/', methods=['GET'])
def index():
    """Serve main page"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>JECRC Foundation - Smart RAG Chatbot</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container { 
                max-width: 800px; 
                margin: 20px; 
                background: white; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            .header { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 30px; 
                text-align: center; 
            }
            .header h1 { font-size: 2.5em; margin-bottom: 10px; }
            .header p { font-size: 1.2em; opacity: 0.9; }
            .chat-container { 
                padding: 30px; 
                height: 500px; 
                display: flex; 
                flex-direction: column; 
            }
            .messages { 
                flex-grow: 1; 
                border: 2px solid #f0f0f0; 
                border-radius: 10px; 
                padding: 20px; 
                overflow-y: auto; 
                margin-bottom: 20px;
                background: #fafafa;
            }
            .input-container { 
                display: flex; 
                gap: 10px; 
            }
            input { 
                flex-grow: 1; 
                padding: 15px; 
                border: 2px solid #ddd; 
                border-radius: 25px; 
                font-size: 16px;
                outline: none;
            }
            input:focus { border-color: #667eea; }
            button { 
                padding: 15px 25px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                border: none; 
                border-radius: 25px; 
                cursor: pointer;
                font-size: 16px;
                transition: transform 0.2s;
            }
            button:hover { transform: translateY(-2px); }
            .message { 
                margin-bottom: 15px; 
                padding: 15px; 
                border-radius: 10px; 
                max-width: 80%;
            }
            .user-message { 
                background: #667eea; 
                color: white; 
                margin-left: auto; 
                text-align: right;
            }
            .bot-message { 
                background: #e8f4f8; 
                color: #333; 
                border-left: 4px solid #667eea;
            }
            .confidence { 
                font-size: 0.8em; 
                opacity: 0.7; 
                margin-top: 5px; 
            }
            .sources { 
                font-size: 0.8em; 
                margin-top: 10px; 
                padding-top: 10px; 
                border-top: 1px solid #ddd; 
            }
            .loading { 
                text-align: center; 
                color: #667eea; 
                font-style: italic; 
            }
            .stats { 
                background: #f8f9fa; 
                padding: 20px; 
                border-top: 1px solid #eee; 
                text-align: center; 
                font-size: 0.9em; 
                color: #666; 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1><i class="fas fa-robot"></i> JECRC Smart RAG Chatbot</h1>
                <p>Intelligent College Information Assistant</p>
            </div>
            <div class="chat-container">
                <div class="messages" id="messages">
                    <div class="bot-message message">
                        <strong>🤖 RAG Assistant:</strong> Hello! I'm your intelligent college assistant. I can help you with information about admissions, courses, fees, hostel, placements, and more. Just ask me anything!
                    </div>
                </div>
                <div class="input-container">
                    <input type="text" id="messageInput" placeholder="Ask me about college information..." onkeypress="if(event.key==='Enter') sendMessage()">
                    <button onclick="sendMessage()"><i class="fas fa-paper-plane"></i> Send</button>
                </div>
            </div>
            <div class="stats" id="stats">Loading system stats...</div>
        </div>

        <script>
            // Load stats on page load
            fetch('/stats')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        document.getElementById('stats').innerHTML = `
                            📊 Knowledge Base: ${data.stats.total_documents} documents | 
                            📝 ${data.stats.total_chunks} text chunks | 
                            📂 ${data.stats.categories} categories | 
                            🧠 Vector DB: ${data.stats.vector_db_size} embeddings
                        `;
                    }
                });

            function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                const messagesContainer = document.getElementById('messages');
                
                // Add user message
                messagesContainer.innerHTML += `
                    <div class="user-message message">
                        <strong>👤 You:</strong> ${message}
                    </div>
                `;
                
                // Add loading message
                messagesContainer.innerHTML += `
                    <div class="bot-message message loading" id="loading">
                        🤖 Thinking and searching knowledge base...
                    </div>
                `;
                
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                input.value = '';
                
                // Send request to chatbot
                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').remove();
                    
                    if (data.status === 'success') {
                        let sourcesHtml = '';
                        if (data.sources && data.sources.length > 0) {
                            sourcesHtml = `
                                <div class="sources">
                                    📚 <strong>Sources:</strong> 
                                    ${data.sources.map(s => `${s.filename} (${s.category})`).join(', ')}
                                </div>
                            `;
                        }
                        
                        messagesContainer.innerHTML += `
                            <div class="bot-message message">
                                <strong>🤖 RAG Assistant:</strong> ${data.response}
                                <div class="confidence">
                                    🎯 Confidence: ${(data.confidence * 100).toFixed(1)}% | 
                                    📖 Context: ${data.context_used} chunks used
                                </div>
                                ${sourcesHtml}
                            </div>
                        `;
                    } else {
                        messagesContainer.innerHTML += `
                            <div class="bot-message message">
                                <strong>🤖 RAG Assistant:</strong> Sorry, I encountered an error. Please try again.
                            </div>
                        `;
                    }
                    
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                })
                .catch(error => {
                    document.getElementById('loading').remove();
                    messagesContainer.innerHTML += `
                        <div class="bot-message message">
                            <strong>🤖 RAG Assistant:</strong> Sorry, I'm having trouble connecting. Please check if the server is running.
                        </div>
                    `;
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                });
            }
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("🚀 Starting JECRC Foundation Smart RAG Chatbot")
    print("=" * 60)
    print("🏗  PROJECT ARCHITECTURE")
    print("   System Type: Retrieval-Augmented Generation (RAG) Chatbot")
    print("   Domain: JECRC Foundation College Information")
    print("   Deployment: Local with Web Interface")
    print("   License: Free & Open Source")
    print()
    print("💻 CORE TECHNOLOGIES")
    print("   🐍 Flask - Python web framework")
    print("   🤖 Hugging Face Transformers - AI models")
    print("   🧠 SentenceTransformers - Text embeddings")
    print("   📊 ChromaDB - Vector database")
    print("   📚 NLTK - Natural language processing")
    print("   📄 PyPDF2, python-docx - Document processing")
    print()
    print("🎯 AI COMPONENTS")
    print("   📝 Embedding: all-MiniLM-L6-v2 (384-dim vectors)")
    print("   ❓ QA Model: DistilBERT (SQuAD fine-tuned)")
    print("   🔍 Search: Hybrid (Semantic + Keyword)")
    print("   🧩 Processing: Smart chunking with overlap")
    print()
    print("📁 DOCUMENT CATEGORIES")
    print("   📋 admissions - Admission procedures and requirements")
    print("   📚 courses - Course details and curriculum")
    print("   💰 fees - Fee structure and payment info")
    print("   🏛️ general - General college information")
    print("   🏠 hostel - Accommodation and hostel details")
    print("   💼 placement - Career and placement information")
    print("   📄 forms - Application forms and documents")
    print()
    print("🌐 API ENDPOINTS")
    print("   GET  /health - System health check")
    print("   POST /chat - Main chatbot interface")
    print("   GET  /stats - Knowledge base statistics")
    print("   POST /reprocess - Reprocess all documents")
    print()
    print("🔗 Access URLs:")
    print("   📱 Web Interface: http://localhost:8000")
    print("   📡 API Base: http://localhost:8000")
    print("   🔍 Health Check: http://localhost:8000/health")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=8000, debug=True)