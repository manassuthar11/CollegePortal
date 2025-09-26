/**
 * Language Detection and Processing Utilities
 * Handles multilingual support for Hindi, English, and Rajasthani
 */

import { franc } from 'franc';
import { SupportedLanguage, ILanguageDetectionResult } from '../types';

// Language detection patterns and keywords
const languagePatterns = {
  [SupportedLanguage.HINDI]: {
    keywords: [
      'मैं', 'आप', 'क्या', 'कैसे', 'कहाँ', 'कब', 'क्यों', 'है', 'हैं', 'था', 'थे', 'होगा', 'होंगे',
      'नमस्ते', 'धन्यवाद', 'कृपया', 'हाँ', 'नहीं', 'अच्छा', 'बुरा', 'छात्र', 'शिक्षक', 'कॉलेज'
    ],
    script: /[\u0900-\u097F]/g, // Devanagari script range
  },
  [SupportedLanguage.RAJASTHANI]: {
    keywords: [
      'हूँ', 'थारो', 'थारी', 'क्यूं', 'कित्ते', 'राम', 'राम', 'धन्यो', 'म्हारो', 'म्हारी',
      'राजस्थान', 'मारवाड़', 'जैसलमेर', 'जोधपुर', 'उदयपुर', 'भाषा', 'बोली'
    ],
    script: /[\u0900-\u097F]/g, // Devanagari script (same as Hindi)
  },
  [SupportedLanguage.ENGLISH]: {
    keywords: [
      'hello', 'hi', 'thank', 'please', 'yes', 'no', 'good', 'bad', 'student', 'teacher', 'college',
      'what', 'where', 'when', 'why', 'how', 'who', 'which', 'can', 'will', 'would', 'should'
    ],
    script: /[a-zA-Z]/g, // Latin script
  },
};

/**
 * Detect language of input text using keyword matching and script detection
 */
export const detectLanguage = (text: string): ILanguageDetectionResult => {
  if (!text || text.trim().length === 0) {
    return {
      language: SupportedLanguage.ENGLISH,
      confidence: 0.5,
    };
  }

  const cleanText = text.toLowerCase().trim();
  
  // Use franc for basic detection
  try {
    const detectedCode = franc(text);
    
    // Enhanced scoring with franc results
    let francBonus: { [key in SupportedLanguage]: number } = {
      [SupportedLanguage.ENGLISH]: detectedCode === 'eng' ? 0.4 : 0,
      [SupportedLanguage.HINDI]: detectedCode === 'hin' ? 0.4 : 0,
      [SupportedLanguage.RAJASTHANI]: 0, // Franc won't detect this, rely on keywords
    };
    
    const scores: { [key in SupportedLanguage]: number } = {
      [SupportedLanguage.ENGLISH]: francBonus[SupportedLanguage.ENGLISH],
      [SupportedLanguage.HINDI]: francBonus[SupportedLanguage.HINDI],
      [SupportedLanguage.RAJASTHANI]: 0,
    };

  // Check for script patterns
  Object.entries(languagePatterns).forEach(([lang, pattern]) => {
    const scriptMatches = (text.match(pattern.script) || []).length;
    scores[lang as SupportedLanguage] += scriptMatches * 0.3;
  });

  // Check for keyword matches
  Object.entries(languagePatterns).forEach(([lang, pattern]) => {
    const keywordMatches = pattern.keywords.filter(keyword => 
      cleanText.includes(keyword.toLowerCase())
    ).length;
    scores[lang as SupportedLanguage] += keywordMatches * 0.7;
  });

  // Find language with highest score
  const sortedScores = Object.entries(scores)
    .sort(([, a], [, b]) => b - a)
    .map(([lang, score]) => ({ 
      language: lang as SupportedLanguage, 
      confidence: Math.min(score / 10, 1) 
    }));

  const primaryResult = sortedScores[0];
  const alternatives = sortedScores.slice(1, 3).filter(result => result.confidence > 0.1);

  // Default to English if confidence is very low
  if (primaryResult.confidence < 0.2) {
    return {
      language: SupportedLanguage.ENGLISH,
      confidence: 0.5,
      alternatives: alternatives.length > 0 ? alternatives : undefined,
    };
  }

  return {
    language: primaryResult.language,
    confidence: primaryResult.confidence,
    alternatives: alternatives.length > 0 ? alternatives : undefined,
  };
  } catch (error) {
    // If franc fails, fall back to keyword matching only
    const scores: { [key in SupportedLanguage]: number } = {
      [SupportedLanguage.ENGLISH]: 0,
      [SupportedLanguage.HINDI]: 0,
      [SupportedLanguage.RAJASTHANI]: 0,
    };
    
    // Check for script patterns and keywords
    Object.entries(languagePatterns).forEach(([lang, pattern]) => {
      const scriptMatches = (text.match(pattern.script) || []).length;
      const keywordMatches = pattern.keywords.filter(keyword => 
        cleanText.includes(keyword.toLowerCase())
      ).length;
      scores[lang as SupportedLanguage] += scriptMatches * 0.3 + keywordMatches * 0.7;
    });
    
    const bestMatch = Object.entries(scores).reduce((a, b) => a[1] > b[1] ? a : b);
    return {
      language: bestMatch[0] as SupportedLanguage,
      confidence: Math.min(bestMatch[1] / 10, 1),
    };
  }
};

/**
 * Get language-specific greeting messages
 */
export const getGreeting = (language: SupportedLanguage): string => {
  const greetings = {
    [SupportedLanguage.ENGLISH]: "Hello! I'm your college assistant. How can I help you today?",
    [SupportedLanguage.HINDI]: "नमस्ते! मैं आपका कॉलेज सहायक हूँ। आज मैं आपकी कैसे सहायता कर सकता हूँ?",
    [SupportedLanguage.RAJASTHANI]: "राम राम! हूँ थारो कॉलेज सहायक। आज म्हे थारी कैसी मदद करणी है?",
  };

  return greetings[language] || greetings[SupportedLanguage.ENGLISH];
};

/**
 * Get language-specific error messages
 */
export const getErrorMessage = (language: SupportedLanguage, errorType: string): string => {
  const errorMessages = {
    [SupportedLanguage.ENGLISH]: {
      general: "I'm sorry, I couldn't understand your question. Could you please rephrase it?",
      noContext: "I don't have enough information to answer that question.",
      technical: "I'm experiencing some technical difficulties. Please try again later.",
    },
    [SupportedLanguage.HINDI]: {
      general: "मुझे खुशी है कि आपने पूछा, लेकिन मैं आपका प्रश्न समझ नहीं सका। कृपया इसे दोबारा पूछें।",
      noContext: "मेरे पास इस प्रश्न का उत्तर देने के लिए पर्याप्त जानकारी नहीं है।",
      technical: "मुझे कुछ तकनीकी समस्याएं आ रही हैं। कृपया बाद में फिर कोशिश करें।",
    },
    [SupportedLanguage.RAJASTHANI]: {
      general: "म्हे खुशी है कि थमने पूछ्यो, पण म्हे थारो सवाल समझ कोनी आयो। कृपया दोबारा पूछो।",
      noContext: "म्हारे कैं इस सवाल को जवाब देवण खातर काफी जाणकारी कोनी है।",
      technical: "म्हे कुछ तकनीकी दिक्कत आवै रही है। कृपया बाद में फिर कोशिश करो।",
    },
  };

  return errorMessages[language]?.[errorType as keyof typeof errorMessages[typeof language]] ||
         errorMessages[SupportedLanguage.ENGLISH]?.general ||
         "I'm sorry, something went wrong.";
};

/**
 * Get language-specific success messages
 */
export const getSuccessMessage = (language: SupportedLanguage, messageType: string): string => {
  const successMessages = {
    [SupportedLanguage.ENGLISH]: {
      helpful: "I'm glad I could help! Is there anything else you'd like to know?",
      complete: "Great! I've provided the information you requested.",
      more: "Would you like more details about this topic?",
    },
    [SupportedLanguage.HINDI]: {
      helpful: "मुझे खुशी है कि मैं आपकी सहायता कर सका! क्या आप कुछ और जानना चाहेंगे?",
      complete: "बहुत बढ़िया! मैंने आपको वह जानकारी दी है जिसकी आपने मांग की थी।",
      more: "क्या आप इस विषय के बारे में और विस्तार से जानना चाहेंगे?",
    },
    [SupportedLanguage.RAJASTHANI]: {
      helpful: "म्हे खुशी है कि म्हे थारी मदद कर सक्यो! के थमे कुछ और जाणणो चावो?",
      complete: "बहुत बढ़िया! म्हैं थमने वा जाणकारी दी है जिसकी थमने मांग की थी।",
      more: "के थमे इस विषय के बारे में और जाणणो चावो?",
    },
  };

  return successMessages[language]?.[messageType as keyof typeof successMessages[typeof language]] ||
         successMessages[SupportedLanguage.ENGLISH]?.helpful ||
         "Thank you for using our service!";
};