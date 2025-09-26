/**
 * RAG (Retrieval-Augmented Generation) Implementation
 * Handles document retrieval and context-aware response generation
 */

import { HfInference } from '@huggingface/inference';
import { SupportedLanguage, IRAGResult, IDocumentChunk } from '../types';
import { detectLanguage, getErrorMessage } from './languageUtils';

// Initialize Hugging Face client
const hf = new HfInference(process.env.HUGGINGFACE_API_KEY);

// Sample college-related document chunks (in a real implementation, this would come from ChromaDB)
const collegeDocuments: IDocumentChunk[] = [
  // English documents
  {
    id: 'admission-en',
    content: 'College admission process requires completion of application form, submission of academic transcripts, and entrance exam scores. The admission committee reviews applications based on merit and availability of seats.',
    metadata: {
      source: 'admission-guidelines',
      language: SupportedLanguage.ENGLISH,
      category: 'admission',
      lastUpdated: new Date('2024-01-15'),
    },
  },
  {
    id: 'fees-en',
    content: 'Annual tuition fees are $5000 for undergraduate programs and $7000 for graduate programs. Payment can be made in installments. Scholarships are available for meritorious students.',
    metadata: {
      source: 'fee-structure',
      language: SupportedLanguage.ENGLISH,
      category: 'fees',
      lastUpdated: new Date('2024-02-01'),
    },
  },
  {
    id: 'library-en',
    content: 'The college library is open from 8 AM to 10 PM on weekdays and 9 AM to 6 PM on weekends. Students can borrow up to 5 books at a time. Digital resources are available 24/7.',
    metadata: {
      source: 'library-rules',
      language: SupportedLanguage.ENGLISH,
      category: 'facilities',
      lastUpdated: new Date('2024-01-20'),
    },
  },
  // Hindi documents
  {
    id: 'admission-hi',
    content: 'कॉलेज में प्रवेश के लिए आवेदन पत्र भरना, शैक्षणिक प्रमाण पत्र जमा करना और प्रवेश परीक्षा के अंक आवश्यक हैं। प्रवेश समिति योग्यता और सीटों की उपलब्धता के आधार पर आवेदनों की समीक्षा करती है।',
    metadata: {
      source: 'admission-guidelines-hindi',
      language: SupportedLanguage.HINDI,
      category: 'admission',
      lastUpdated: new Date('2024-01-15'),
    },
  },
  {
    id: 'fees-hi',
    content: 'स्नातक कार्यक्रमों के लिए वार्षिक शिक्षा शुल्क ₹50,000 और स्नातकोत्तर कार्यक्रमों के लिए ₹70,000 है। भुगतान किश्तों में किया जा सकता है। मेधावी छात्रों के लिए छात्रवृत्ति उपलब्ध है।',
    metadata: {
      source: 'fee-structure-hindi',
      language: SupportedLanguage.HINDI,
      category: 'fees',
      lastUpdated: new Date('2024-02-01'),
    },
  },
  // Rajasthani documents
  {
    id: 'library-raj',
    content: 'कॉलेज री लाइब्रेरी सोमवार सूं शुक्रवार सवेरे 8 बजे सूं रात 10 बजे तक अर शनिवार-रविवार सवेरे 9 बजे सूं शाम 6 बजे तक खुली रैवै है। छात्र एक बारी मैं 5 किताबां ले सकै हैं।',
    metadata: {
      source: 'library-rules-rajasthani',
      language: SupportedLanguage.RAJASTHANI,
      category: 'facilities',
      lastUpdated: new Date('2024-01-20'),
    },
  },
];

/**
 * Perform semantic search on document chunks
 */
const searchDocuments = async (query: string, language: SupportedLanguage): Promise<IDocumentChunk[]> => {
  try {
    // Filter documents by language first
    const languageSpecificDocs = collegeDocuments.filter(
      doc => doc.metadata.language === language
    );

    // If no documents in the detected language, fall back to English
    const searchDocs = languageSpecificDocs.length > 0 
      ? languageSpecificDocs 
      : collegeDocuments.filter(doc => doc.metadata.language === SupportedLanguage.ENGLISH);

    // Simple keyword-based search (in a real implementation, use vector similarity)
    const queryWords = query.toLowerCase().split(/\s+/);
    const scoredDocs = searchDocs.map(doc => {
      const contentWords = doc.content.toLowerCase();
      const score = queryWords.reduce((acc, word) => {
        return acc + (contentWords.includes(word) ? 1 : 0);
      }, 0);
      
      return { doc, score };
    });

    // Return top 3 most relevant documents
    return scoredDocs
      .filter(item => item.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 3)
      .map(item => item.doc);

  } catch (error) {
    console.error('Error in document search:', error);
    return [];
  }
};

/**
 * Generate response using retrieved context
 */
const generateContextualResponse = async (
  query: string,
  context: string[],
  language: SupportedLanguage
): Promise<string> => {
  try {
    // Create a context-aware prompt
    const contextText = context.join('\n\n');
    const prompt = `Context: ${contextText}\n\nQuestion: ${query}\n\nAnswer:`;

    // Use Hugging Face for text generation (fallback to simple response if API unavailable)
    try {
      const response = await hf.textGeneration({
        model: 'microsoft/DialoGPT-medium',
        inputs: prompt,
        parameters: {
          max_length: 200,
          temperature: 0.7,
          top_p: 0.9,
        },
      });

      return response.generated_text || generateFallbackResponse(query, context, language);
    } catch (apiError) {
      console.warn('Hugging Face API unavailable, using fallback response');
      return generateFallbackResponse(query, context, language);
    }

  } catch (error) {
    console.error('Error generating response:', error);
    return getErrorMessage(language, 'technical');
  }
};

/**
 * Generate fallback response when API is unavailable
 */
const generateFallbackResponse = (query: string, context: string[], language: SupportedLanguage): string => {
  if (context.length === 0) {
    return getErrorMessage(language, 'noContext');
  }

  // Simple template-based response generation
  const contextSummary = context[0]; // Use the most relevant context
  
  const responses = {
    [SupportedLanguage.ENGLISH]: `Based on the information I have: ${contextSummary}`,
    [SupportedLanguage.HINDI]: `उपलब्ध जानकारी के आधार पर: ${contextSummary}`,
    [SupportedLanguage.RAJASTHANI]: `उपलब्ध जाणकारी के आधार पर: ${contextSummary}`,
  };

  return responses[language] || responses[SupportedLanguage.ENGLISH];
};

/**
 * Main RAG function - combines retrieval and generation
 */
export const processRAGQuery = async (query: string, userLanguage?: SupportedLanguage): Promise<IRAGResult> => {
  const startTime = Date.now();

  try {
    // Detect language if not provided
    const detectedLanguage = userLanguage || detectLanguage(query).language;

    // Search for relevant documents
    const relevantDocs = await searchDocuments(query, detectedLanguage);

    if (relevantDocs.length === 0) {
      return {
        answer: getErrorMessage(detectedLanguage, 'noContext'),
        context: [],
        confidence: 0.1,
        sources: [],
        language: detectedLanguage,
      };
    }

    // Extract context from documents
    const context = relevantDocs.map(doc => doc.content);
    const sources = relevantDocs.map(doc => doc.metadata.source);

    // Generate response
    const answer = await generateContextualResponse(query, context, detectedLanguage);

    // Calculate confidence based on context relevance
    const confidence = Math.min(0.3 + (relevantDocs.length * 0.2), 0.9);

    const responseTime = Date.now() - startTime;
    console.log(`RAG query processed in ${responseTime}ms for language: ${detectedLanguage}`);

    return {
      answer,
      context,
      confidence,
      sources,
      language: detectedLanguage,
    };

  } catch (error) {
    console.error('Error in RAG processing:', error);
    const fallbackLanguage = userLanguage || SupportedLanguage.ENGLISH;
    
    return {
      answer: getErrorMessage(fallbackLanguage, 'technical'),
      context: [],
      confidence: 0.1,
      sources: [],
      language: fallbackLanguage,
    };
  }
};

/**
 * Add new document to the knowledge base (simulate ChromaDB insertion)
 */
export const addDocument = (document: Omit<IDocumentChunk, 'id'>): string => {
  const id = `doc-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  const newDoc: IDocumentChunk = {
    ...document,
    id,
  };
  
  collegeDocuments.push(newDoc);
  console.log(`Added new document with ID: ${id}`);
  
  return id;
};

/**
 * Get statistics about the document collection
 */
export const getDocumentStats = () => {
  const stats = {
    totalDocuments: collegeDocuments.length,
    byLanguage: {
      [SupportedLanguage.ENGLISH]: collegeDocuments.filter(doc => doc.metadata.language === SupportedLanguage.ENGLISH).length,
      [SupportedLanguage.HINDI]: collegeDocuments.filter(doc => doc.metadata.language === SupportedLanguage.HINDI).length,
      [SupportedLanguage.RAJASTHANI]: collegeDocuments.filter(doc => doc.metadata.language === SupportedLanguage.RAJASTHANI).length,
    },
    byCategory: collegeDocuments.reduce((acc, doc) => {
      acc[doc.metadata.category] = (acc[doc.metadata.category] || 0) + 1;
      return acc;
    }, {} as Record<string, number>),
  };

  return stats;
};