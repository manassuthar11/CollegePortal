"""
Enhanced RAG System - Real Document Based Only
=============================================

This RAG system uses ONLY information extracted from real documents.
No synthetic data, no assumptions, no fabricated responses.

Features:
- Knowledge base built from actual document extraction
- Confidence scoring for responses
- Source attribution for all information
- Clear indication when information is not available
- Honest responses about data limitations

Author: College Portal Team
Date: September 2025
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import re
import json
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class RealDocumentRAG:
    def __init__(self):
        self.knowledge_base = ""
        self.extraction_data = {}
        self.load_real_document_data()
    
    def load_real_document_data(self):
        """Load knowledge base from real document extraction"""
        kb_path = "documents/general/jecrc_college_info.txt"
        json_path = "documents/general/jecrc_extraction_data.json"
        
        # Load knowledge base text
        if os.path.exists(kb_path):
            with open(kb_path, 'r', encoding='utf-8') as f:
                self.knowledge_base = f.read()
            logger.info(f"Loaded knowledge base: {len(self.knowledge_base)} characters")
        else:
            logger.warning(f"Knowledge base not found: {kb_path}")
            self.knowledge_base = self._create_fallback_message()
        
        # Load detailed extraction data
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                self.extraction_data = json.load(f)
            logger.info(f"Loaded extraction data with {len(self.extraction_data.get('raw_pages', {}))} pages")
        else:
            logger.warning(f"Extraction data not found: {json_path}")
            self.extraction_data = {}
    
    def _create_fallback_message(self):
        """Create message when no real data is available"""
        return """
JECRC College Information System - Real Document Mode

⚠️ NOTICE: No extracted document data found.

This system is designed to provide information ONLY from your actual JECRC documents.
Currently, no processed document data is available.

To get real information:
1. Run the document extractor: python real_document_extractor.py
2. This will process your JECRC PDF and extract actual information
3. The system will then provide responses based only on your document content

Why this approach?
✅ No synthetic or fabricated information
✅ Only genuine data from your actual documents
✅ Transparent about data limitations
✅ No misleading responses

Contact JECRC directly for official information:
- Visit their official website
- Call their admissions office
- Request current brochures

This system prioritizes accuracy over convenience.
"""
    
    def search_knowledge_base(self, query):
        """Search the knowledge base for relevant information"""
        if not self.knowledge_base or "No extracted document data found" in self.knowledge_base:
            return {
                'found_information': False,
                'response': self._create_fallback_message(),
                'confidence': 0.0,
                'sources': []
            }
        
        query_lower = query.lower()
        kb_lower = self.knowledge_base.lower()
        
        # Simple relevance scoring
        relevance_score = 0
        matched_sections = []
        sources = []
        
        # Check for direct matches
        if query_lower in kb_lower:
            relevance_score += 0.8
        
        # Check for keyword matches
        query_keywords = re.findall(r'\b\w+\b', query_lower)
        for keyword in query_keywords:
            if len(keyword) > 3 and keyword in kb_lower:
                relevance_score += 0.1
        
        # Find relevant sections
        kb_lines = self.knowledge_base.split('\n')
        relevant_lines = []
        
        for i, line in enumerate(kb_lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in query_keywords):
                # Include context around the matching line
                start = max(0, i - 2)
                end = min(len(kb_lines), i + 3)
                context = '\n'.join(kb_lines[start:end])
                relevant_lines.append(context)
                
                # Track sources (page numbers if mentioned)
                page_matches = re.findall(r'page\s+(\d+)', line_lower)
                sources.extend(page_matches)
        
        if relevant_lines:
            response = self._format_response(query, relevant_lines, sources)
            return {
                'found_information': True,
                'response': response,
                'confidence': min(relevance_score, 1.0),
                'sources': list(set(sources))
            }
        else:
            return self._handle_no_match(query)
    
    def _format_response(self, query, relevant_sections, sources):
        """Format the response based on extracted information"""
        response = f"Based on the information extracted from your JECRC document:\n\n"
        
        # Combine relevant sections
        combined_info = '\n---\n'.join(relevant_sections)
        response += combined_info
        
        # Add source attribution
        if sources:
            response += f"\n\n📄 Information found on pages: {', '.join(set(sources))}"
        
        response += f"\n\n⚠️ IMPORTANT: This information is extracted directly from your provided PDF document. For the most current and complete information, please verify with JECRC directly."
        
        return response
    
    def _handle_no_match(self, query):
        """Handle cases where no relevant information is found"""
        return {
            'found_information': False,
            'response': f"""I couldn't find specific information about "{query}" in the extracted document content.

This could be because:
• The information isn't present in the provided PDF
• It might be in a format that wasn't successfully extracted (images, complex tables)
• The query might be about information not covered in the document

Available information categories in the extracted data:
{self._get_available_categories()}

For complete and current information about "{query}", I recommend:
1. Contacting JECRC directly
2. Visiting their official website
3. Requesting updated brochures

This system only provides information that was successfully extracted from your documents to ensure accuracy.""",
            'confidence': 0.0,
            'sources': []
        }
    
    def _get_available_categories(self):
        """Get list of available information categories"""
        categories = []
        
        if self.extraction_data:
            fee_count = len(self.extraction_data.get('fee_information', []))
            if fee_count > 0:
                categories.append(f"• Fee Information ({fee_count} instances)")
            
            program_count = len(self.extraction_data.get('academic_programs', []))
            if program_count > 0:
                categories.append(f"• Academic Programs ({program_count} found)")
            
            contact_count = len(self.extraction_data.get('contact_details', []))
            if contact_count > 0:
                categories.append(f"• Contact Information ({contact_count} details)")
            
            placement_count = len(self.extraction_data.get('placement_info', []))
            if placement_count > 0:
                categories.append(f"• Placement Information ({placement_count} references)")
        
        return '\n'.join(categories) if categories else "• Limited information was extractable from the document"

# Initialize RAG system
rag_system = RealDocumentRAG()

# HTML template for the web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JECRC Real Document RAG System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.2em;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .status-badge {
            display: inline-block;
            background: #27ae60;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-top: 15px;
        }
        
        .warning-badge {
            background: #e74c3c;
        }
        
        .chat-container {
            padding: 30px;
        }
        
        .query-form {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .query-input {
            flex: 1;
            padding: 15px;
            border: 2px solid #ecf0f1;
            border-radius: 10px;
            font-size: 1.1em;
            outline: none;
            transition: border-color 0.3s;
        }
        
        .query-input:focus {
            border-color: #3498db;
        }
        
        .query-btn {
            padding: 15px 25px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: bold;
            transition: background 0.3s;
        }
        
        .query-btn:hover {
            background: #2980b9;
        }
        
        .response-area {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            margin-top: 20px;
            min-height: 150px;
            border-left: 5px solid #3498db;
        }
        
        .response-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            font-size: 0.9em;
            color: #7f8c8d;
        }
        
        .confidence-score {
            background: #ecf0f1;
            padding: 5px 12px;
            border-radius: 15px;
        }
        
        .high-confidence { background: #d5f4e6; color: #27ae60; }
        .medium-confidence { background: #fff3cd; color: #856404; }
        .low-confidence { background: #f8d7da; color: #721c24; }
        
        .sample-queries {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            margin-top: 30px;
        }
        
        .sample-queries h3 {
            margin-bottom: 15px;
            color: #2c3e50;
        }
        
        .sample-query {
            background: white;
            padding: 10px 15px;
            margin: 8px 0;
            border-radius: 8px;
            cursor: pointer;
            border: 1px solid #ecf0f1;
            transition: all 0.3s;
        }
        
        .sample-query:hover {
            background: #e8f4f8;
            border-color: #3498db;
        }
        
        .disclaimer {
            background: #fffbf0;
            border: 1px solid #ffd93d;
            border-radius: 10px;
            padding: 20px;
            margin-top: 30px;
        }
        
        .disclaimer h4 {
            color: #8b6914;
            margin-bottom: 10px;
        }
        
        .disclaimer p {
            color: #856404;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 JECRC Real Document RAG</h1>
            <p>Honest AI responses from your actual documents</p>
            <div class="status-badge" id="statusBadge">
                📄 Real Document Mode Active
            </div>
        </div>
        
        <div class="chat-container">
            <div class="query-form">
                <input type="text" class="query-input" id="queryInput" placeholder="Ask about JECRC College (e.g., 'fees', 'programs', 'contact')" maxlength="200">
                <button class="query-btn" onclick="askQuestion()">Ask</button>
            </div>
            
            <div class="response-area" id="responseArea">
                <div class="response-meta">
                    <span>💡 Ready to answer questions from your extracted document data</span>
                </div>
                <p>Enter a question above to get information from your JECRC document. The system will only provide information that was successfully extracted from your actual PDF.</p>
            </div>
            
            <div class="sample-queries">
                <h3>💭 Try asking about:</h3>
                <div class="sample-query" onclick="setQuery('What are the fees?')">What are the fees?</div>
                <div class="sample-query" onclick="setQuery('What programs are available?')">What programs are available?</div>
                <div class="sample-query" onclick="setQuery('Contact information')">Contact information</div>
                <div class="sample-query" onclick="setQuery('Placement details')">Placement details</div>
                <div class="sample-query" onclick="setQuery('Hostel facilities')">Hostel facilities</div>
            </div>
            
            <div class="disclaimer">
                <h4>🔍 Transparency Notice</h4>
                <p>This system provides information ONLY from your extracted JECRC document. No synthetic data is generated. If information seems incomplete, it reflects what was extractable from your PDF, ensuring complete honesty and accuracy.</p>
            </div>
        </div>
    </div>

    <script>
        function setQuery(query) {
            document.getElementById('queryInput').value = query;
        }
        
        function getConfidenceClass(confidence) {
            if (confidence >= 0.7) return 'high-confidence';
            if (confidence >= 0.4) return 'medium-confidence';
            return 'low-confidence';
        }
        
        function getConfidenceText(confidence) {
            const percentage = Math.round(confidence * 100);
            if (confidence >= 0.7) return `High Confidence (${percentage}%)`;
            if (confidence >= 0.4) return `Medium Confidence (${percentage}%)`;
            return `Low Confidence (${percentage}%)`;
        }
        
        async function askQuestion() {
            const query = document.getElementById('queryInput').value.trim();
            if (!query) return;
            
            const responseArea = document.getElementById('responseArea');
            responseArea.innerHTML = `
                <div class="response-meta">
                    <span>🔍 Searching extracted document data...</span>
                </div>
                <p>Processing your question...</p>
            `;
            
            try {
                const response = await fetch('/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query })
                });
                
                const result = await response.json();
                
                const confidenceClass = getConfidenceClass(result.confidence);
                const confidenceText = getConfidenceText(result.confidence);
                
                responseArea.innerHTML = `
                    <div class="response-meta">
                        <span>${result.found_information ? '✅ Information found' : '❌ Limited information available'}</span>
                        <span class="confidence-score ${confidenceClass}">${confidenceText}</span>
                    </div>
                    <div style="white-space: pre-line; line-height: 1.8;">${result.response}</div>
                `;
                
            } catch (error) {
                responseArea.innerHTML = `
                    <div class="response-meta">
                        <span>❌ Error occurred</span>
                    </div>
                    <p>Sorry, there was an error processing your request. Please try again.</p>
                `;
            }
        }
        
        // Allow Enter key to submit
        document.getElementById('queryInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                askQuestion();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    """Main web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/search', methods=['POST'])
def search():
    """Handle search requests"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'found_information': False,
                'response': 'Please enter a question.',
                'confidence': 0.0,
                'sources': []
            })
        
        # Log the query
        logger.info(f"Query received: {query}")
        
        # Search the knowledge base
        result = rag_system.search_knowledge_base(query)
        
        # Log the result
        logger.info(f"Query result - Found: {result['found_information']}, Confidence: {result['confidence']:.2f}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing search: {e}")
        return jsonify({
            'found_information': False,
            'response': 'An error occurred while processing your request.',
            'confidence': 0.0,
            'sources': []
        }), 500

@app.route('/reload', methods=['POST'])
def reload_data():
    """Reload document data"""
    try:
        rag_system.load_real_document_data()
        return jsonify({
            'success': True,
            'message': 'Document data reloaded successfully.',
            'kb_length': len(rag_system.knowledge_base)
        })
    except Exception as e:
        logger.error(f"Error reloading data: {e}")
        return jsonify({
            'success': False,
            'message': f'Error reloading data: {str(e)}'
        }), 500

@app.route('/status')
def status():
    """Get system status"""
    return jsonify({
        'system': 'JECRC Real Document RAG',
        'mode': 'Real Document Only',
        'knowledge_base_size': len(rag_system.knowledge_base),
        'extraction_data_available': bool(rag_system.extraction_data),
        'pages_in_data': len(rag_system.extraction_data.get('raw_pages', {})),
        'fee_info_count': len(rag_system.extraction_data.get('fee_information', [])),
        'program_count': len(rag_system.extraction_data.get('academic_programs', [])),
        'contact_count': len(rag_system.extraction_data.get('contact_details', [])),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting JECRC Real Document RAG System")
    print("=" * 60)
    print("🎯 This system provides ONLY real information from your documents")
    print("❌ No synthetic data • No assumptions • No fabrication")
    print("✅ Only genuine extracted content from your JECRC PDF")
    print("=" * 60)
    print(f"📊 Knowledge base loaded: {len(rag_system.knowledge_base)} characters")
    print(f"📁 Extraction data: {'Available' if rag_system.extraction_data else 'Not found'}")
    
    if rag_system.extraction_data:
        print(f"📄 Pages processed: {len(rag_system.extraction_data.get('raw_pages', {}))}")
        print(f"💰 Fee information: {len(rag_system.extraction_data.get('fee_information', []))} instances")
        print(f"🎓 Programs found: {len(rag_system.extraction_data.get('academic_programs', []))}")
        print(f"📞 Contact details: {len(rag_system.extraction_data.get('contact_details', []))}")
    
    print("=" * 60)
    print("🌐 Access at: http://localhost:8000")
    print("🔄 To update data: Run real_document_extractor.py first")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=8000, debug=False)