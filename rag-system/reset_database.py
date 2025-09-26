"""
JECRC Foundation RAG System - Database Reset Utility

This utility helps you:
1. Clear the existing vector database
2. Remove cached document data  
3. Force reprocessing of all documents
4. Useful when you add/remove/update documents

Usage: python reset_database.py
"""

import os
import shutil
import pickle
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def reset_database():
    """Reset the RAG system database and cache"""
    
    print("🔄 JECRC RAG System - Database Reset Utility")
    print("=" * 50)
    
    # Paths to clear
    vector_db_path = "advanced_jecrc_vectordb"
    cache_file = "document_cache.pkl"
    log_file = "rag_system.log"
    
    items_removed = 0
    
    # Remove vector database
    if os.path.exists(vector_db_path):
        try:
            shutil.rmtree(vector_db_path)
            print(f"✅ Removed vector database: {vector_db_path}")
            items_removed += 1
        except Exception as e:
            print(f"❌ Error removing vector database: {e}")
    else:
        print(f"ℹ️  Vector database not found: {vector_db_path}")
    
    # Remove cache file
    if os.path.exists(cache_file):
        try:
            os.remove(cache_file)
            print(f"✅ Removed cache file: {cache_file}")
            items_removed += 1
        except Exception as e:
            print(f"❌ Error removing cache file: {e}")
    else:
        print(f"ℹ️  Cache file not found: {cache_file}")
    
    # Clear log file (optional)
    clear_logs = input("\n🗂️  Clear log file? (y/n): ").lower().strip()
    if clear_logs == 'y' and os.path.exists(log_file):
        try:
            os.remove(log_file)
            print(f"✅ Removed log file: {log_file}")
            items_removed += 1
        except Exception as e:
            print(f"❌ Error removing log file: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    if items_removed > 0:
        print(f"🎉 Database reset complete! Removed {items_removed} items.")
        print("\n📋 Next Steps:")
        print("1. Add your documents to the documents/ folders")
        print("2. Run: python smart_rag_app.py")
        print("3. The system will automatically process your documents")
    else:
        print("ℹ️  No database files found to remove.")
        print("The system appears to be already clean.")
    
    print("\n📁 Document folders available:")
    print("   📂 documents/admissions/")
    print("   📂 documents/courses/")
    print("   📂 documents/fees/")
    print("   📂 documents/general/")
    print("   📂 documents/hostel/")
    print("   📂 documents/placement/")
    print("   📂 documents/forms/")
    
    # Check if documents exist
    documents_path = Path("documents")
    if documents_path.exists():
        total_files = 0
        for category in ["admissions", "courses", "fees", "general", "hostel", "placement", "forms"]:
            category_path = documents_path / category
            if category_path.exists():
                files = list(category_path.glob("*.*"))
                pdf_files = list(category_path.glob("*.pdf"))
                docx_files = list(category_path.glob("*.docx"))
                txt_files = list(category_path.glob("*.txt"))
                
                supported_files = pdf_files + docx_files + txt_files
                if supported_files:
                    print(f"   └── {category}/: {len(supported_files)} files ready for processing")
                    total_files += len(supported_files)
        
        if total_files > 0:
            print(f"\n📊 Total {total_files} documents ready for processing!")
        else:
            print(f"\n📝 No documents found. Please add PDF, DOCX, or TXT files to the category folders.")
    
    print(f"\n🚀 Ready to start the RAG system with fresh database!")

if __name__ == "__main__":
    try:
        reset_database()
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logger.error(f"Reset database error: {e}")
    
    input(f"\nPress Enter to exit...")