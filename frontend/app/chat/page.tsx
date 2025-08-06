'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { Send, Plus, Menu, X, MessageSquare, User, MoreVertical, FileText, File, Copy, Check, Bot, Upload, PaperclipIcon, LogOut, Database, Zap, ArrowRight, Trash2, Info, Save } from 'lucide-react';
import { apiEndpoints } from '@/lib/api';

interface Session {
  id: string;
  title: string;
  created_at: string;
}

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: string;
}

interface ChatHistoryItem {
  question: string;
  answer: string;
}

interface FileItem {
  file_name: string;
  storage_uri?: string;
  description?: string;
  summary?: string;
  size?: number;
  type?: string;
  upload_time?: string;
  is_active?: boolean;
}

const ChatPage: React.FC = () => {
  const router = useRouter();
  const [sessions, setSessions] = useState<Session[]>([]);
  const [currentSession, setCurrentSession] = useState<Session | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [leftSidebarOpen, setLeftSidebarOpen] = useState(true);
  const [rightSidebarOpen, setRightSidebarOpen] = useState(false);
  const [showNewSessionModal, setShowNewSessionModal] = useState(false);
  const [newSessionName, setNewSessionName] = useState('');
  const [newSessionError, setNewSessionError] = useState('');
  const [files, setFiles] = useState<FileItem[]>([]);
  const [loadingFiles, setLoadingFiles] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadingFile, setUploadingFile] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState('');
  const [fileDescription, setFileDescription] = useState('');
  const [uploadError, setUploadError] = useState('');
  const [settingActiveFile, setSettingActiveFile] = useState<string | null>(null);
  const [activeFile, setActiveFile] = useState<FileItem | null>(null);
  const [sessionActiveFiles, setSessionActiveFiles] = useState<{[sessionId: string]: string | null}>({});
  const [copiedCode, setCopiedCode] = useState<string | null>(null);
  const [streamingMessage, setStreamingMessage] = useState('');
  const [showDeleteSessionModal, setShowDeleteSessionModal] = useState(false);
  const [sessionToDelete, setSessionToDelete] = useState<Session | null>(null);
  const [showDeleteFileModal, setShowDeleteFileModal] = useState(false);
  const [fileToDelete, setFileToDelete] = useState<FileItem | null>(null);
  const [deletingSession, setDeletingSession] = useState(false);
  const [deletingFile, setDeletingFile] = useState(false);
  const [showDatasetInfoTab, setShowDatasetInfoTab] = useState(false);
  const [selectedDatasetInfo, setSelectedDatasetInfo] = useState<FileItem | null>(null);
  const [loadingDatasetInfo, setLoadingDatasetInfo] = useState(false);
  const [savingConversation, setSavingConversation] = useState(false);
  const [saveMessage, setSaveMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // Debug mode for development
  const DEBUG_STREAMING = process.env.NODE_ENV === 'development';

  // Logout function
  const handleLogout = useCallback(() => {
    try {
      // Clear all localStorage data
      localStorage.removeItem('access_token');
      localStorage.removeItem('token_type');
      localStorage.removeItem('activeSessionId');
      localStorage.removeItem('activeSessionTitle');
      
      // Clear all state
      setSessions([]);
      setCurrentSession(null);
      setMessages([]);
      setFiles([]);
      setActiveFile(null);
      setInputMessage('');
      
      // Redirect to login page
      router.push('/login');
    } catch (error) {
      console.error('Error during logout:', error);
      // Fallback to window.location if router fails
      window.location.href = '/login';
    }
  }, [router]);

  // Get auth headers
  const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token');
    const tokenType = localStorage.getItem('token_type') || 'Bearer';
    return {
      'Authorization': `${tokenType} ${token}`,
      'Content-Type': 'application/json',
    };
  };

  // Check if response indicates authentication failure
  const handleAuthError = useCallback((response: Response) => {
    if (response.status === 401 || response.status === 403) {
      console.log('Authentication failed, redirecting to login');
      handleLogout();
      return true;
    }
    return false;
  }, [handleLogout]);

  // Copy code to clipboard
  const copyToClipboard = async (code: string, codeId: string) => {
    try {
      await navigator.clipboard.writeText(code);
      setCopiedCode(codeId);
      setTimeout(() => setCopiedCode(null), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  // Parse message content to detect code blocks
  const parseMessageContent = (content: string) => {
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = codeBlockRegex.exec(content)) !== null) {
      if (match.index > lastIndex) {
        parts.push({
          type: 'text',
          content: content.slice(lastIndex, match.index)
        });
      }

      parts.push({
        type: 'code',
        language: match[1] || 'text',
        content: match[2].trim()
      });

      lastIndex = match.index + match[0].length;
    }

    if (lastIndex < content.length) {
      parts.push({
        type: 'text',
        content: content.slice(lastIndex)
      });
    }

    return parts.length > 0 ? parts : [{ type: 'text', content }];
  };

  // Render message content with code highlighting
  const renderMessageContent = (content: string, messageId: string) => {
    const parts = parseMessageContent(content);
    
    return (
      <div className="prose max-w-none">
        {parts.map((part, index) => {
          if (part.type === 'code') {
            const codeId = `${messageId}-${index}`;
            return (
              <div key={index} className="my-4 first:mt-0 last:mb-0">
                <div className="bg-black rounded-t-lg px-4 py-2 flex items-center justify-between">
                  <span className="text-gray-400 text-sm font-mono">{part.language}</span>
                  <button
                    onClick={() => copyToClipboard(part.content, codeId)}
                    className="flex items-center space-x-1 px-2 py-1 text-gray-400 hover:text-white transition-colors rounded text-sm"
                  >
                    {copiedCode === codeId ? (
                      <>
                        <Check className="w-4 h-4" />
                        <span>Copied!</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-4 h-4" />
                        <span>Copy</span>
                      </>
                    )}
                  </button>
                </div>
                <div className="bg-gray-800 rounded-b-lg p-4 overflow-x-auto">
                  <pre className="text-gray-100 text-sm leading-relaxed font-mono">
                    <code>{part.content}</code>
                  </pre>
                </div>
              </div>
            );
          } else {
            return (
              <div key={index} className="whitespace-pre-wrap leading-relaxed">
                {part.content.trim()}
              </div>
            );
          }
        })}
      </div>
    );
  };

  // Load messages for a session
  const loadMessages = useCallback(async (sessionId: string) => {
    try {
      const response = await fetch(`http://localhost:8003/api/v1/gateway/sessions/${sessionId}/messages`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (response.ok) {
        const data = await response.json();
        setMessages(data);
      } else if (response.status === 404) {
        console.log(`Messages endpoint not found for session ${sessionId}, starting with empty messages`);
        setMessages([]);
      } else {
        console.error(`Failed to load messages, status: ${response.status}`);
        setMessages([]);
      }
    } catch (error) {
      console.error('Error loading messages:', error);
      setMessages([]);
    }
  }, []);

  // Load chat history from chat history service
  const loadChatHistory = useCallback(async () => {
    try {
      // Clear existing messages immediately to show loading state
      setMessages([]);
      
      // Get current values at time of call
      const sessionInfo = { sessionId: currentSession?.id, sessionTitle: currentSession?.title };
      const activeFileName = activeFile?.file_name || 'None';
      
      console.log('🔍 TRIGGERING CHAT HISTORY ENDPOINT:', apiEndpoints.chatHistory);
      console.log('📤 Expected response format: [{"question": "...", "answer": "..."}]');
      console.log('📋 Current session info:', sessionInfo);
      console.log('📁 Active file:', activeFileName);
      
      // TEST MODE: Set this to true to test with sample data without backend
      const TEST_MODE = false;
      if (TEST_MODE) {
        const testChatHistory = [
          {
            "question": "check data types",
            "answer": "DATA TYPE OPTIMIZATION ANALYSIS SUMMARY\n\nOVERVIEW:\nAnalyzed 11 columns in a hypertension dataset to optimize data types for improved analysis performance and memory efficiency.\n\nKEY FINDINGS:\n- 6 out of 11 columns are using suboptimal data types, all stored as generic \"object\" types instead of specialized categorical formats\n- All numeric data (Age, Salt Intake, Stress Score, Sleep Duration, BMI) is clean with no missing values or data quality issues\n- 3 columns contain simple yes/no data that can be converted to efficient boolean types\n- No mixed data types or corrupted entries detected - dataset is structurally sound\n\nRECOMMENDED OPTIMIZATIONS:\n1. Convert 5 categorical columns (BP History, Medication, Family History, Exercise Level, Smoking Status) from object to category type for better memory usage and analysis capabilities\n2. Convert 1 target column (Has Hypertension) to boolean for logical operations\n3. Keep numeric columns as-is - they are properly formatted\n\nBUSINESS IMPACT:\n- Improved memory efficiency for larger datasets\n- Faster analysis and modeling operations\n- Better data integrity for machine learning workflows\n- Enhanced categorical analysis capabilities for health risk factors\n\nNEXT STEPS:\nImplement the 6 recommended data type conversions to prepare the dataset for advanced analytics and predictive modeling. The clean data quality means conversions can proceed without additional data cleaning steps."
          }
        ];
        console.log('🧪 TEST MODE: Using sample chat history');
        
        // Process test data directly
        const messages: Message[] = [];
        testChatHistory.forEach((item, index) => {
          const baseId = Date.now() + index * 2;
          const currentTime = new Date();
          
          messages.push({
            id: `${baseId}`,
            content: item.question,
            role: 'user',
            timestamp: new Date(currentTime.getTime() + index * 2).toISOString(),
          });
          
          messages.push({
            id: `${baseId + 1}`,
            content: item.answer,
            role: 'assistant',
            timestamp: new Date(currentTime.getTime() + index * 2 + 1).toISOString(),
          });
        });
        
        setMessages(messages);
        console.log(`✅ TEST MODE: Successfully loaded ${messages.length} messages`);
        return;
      }
      
      // Gateway handles all parameter extraction from token automatically
      // Just need to ensure user is authenticated and has active session/file
      const currentState = { 
        hasSession: !!currentSession,
        sessionTitle: currentSession?.title,
        hasActiveFile: !!activeFile,
        fileName: activeFile?.file_name,
        isAuthenticated: !!localStorage.getItem('access_token')
      };
      console.log('📋 Current state:', currentState);

      const response = await fetch(apiEndpoints.chatHistory, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      console.log('📡 Response status:', response.status, 'OK:', response.ok);
      
      if (response.ok) {
        const chatHistory: ChatHistoryItem[] = await response.json();
        console.log('📖 Raw chat history response:', JSON.stringify(chatHistory, null, 2));
        
        if (chatHistory && chatHistory.length > 0) {
          // Convert chat history to dialog format: questions on RIGHT (user), answers on LEFT (assistant)
          const messages: Message[] = [];
          chatHistory.forEach((item, index) => {
            const baseId = Date.now() + index * 2;
            const currentTime = new Date();
            
            // Add user question (will appear on RIGHT side)
            messages.push({
              id: `${baseId}`,
              content: item.question,
              role: 'user',
              timestamp: new Date(currentTime.getTime() + index * 2).toISOString(),
            });
            
            // Add assistant answer (will appear on LEFT side)
            messages.push({
              id: `${baseId + 1}`,
              content: item.answer,
              role: 'assistant',
              timestamp: new Date(currentTime.getTime() + index * 2 + 1).toISOString(),
            });
          });
          
          setMessages(messages);
          console.log(`✅ Successfully converted ${chatHistory.length} chat history items to ${messages.length} dialog messages`);
          console.log('💬 Chat history recreated: Questions on RIGHT (user), Answers on LEFT (assistant)');
          console.log(`📋 Sample format - Question: "${chatHistory[0].question.substring(0, 30)}..." Answer: "${chatHistory[0].answer.substring(0, 30)}..."`);
          console.log(`📁 Chat history loaded for file: ${activeFileName}`);
        } else {
          console.log('📝 No previous conversation history found - showing empty chat (like new session)');
          setMessages([]);
        }
      } else {
        const errorText = await response.text().catch(() => 'No error details');
        console.log(`⚠️ Chat history service responded with status ${response.status}`);
        console.log(`📝 Error response body:`, errorText);
        setMessages([]);
      }
    } catch (error) {
      console.error('❌ Error loading chat history:', error);
      console.log('🔧 Possible issues: 1) API gateway not running on port 8003, 2) Not authenticated, 3) No active session/file');
      
      // Try to provide helpful debugging info
      if (error instanceof TypeError && error.message.includes('fetch')) {
        console.log('🚨 Network error - API gateway may not be running on http://localhost:8003');
      }
      
      console.log('📝 Showing empty chat due to chat history service error');
      setMessages([]);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Empty dependency array - only call manually, access current values from closure

  // Load sessions from API
  const loadSessions = useCallback(async () => {
    try {
      const response = await fetch('http://localhost:8003/api/v1/gateway/sessions', {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (handleAuthError(response)) return;

      if (response.ok) {
        const data = await response.json();
        setSessions(data);
      } else {
        console.error('Failed to load sessions');
      }
    } catch (error) {
      console.error('Error loading sessions:', error);
    }
  }, [handleAuthError]);

  // Load files from API
  const loadFiles = useCallback(async () => {
    setLoadingFiles(true);
    try {
      const response = await fetch('http://localhost:8003/api/v1/gateway/files', {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (response.ok) {
        const data = await response.json();
        setFiles(data);
      } else {
        console.error('Failed to load files');
        setFiles([]);
      }
    } catch (error) {
      console.error('Error loading files:', error);
      setFiles([]);
    } finally {
      setLoadingFiles(false);
    }
  }, []);

  // Get active file for current session
  const getActiveFile = useCallback(async () => {
    if (!currentSession) {
      setActiveFile(null);
      return;
    }

    try {
      console.log(`Getting active file for session: ${currentSession.title}`);
      
      // Try the files/active endpoint first
      let response = await fetch('http://localhost:8003/api/v1/gateway/files/active', {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      // If that fails with 405 or 404, try alternative approaches
      if (!response.ok && (response.status === 405 || response.status === 404)) {
        console.log(`GET /files/active failed with ${response.status}, trying alternative...`);
        
        // Clear active file state since we can't retrieve it
        setActiveFile(null);
        console.log(`Cleared active file for session ${currentSession.title} due to endpoint unavailability`);
        return;
      }

      if (response.ok) {
        const data = await response.json();
        console.log('Active file response:', data);
        
        // Set active file state for current session only
        setActiveFile(data);
        console.log(`Updated active file for current session ${currentSession.title}: ${data?.file_name || 'None'}`);
        
      } else {
        console.log(`Failed to get active file, status: ${response.status}`);
        setActiveFile(null);
        console.log(`Cleared active file for session ${currentSession.title}`);
      }
    } catch (error) {
      console.error('Error getting active file:', error);
      setActiveFile(null);
    }
  }, [currentSession]);

  // Set active file for current session
  const setActiveFileForSession = async (fileName: string) => {
    if (!currentSession || settingActiveFile === fileName) return;

    setSettingActiveFile(fileName);
    
    try {
      // Try with trailing slash first (as documented)
      let response = await fetch('http://localhost:8003/api/v1/gateway/files/active/', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          file_name: fileName,
        }),
      });

      // If that fails with 405, try without trailing slash
      if (!response.ok && response.status === 405) {
        console.log('POST /files/active/ failed with 405, trying without trailing slash...');
        response = await fetch('http://localhost:8003/api/v1/gateway/files/active', {
          method: 'POST',
          headers: getAuthHeaders(),
          body: JSON.stringify({
            file_name: fileName,
          }),
        });
      }

      if (response.ok) {
        // Immediately update the active file for visual feedback
        const selectedFile = files.find(f => f.file_name === fileName);
        if (selectedFile) {
          setActiveFile(selectedFile);
        }
        // The active file state is already updated above for immediate visual feedback
        await loadFiles();
        await getActiveFile();
        
        // IMPORTANT: Load chat history for this file when it becomes active
        console.log(`📂 File ${fileName} is now active - loading chat history`);
        await loadChatHistory();
        
        console.log(`Successfully set ${fileName} as active file for session ${currentSession.title}`);
      } else {
        console.error(`Failed to set active file, status: ${response.status}`);
        // Still update the UI optimistically
        const selectedFile = files.find(f => f.file_name === fileName);
        if (selectedFile) {
          setActiveFile(selectedFile);
          console.log(`Set active file locally despite API failure: ${fileName}`);
          
          // Load chat history even if API failed
          console.log(`📂 File ${fileName} set locally - loading chat history`);
          await loadChatHistory();
        }
      }
    } catch (error) {
      console.error('Error setting active file:', error);
      // Still update the UI optimistically
      const selectedFile = files.find(f => f.file_name === fileName);
      if (selectedFile) {
        setActiveFile(selectedFile);
        console.log(`Set active file locally due to network error: ${fileName}`);
        
        // Load chat history even on network error
        try {
          console.log(`📂 File ${fileName} set locally (network error) - loading chat history`);
          await loadChatHistory();
        } catch (historyError) {
          console.error('Failed to load chat history after network error:', historyError);
        }
      }
    } finally {
      setSettingActiveFile(null);
    }
  };

  // Upload file function
  const uploadFile = async () => {
    if (!selectedFile || !fileName.trim()) {
      setUploadError('Please select a file and provide a name');
      return;
    }

    setUploadingFile(true);
    setUploadProgress(0);
    setUploadError('');

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('file_name', fileName.trim());
      formData.append('description', fileDescription.trim());

      const response = await fetch('http://localhost:8003/api/v1/gateway/files', {
        method: 'POST',
        headers: {
          'Authorization': `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`,
        },
        body: formData,
      });

      if (response.ok) {
        await loadFiles();
        // Automatically set the uploaded file as active for current session
        if (currentSession) {
          await setActiveFileForSession(fileName.trim());
        }
        setShowUploadModal(false);
        setSelectedFile(null);
        setFileName('');
        setFileDescription('');
        setUploadProgress(100);
      } else {
        const errorData = await response.json().catch(() => ({}));
        setUploadError(errorData.detail || 'Failed to upload file. Please try again.');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadError('Network error. Please check your connection and try again.');
    } finally {
      setUploadingFile(false);
      setTimeout(() => setUploadProgress(0), 1000);
    }
  };

  // Create new session
  const createNewSession = async (sessionName: string) => {
    if (!sessionName.trim()) {
      setNewSessionError('Session name is required');
      return;
    }

    setNewSessionError('');

    try {
      const response = await fetch('http://localhost:8003/api/v1/gateway/sessions', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          title: sessionName.trim(),
        }),
      });

      if (response.ok) {
        const newSession = await response.json();
        setSessions(prev => [newSession, ...prev]);
        setCurrentSession(newSession);
        setMessages([]);
        setShowNewSessionModal(false);
        setNewSessionName('');
        
        loadFiles();
        
        localStorage.setItem('activeSessionId', newSession.id);
        localStorage.setItem('activeSessionTitle', newSession.title);
        
        try {
          await fetch(`http://localhost:8003/api/v1/gateway/sessions/active/${newSession.title}`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({
              title: newSession.title,
            }),
          });
          
          // Load chat history for the new session (will be empty for new sessions)
          await loadChatHistory();
          
          // After setting session as active, get the active file
          await getActiveFile();
        } catch (error) {
          console.error('Failed to set new session as active:', error);
        }
      } else if (response.status === 409) {
        setNewSessionError('A chat with this name already exists. Please choose a different name.');
      } else {
        console.error('Failed to create session');
        setNewSessionError('Failed to create session. Please try again.');
      }
    } catch (error) {
      console.error('Error creating session:', error);
      setNewSessionError('Network error. Please check your connection and try again.');
    }
  };

  // Switch session
  const switchSession = async (session: Session) => {
    if (currentSession?.id === session.id) return;

    try {
      console.log(`🔄 User clicked to switch to session: ${session.title}`);
      const response = await fetch(`http://localhost:8003/api/v1/gateway/sessions/active/${session.title}`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          title: session.title,
        }),
      });

      if (response.ok) {
        console.log(`✅ Successfully set session ${session.title} as active`);
        
        // Set the current session first
        setCurrentSession(session);
        
        // ALWAYS load chat history when switching sessions - this is the key functionality
        console.log(`📚 Loading chat history for session: ${session.title}`);
        await loadChatHistory();
        
        // Load other session data
        loadFiles();
        
        // Store session info
        localStorage.setItem('activeSessionId', session.id);
        localStorage.setItem('activeSessionTitle', session.title);
        
        // Now get the active file for this session
        await getActiveFile();
        
        console.log(`🎉 Session switch complete for: ${session.title} - Chat history loaded`);
      } else {
        console.error('❌ Failed to set session as active on backend');
        // Even if backend fails, still try to load chat history for better UX
        setCurrentSession(session);
        console.log(`📚 Loading chat history despite backend error for session: ${session.title}`);
        await loadChatHistory();
      }
    } catch (error) {
      console.error('❌ Error switching session:', error);
      // Fallback: still try to show the session with chat history
      setCurrentSession(session);
      console.log(`📚 Loading chat history in fallback mode for session: ${session.title}`);
      await loadChatHistory();
    }
  };

  // Delete session
  const deleteSession = async (session: Session) => {
    // Check if this is the currently active session
    if (currentSession?.id === session.id) {
      alert(`Cannot delete "${session.title}" because it is currently active. Please switch to a different session first.`);
      return;
    }
    setSessionToDelete(session);
    setShowDeleteSessionModal(true);
  };

  const confirmDeleteSession = async () => {
    if (!sessionToDelete) return;

    setDeletingSession(true);
    try {
      // Based on UI requirements: DELETE to /api/v1/gateway/sessions/{title}
      const response = await fetch(`http://localhost:8003/api/v1/gateway/sessions/${sessionToDelete.title}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });

      if (response.ok) {
        // Remove session from list
        setSessions(prev => prev.filter(s => s.id !== sessionToDelete.id));
        
        // If this was the current session, switch to another or clear
        if (currentSession?.id === sessionToDelete.id) {
          const remainingSessions = sessions.filter(s => s.id !== sessionToDelete.id);
          if (remainingSessions.length > 0) {
            await switchSession(remainingSessions[0]);
          } else {
            setCurrentSession(null);
            setMessages([]);
            setActiveFile(null);
          }
        }
      } else {
        console.error('Failed to delete session');
      }
    } catch (error) {
      console.error('Error deleting session:', error);
    } finally {
      setDeletingSession(false);
      setShowDeleteSessionModal(false);
      setSessionToDelete(null);
    }
  };

  // Get dataset info
  const getDatasetInfo = async (fileName: string) => {
    setLoadingDatasetInfo(true);
    try {
      // First set the file as active to get its detailed info
      let response = await fetch('http://localhost:8003/api/v1/gateway/files/active/', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          file_name: fileName,
        }),
      });

      // If that fails with 405, try without trailing slash
      if (!response.ok && response.status === 405) {
        console.log('POST /files/active/ failed with 405 for dataset info, trying without trailing slash...');
        response = await fetch('http://localhost:8003/api/v1/gateway/files/active', {
          method: 'POST',
          headers: getAuthHeaders(),
          body: JSON.stringify({
            file_name: fileName,
          }),
        });
      }

      if (response.ok) {
        // Now get the active file details
        const activeResponse = await fetch('http://localhost:8003/api/v1/gateway/files/active', {
          method: 'GET',
          headers: getAuthHeaders(),
        });

        if (activeResponse.ok) {
          const datasetInfo = await activeResponse.json();
          setSelectedDatasetInfo(datasetInfo);
          setShowDatasetInfoTab(true);
        } else {
          console.error('Failed to get dataset info after setting file as active');
        }
      } else {
        console.error(`Failed to set file as active for info retrieval, status: ${response.status}`);
        // Show an error message to the user
        alert(`Unable to retrieve dataset information. The backend may not support this feature yet.`);
      }
    } catch (error) {
      console.error('Error getting dataset info:', error);
    } finally {
      setLoadingDatasetInfo(false);
    }
  };

  // Save conversation
  const saveConversation = async () => {
    if (!currentSession || messages.length === 0) {
      setSaveMessage('No conversation to save');
      setTimeout(() => setSaveMessage(''), 3000);
      return;
    }

    if (isLoading) {
      setSaveMessage('Please wait for the response to complete before saving');
      setTimeout(() => setSaveMessage(''), 3000);
      return;
    }

    setSavingConversation(true);
    setSaveMessage('');

    try {
      const response = await fetch('http://localhost:8003/api/v1/gateway/chat/save', {
        method: 'POST',
        headers: getAuthHeaders(),
      });

      if (response.ok) {
        setSaveMessage('Conversation saved successfully!');
        setTimeout(() => setSaveMessage(''), 3000);
      } else {
        throw new Error('Failed to save conversation');
      }
    } catch (error) {
      console.error('Error saving conversation:', error);
      setSaveMessage('Failed to save conversation. Please try again.');
      setTimeout(() => setSaveMessage(''), 5000);
    } finally {
      setSavingConversation(false);
    }
  };

  // Delete file
  const deleteFile = async (file: FileItem) => {
    // Check if this file is currently active
    if (activeFile?.file_name === file.file_name) {
      alert(`Cannot delete "${file.file_name}" because it is currently active for this session. Please select a different file first.`);
      return;
    }
    setFileToDelete(file);
    setShowDeleteFileModal(true);
  };

  const confirmDeleteFile = async () => {
    if (!fileToDelete) return;

    setDeletingFile(true);
    try {
      // Based on UI requirements: DELETE to /api/v1/gateway/files/{file_name}
      const response = await fetch(`http://localhost:8003/api/v1/gateway/files/${fileToDelete.file_name}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });

      if (response.ok) {
        // Remove file from list
        setFiles(prev => prev.filter(f => f.file_name !== fileToDelete.file_name));
        
        // If this was the active file, clear it
        if (activeFile?.file_name === fileToDelete.file_name) {
          setActiveFile(null);
        }
      } else {
        console.error('Failed to delete file');
      }
    } catch (error) {
      console.error('Error deleting file:', error);
    } finally {
      setDeletingFile(false);
      setShowDeleteFileModal(false);
      setFileToDelete(null);
    }
  };

  // Send message with streaming
  const sendMessage = async () => {
    if (!inputMessage.trim() || !currentSession || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage,
      role: 'user',
      timestamp: new Date().toISOString(),
    };

    const currentQuestion = inputMessage;
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setStreamingMessage('');

    try {
      console.log('🚀 Starting streaming request for question:', currentQuestion.substring(0, 50) + '...');
      if (DEBUG_STREAMING) {
        console.log('Starting streaming request to:', `http://localhost:8003/api/v1/gateway/chat/stream?question=${encodeURIComponent(currentQuestion)}`);
      }
      
      // Try streaming endpoint - first without trailing slash
      let response = await fetch(`http://localhost:8003/api/v1/gateway/chat/stream?question=${encodeURIComponent(currentQuestion)}`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      // If that fails, try with trailing slash
      if (!response.ok && (response.status === 404 || response.status === 405)) {
        console.log(`Streaming endpoint failed with ${response.status}, trying with trailing slash...`);
        response = await fetch(`http://localhost:8003/api/v1/gateway/chat/stream/?question=${encodeURIComponent(currentQuestion)}`, {
          method: 'GET',
          headers: getAuthHeaders(),
        });
      }

      if (DEBUG_STREAMING) {
        console.log('Stream response status:', response.status, 'OK:', response.ok);
        console.log('Stream response headers:', Object.fromEntries(response.headers.entries()));
      }

      if (handleAuthError(response)) {
        setIsLoading(false);
        return;
      }

      if (response.ok && response.body) {
        console.log('✅ Streaming response received, starting to read chunks...');
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullContent = '';
        let chunkCount = 0;

        try {
          while (true) {
            const { done, value } = await reader.read();
            if (done) {
              console.log(`✅ Streaming completed. Total chunks: ${chunkCount}, Final content length: ${fullContent.length}`);
              break;
            }

            // Decode the chunk - this is plain text from the ML agent
            const chunk = decoder.decode(value, { stream: true });
            chunkCount++;
            
            if (DEBUG_STREAMING) {
              console.log(`📦 Chunk ${chunkCount}:`, JSON.stringify(chunk));
            }
            
            // Simply append the chunk to the full content
            fullContent += chunk;
            setStreamingMessage(fullContent);
          }
        } catch (readError) {
          console.error('❌ Error reading stream:', readError);
          // If streaming fails, fall back to regular chat
          throw readError;
        }

        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: fullContent || 'No response received',
          role: 'assistant',
          timestamp: new Date().toISOString(),
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        // Fallback to regular chat endpoint
        console.log(`❌ Streaming failed with status ${response.status}, falling back to regular chat endpoint`);
        let fallbackResponse = await fetch(`http://localhost:8003/api/v1/gateway/chat?question=${encodeURIComponent(currentQuestion)}`, {
          method: 'GET',
          headers: getAuthHeaders(),
        });

        // If that fails, try with trailing slash
        if (!fallbackResponse.ok && (fallbackResponse.status === 404 || fallbackResponse.status === 405)) {
          console.log('Regular chat endpoint failed, trying with trailing slash...');
          fallbackResponse = await fetch(`http://localhost:8003/api/v1/gateway/chat/?question=${encodeURIComponent(currentQuestion)}`, {
            method: 'GET',
            headers: getAuthHeaders(),
          });
        }

        if (fallbackResponse.ok) {
          const contentType = fallbackResponse.headers.get('content-type');
          let content;
          
          if (contentType && contentType.includes('application/json')) {
            const data = await fallbackResponse.json();
            content = data.response || data.message || data.answer || JSON.stringify(data);
          } else {
            content = await fallbackResponse.text();
          }
          
          const assistantMessage: Message = {
            id: (Date.now() + 1).toString(),
            content: content || 'No response received',
            role: 'assistant',
            timestamp: new Date().toISOString(),
          };
          setMessages(prev => [...prev, assistantMessage]);
        } else {
          throw new Error('Failed to get response');
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error. Please try again.',
        role: 'assistant',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setStreamingMessage('');
    }
  };

  // Initialize sessions
  const initializeSessions = useCallback(async () => {
    await loadSessions();
    // Load files initially
    await loadFiles();
  }, [loadSessions, loadFiles]);

  // Restore active session after sessions are loaded
  const restoreActiveSession = useCallback(async () => {
    const savedSessionId = localStorage.getItem('activeSessionId');
    const savedSessionTitle = localStorage.getItem('activeSessionTitle');
    
    if (savedSessionId && savedSessionTitle && sessions.length > 0) {
      const savedSession = sessions.find(s => s.id === savedSessionId && s.title === savedSessionTitle);
      if (savedSession) {
        console.log(`Restoring active session: ${savedSession.title}`);
        setCurrentSession(savedSession);
        
        // Load chat history for the restored session
        await loadChatHistory();
        
        // Ensure we get the active file for this restored session
        await getActiveFile();
        console.log(`Session restoration complete for: ${savedSession.title}`);
      } else {
        console.log('Saved session not found, clearing localStorage');
        localStorage.removeItem('activeSessionId');
        localStorage.removeItem('activeSessionTitle');
      }
    }
  }, [sessions, loadChatHistory, getActiveFile]);

  // Check if user is authenticated and initialize
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      router.push('/login');
      return;
    }
    
    initializeSessions();
  }, [initializeSessions, router]);

  // Restore active session after sessions are loaded
  useEffect(() => {
    if (sessions.length > 0) {
      restoreActiveSession();
    }
  }, [sessions, restoreActiveSession]);

  // Auto scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingMessage]);

  return (
    <div className="h-screen bg-white flex relative">
      {/* Mobile backdrop */}
      {(leftSidebarOpen || rightSidebarOpen) && (
        <div 
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-30 md:hidden transition-all duration-300"
          onClick={() => {
            setLeftSidebarOpen(false);
            setRightSidebarOpen(false);
          }}
        />
      )}
      
      {/* Left Sidebar - Chat History */}
      <div className={`${
        leftSidebarOpen ? 'w-80 md:w-80' : 'w-0'
      } transition-all duration-500 ease-in-out overflow-hidden bg-white flex flex-col ${
        leftSidebarOpen ? 'fixed md:relative z-40 md:z-auto h-full shadow-xl' : ''
      } border-r border-blue-100`}>
        {/* Sidebar Header */}
        <div className="p-8 border-b border-blue-100 bg-gradient-to-r from-blue-50 to-indigo-50 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-3xl flex items-center justify-center shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-gray-800 font-bold text-xl">ML Agent</h1>
                <p className="text-blue-600 text-sm font-medium">Intelligent Data Assistant</p>
              </div>
            </div>
            <button
              onClick={() => setLeftSidebarOpen(false)}
              className="p-2 hover:bg-blue-100 rounded-xl transition-all duration-200 group shadow-sm hover:shadow-md"
              title="Close sidebar"
            >
              <X className="w-5 h-5 text-blue-400 group-hover:text-blue-600" />
            </button>
          </div>
          <button
            onClick={() => setShowNewSessionModal(true)}
            className="w-full flex items-center justify-center space-x-4 px-6 py-4 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white rounded-2xl transition-all duration-300 font-semibold shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98] hover:-translate-y-0.5"
          >
            <Plus className="w-5 h-5" />
            <span className="text-base">New Chat</span>
            <div className="w-2 h-2 bg-white/40 rounded-full animate-pulse"></div>
          </button>
        </div>

        {/* Chat Sessions */}
        <div className="flex-1 overflow-y-auto p-6 space-y-3">
          <div className="text-blue-600 text-sm font-semibold uppercase tracking-wider mb-6 px-3">
            Recent Conversations
          </div>
          {sessions.map((session, index) => (
            <div
              key={session.id}
              className="opacity-0 animate-fade-in"
              style={{ animationDelay: `${index * 0.05}s`, animationFillMode: 'forwards' }}
            >
              <div className={`w-full text-left p-5 rounded-2xl transition-all duration-300 group relative overflow-hidden shadow-md hover:shadow-lg ${
                currentSession?.id === session.id
                  ? 'bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-900 border-2 border-blue-200 transform scale-[1.02] shadow-lg'
                  : 'bg-white text-gray-700 hover:bg-blue-50 hover:text-blue-900 hover:shadow-xl hover:transform hover:scale-[1.01] hover:-translate-y-1 border border-gray-200 hover:border-blue-200'
              }`}>
                <div className="flex items-center space-x-4">
                  <div className={`w-3 h-3 rounded-full transition-all duration-300 shadow-sm ${
                    currentSession?.id === session.id 
                      ? 'bg-blue-500 shadow-lg animate-pulse' 
                      : 'bg-gray-400 group-hover:bg-blue-400'
                  }`} />
                  <div 
                    className="min-w-0 flex-1 cursor-pointer"
                    onClick={() => switchSession(session)}
                  >
                    <span className="text-base font-semibold truncate block leading-6">
                      {session.title}
                    </span>
                    <span className="text-sm opacity-75 truncate block font-medium">
                      {session.created_at && !isNaN(new Date(session.created_at).getTime()) 
                        ? new Date(session.created_at).toLocaleDateString('en-US', {
                            month: 'short',
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })
                        : 'Recent'
                      }
                    </span>
                    {/* Active file indicator - only show for currently active session */}
                    {currentSession?.id === session.id && (
                      <>
                        {activeFile?.file_name ? (
                          <div className="flex items-center space-x-2 mt-3 px-3 py-2 bg-gradient-to-r from-emerald-100 to-green-100 text-emerald-700 rounded-xl text-xs font-bold shadow-md border border-emerald-200">
                            <File className="w-3.5 h-3.5" />
                            <span className="truncate max-w-[100px]">
                              📊 {activeFile.file_name}
                            </span>
                            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse shadow-sm"></div>
                          </div>
                        ) : (
                          <div className="text-xs text-gray-400 mt-2 px-3 italic">
                            No dataset selected
                          </div>
                        )}
                      </>
                    )}
                  </div>
                  <div className="flex items-center space-x-3">
                    <MessageSquare className={`w-5 h-5 transition-all duration-200 ${
                      currentSession?.id === session.id 
                        ? 'text-blue-600' 
                        : 'text-gray-400 group-hover:text-blue-500'
                    }`} />
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteSession(session);
                      }}
                      disabled={currentSession?.id === session.id}
                      className={`p-2 rounded-xl transition-all duration-200 shadow-sm ${
                        currentSession?.id === session.id
                          ? 'opacity-30 cursor-not-allowed text-gray-400'
                          : 'opacity-0 group-hover:opacity-100 hover:bg-red-100 hover:text-red-500 hover:shadow-md hover:scale-110'
                      }`}
                      title={currentSession?.id === session.id ? 'Cannot delete active session' : 'Delete session'}
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                
                {/* Active session indicator */}
                {currentSession?.id === session.id && (
                  <div className="absolute left-0 top-1/2 transform -translate-y-1/2 w-1.5 h-10 bg-gradient-to-b from-blue-500 to-indigo-600 rounded-r-full shadow-lg" />
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Sidebar Footer */}
        <div className="p-6 border-t border-blue-100 bg-gradient-to-r from-blue-50 to-indigo-50 shadow-sm">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
              <User className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-gray-800 font-semibold text-base">User</div>
              <div className="text-blue-600 text-sm font-medium">Free Plan</div>
            </div>
            <button
              onClick={handleLogout}
              className="p-3 hover:bg-red-100 rounded-xl transition-all duration-200 text-gray-500 hover:text-red-600 group shadow-sm hover:shadow-md hover:scale-110"
              title="Sign out"
            >
              <LogOut className="w-5 h-5 group-hover:scale-110 transition-transform" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col bg-white">
        {/* Header */}
        <div className="bg-white border-b border-blue-100 px-8 py-5 flex items-center justify-between shadow-md">
          <div className="flex items-center space-x-4">
            {!leftSidebarOpen && (
              <button
                onClick={() => setLeftSidebarOpen(true)}
                className="p-3 hover:bg-blue-100 rounded-2xl transition-all duration-200 group shadow-sm hover:shadow-md hover:scale-105"
              >
                <Menu className="w-6 h-6 text-blue-500 group-hover:text-blue-700" />
              </button>
            )}
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-gray-800">
                {currentSession?.title || 'ML Agent'}
              </h1>
              {activeFile && (
                <div className="flex items-center space-x-3 px-4 py-2.5 bg-gradient-to-r from-emerald-50 to-green-50 text-emerald-700 rounded-2xl text-base font-semibold shadow-lg border-2 border-emerald-200 hover:shadow-xl transition-all duration-300 hover:scale-105">
                  <div className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse shadow-sm"></div>
                  <File className="w-4 h-4" />
                  <span>{activeFile.file_name}</span>
                </div>
              )}
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            {/* Save Conversation Button */}
            {currentSession && messages.length > 0 && (
              <div className="relative">
                <button
                  onClick={saveConversation}
                  disabled={savingConversation || isLoading}
                  className={`flex items-center space-x-2 px-4 py-3 rounded-2xl transition-all duration-200 group shadow-sm hover:shadow-md hover:scale-105 font-semibold ${
                    savingConversation || isLoading
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white shadow-green-500/30 hover:shadow-green-500/50'
                  }`}
                  title={isLoading ? "Please wait for the response to complete" : "Save conversation"}
                >
                  {savingConversation ? (
                    <>
                      <div className="w-5 h-5 border-2 border-gray-400 border-t-transparent rounded-full animate-spin" />
                      <span>Saving...</span>
                    </>
                  ) : isLoading ? (
                    <>
                      <Save className="w-5 h-5" />
                      <span>Wait...</span>
                    </>
                  ) : (
                    <>
                      <Save className="w-5 h-5" />
                      <span>Save</span>
                    </>
                  )}
                </button>
                {saveMessage && (
                  <div className={`absolute top-full left-1/2 transform -translate-x-1/2 mt-2 px-3 py-2 text-sm rounded-lg shadow-lg z-50 whitespace-nowrap ${
                    saveMessage.includes('success') 
                      ? 'bg-green-100 text-green-800 border border-green-200'
                      : 'bg-red-100 text-red-800 border border-red-200'
                  }`}>
                    {saveMessage}
                  </div>
                )}
              </div>
            )}
            <button
              onClick={() => setRightSidebarOpen(!rightSidebarOpen)}
              className={`p-3 rounded-2xl transition-all duration-200 group shadow-sm hover:shadow-md hover:scale-105 ${
                rightSidebarOpen 
                  ? 'bg-blue-100 text-blue-600 shadow-md' 
                  : 'hover:bg-blue-100 text-blue-500 hover:text-blue-700'
              }`}
              title="Dataset Files"
            >
              <PaperclipIcon className="w-6 h-6" />
            </button>
            {leftSidebarOpen && (
              <button
                onClick={() => setLeftSidebarOpen(false)}
                className="p-3 hover:bg-blue-100 rounded-2xl transition-all duration-200 group shadow-sm hover:shadow-md hover:scale-105"
                title="Close sidebar"
              >
                <X className="w-6 h-6 text-blue-500 group-hover:text-blue-700" />
              </button>
            )}
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto bg-gradient-to-b from-blue-50/30 to-white p-4">
          {!currentSession ? (
            <div className="h-full flex items-center justify-center p-12">
              <div className="text-center max-w-3xl bg-white rounded-3xl p-12 shadow-xl border border-blue-100">
                <div className="mb-10">
                  <div className="w-24 h-24 bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-600 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-2xl hover:shadow-3xl transition-all duration-300 hover:scale-110 animate-pulse">
                    <Bot className="w-12 h-12 text-white" />
                  </div>
                  <h2 className="text-5xl font-bold text-gray-800 mb-6">
                    Welcome to <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">ML Agent</span>
                  </h2>
                  <p className="text-xl text-gray-600 mb-10 leading-relaxed font-medium">
                    Your independent AI assistant for advanced data analysis, insights, and machine learning solutions
                  </p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
                  <div className="bg-white rounded-3xl p-8 shadow-xl border-2 border-blue-100 hover:shadow-2xl transition-all duration-300 hover:scale-105 hover:-translate-y-2">
                    <div className="w-16 h-16 bg-gradient-to-r from-amber-400 to-orange-500 rounded-3xl flex items-center justify-center mb-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-110">
                      <Database className="w-8 h-8 text-white" />
                    </div>
                    <h3 className="text-xl font-bold text-gray-800 mb-3">Data Analysis</h3>
                    <p className="text-gray-600 text-base font-medium">Upload your datasets and get instant insights, visualizations, and statistical analysis</p>
                  </div>
                  
                  <div className="bg-white rounded-3xl p-8 shadow-xl border-2 border-blue-100 hover:shadow-2xl transition-all duration-300 hover:scale-105 hover:-translate-y-2">
                    <div className="w-16 h-16 bg-gradient-to-r from-emerald-400 to-teal-500 rounded-3xl flex items-center justify-center mb-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-110">
                      <Zap className="w-8 h-8 text-white" />
                    </div>
                    <h3 className="text-xl font-bold text-gray-800 mb-3">Smart Insights</h3>
                    <p className="text-gray-600 text-base font-medium">AI-powered recommendations and predictive analytics for your business decisions</p>
                  </div>
                </div>
                
                <button
                  onClick={() => setShowNewSessionModal(true)}
                  className="inline-flex items-center space-x-4 px-10 py-5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold text-lg rounded-3xl transition-all duration-300 shadow-xl hover:shadow-2xl transform hover:scale-105 active:scale-95 hover:-translate-y-1"
                >
                  <Plus className="w-6 h-6" />
                  <span>Start New Conversation</span>
                  <ArrowRight className="w-6 h-6" />
                </button>
              </div>
            </div>
          ) : (
            <div className="max-w-5xl mx-auto px-8 py-10 space-y-10">
              {messages.map((message, index) => (
                <div 
                  key={message.id} 
                  className="opacity-0 animate-fade-in"
                  style={{ animationDelay: `${index * 0.1}s`, animationFillMode: 'forwards' }}
                >
                  <div className={`flex items-start space-x-6 ${message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                    <div className={`w-12 h-12 rounded-3xl flex items-center justify-center shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-110 ${
                      message.role === 'user' 
                        ? 'bg-gradient-to-r from-blue-500 to-indigo-600' 
                        : 'bg-gradient-to-r from-emerald-500 to-teal-600'
                    }`}>
                      {message.role === 'user' ? (
                        <User className="w-6 h-6 text-white" />
                      ) : (
                        <Bot className="w-6 h-6 text-white" />
                      )}
                    </div>
                    <div className={`flex-1 min-w-0 ${message.role === 'user' ? 'text-right' : ''}`}>
                      <div className="flex items-center space-x-3 mb-4">
                        <span className="text-base font-bold text-gray-700">
                          {message.role === 'user' ? 'You' : 'ML Agent'}
                        </span>
                        <span className="text-sm text-blue-500 font-medium">
                          {new Date(message.timestamp).toLocaleTimeString('en-US', {
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </span>
                      </div>
                      <div className={`${
                        message.role === 'user'
                          ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-3xl rounded-br-lg shadow-xl px-8 py-6 hover:shadow-2xl transition-all duration-300'
                          : 'bg-white border-2 border-blue-100 rounded-3xl rounded-bl-lg shadow-xl px-8 py-6 hover:shadow-2xl transition-all duration-300 overflow-hidden'
                      }`}>
                        <div className={`text-base leading-relaxed ${message.role === 'user' ? 'text-white' : 'text-gray-800'}`}>
                          {renderMessageContent(message.content, message.id)}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              
              {/* Streaming message */}
              {isLoading && streamingMessage && (
                <div className="animate-fade-in">
                  <div className="flex items-start space-x-6">
                    <div className="w-12 h-12 rounded-3xl bg-gradient-to-r from-emerald-500 to-teal-600 flex items-center justify-center shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-110 relative">
                      <Bot className="w-6 h-6 text-white" />
                      <div className="absolute -top-1 -right-1 w-4 h-4 bg-blue-500 rounded-full animate-ping shadow-lg"></div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-4 mb-4">
                        <span className="text-base font-bold text-gray-700">ML Agent</span>
                        <div className="flex items-center space-x-2 px-3 py-2 bg-emerald-100 text-emerald-700 rounded-2xl text-sm font-semibold shadow-md">
                          <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                          <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                          <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                          <span>Streaming</span>
                        </div>
                      </div>
                      <div className="bg-white border-2 border-blue-100 rounded-3xl rounded-bl-lg shadow-xl hover:shadow-2xl transition-all duration-300 overflow-hidden">
                        <div className="text-gray-800 p-8 text-base leading-relaxed">
                          {renderMessageContent(streamingMessage, 'streaming')}
                          <span className="inline-block w-2 h-5 bg-emerald-500 animate-pulse ml-1 rounded-sm">▋</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              {/* Loading indicator */}
              {isLoading && !streamingMessage && (
                <div className="animate-fade-in">
                  <div className="flex items-start space-x-4">
                    <div className="w-10 h-10 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg">
                      <Bot className="w-5 h-5 text-white animate-pulse" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-3">
                        <span className="text-sm font-bold text-slate-700">ML Agent</span>
                      </div>
                      <div className="bg-white/80 backdrop-blur-sm border border-slate-200/60 rounded-3xl rounded-bl-lg shadow-lg p-6">
                        <div className="flex items-center space-x-3 text-slate-600">
                          <div className="flex space-x-1">
                            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce"></div>
                            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                          </div>
                          <span className="font-medium">Analyzing your data and preparing insights...</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        {currentSession && (
          <div className="border-t border-blue-100 bg-white shadow-lg p-8">
            <div className="max-w-5xl mx-auto">
              <div className="relative">
                <div className="flex items-end space-x-6 bg-white rounded-3xl border-2 border-blue-100 shadow-xl p-4 focus-within:ring-4 focus-within:ring-blue-500/20 focus-within:border-blue-400 transition-all duration-300 hover:shadow-2xl">
                  <div className="flex-1">
                    <textarea
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                          e.preventDefault();
                          sendMessage();
                        }
                      }}
                      placeholder={`Ask ML Agent${activeFile ? ` about ${activeFile.file_name}` : ' anything about your data'}...`}
                      className="w-full p-6 bg-transparent border-none resize-none focus:outline-none text-gray-800 placeholder-gray-500 text-lg leading-7 font-medium"
                      rows={1}
                      style={{ minHeight: '24px', maxHeight: '160px' }}
                      onInput={(e) => {
                        const target = e.target as HTMLTextAreaElement;
                        target.style.height = 'auto';
                        target.style.height = Math.min(target.scrollHeight, 160) + 'px';
                      }}
                      disabled={isLoading}
                    />
                  </div>
                  <button
                    onClick={sendMessage}
                    disabled={!inputMessage.trim() || isLoading}
                    className={`p-4 rounded-2xl transition-all duration-300 shadow-xl ${
                      inputMessage.trim() && !isLoading
                        ? 'bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white shadow-blue-500/30 hover:shadow-blue-500/50 transform hover:scale-110 active:scale-95 hover:-translate-y-1'
                        : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                    }`}
                  >
                    {isLoading ? (
                      <div className="w-6 h-6 border-2 border-gray-400 border-t-transparent rounded-full animate-spin" />
                    ) : (
                      <Send className="w-6 h-6" />
                    )}
                  </button>
                </div>
                
                {/* Save Message */}
                {saveMessage && (
                  <div className={`mt-3 text-center text-sm font-medium px-4 py-2 rounded-xl shadow-md ${
                    saveMessage.includes('success') 
                      ? 'bg-green-100 text-green-800 border border-green-200'
                      : 'bg-red-100 text-red-800 border border-red-200'
                  }`}>
                    {saveMessage}
                  </div>
                )}
                
                {/* Helper text */}
                <div className="flex items-center justify-center space-x-4 mt-3 text-xs text-slate-500">
                  <div className="flex items-center space-x-1">
                    <Bot className="w-3 h-3" />
                    <span>AI-powered data analysis</span>
                  </div>
                  {activeFile?.file_name && (
                    <>
                      <span>•</span>
                      <div className="flex items-center space-x-1">
                        <File className="w-3 h-3 text-emerald-600" />
                        <span className="text-emerald-600 font-medium">{activeFile.file_name}</span>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Right Sidebar - Files */}
      <div className={`${
        rightSidebarOpen ? 'w-[420px] md:w-[420px]' : 'w-0'
      } transition-all duration-500 ease-in-out overflow-hidden bg-white border-l border-blue-100 flex flex-col ${
        rightSidebarOpen ? 'fixed md:relative z-40 md:z-auto right-0 h-full shadow-xl' : ''
      }`}>
        {/* Files Header */}
        <div className="p-8 border-b border-blue-100 bg-gradient-to-r from-blue-50 to-indigo-50 shadow-sm">
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-3xl flex items-center justify-center shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
                {showDatasetInfoTab ? <Info className="w-6 h-6 text-white" /> : <Database className="w-6 h-6 text-white" />}
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-800">
                  {showDatasetInfoTab ? 'Dataset Information' : 'Dataset Files'}
                </h2>
                <p className="text-sm text-blue-600 font-medium">
                  {showDatasetInfoTab 
                    ? 'Detailed analysis summary' 
                    : `${files.length} file${files.length !== 1 ? 's' : ''} available`
                  }
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              {showDatasetInfoTab && (
                <button
                  onClick={() => {
                    setShowDatasetInfoTab(false);
                    setSelectedDatasetInfo(null);
                  }}
                  className="p-2.5 hover:bg-blue-100 rounded-xl transition-all duration-200 group shadow-sm hover:shadow-md hover:scale-110"
                  title="Back to files"
                >
                  <ArrowRight className="w-6 h-6 text-blue-500 group-hover:text-blue-700 rotate-180" />
                </button>
              )}
              <button
                onClick={() => setRightSidebarOpen(false)}
                className="p-2.5 hover:bg-blue-100 rounded-xl transition-all duration-200 group shadow-sm hover:shadow-md hover:scale-110"
              >
                <X className="w-6 h-6 text-blue-500 group-hover:text-blue-700" />
              </button>
            </div>
          </div>
          {!showDatasetInfoTab && (
            <button
              onClick={() => setShowUploadModal(true)}
              className="w-full flex items-center justify-center space-x-4 px-6 py-4 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white rounded-2xl transition-all duration-300 font-semibold text-base shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98] hover:-translate-y-0.5"
            >
              <Upload className="w-5 h-5" />
              <span>Upload Dataset</span>
              <div className="w-2 h-2 bg-white/40 rounded-full animate-pulse"></div>
            </button>
          )}
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-8 space-y-6">
          {showDatasetInfoTab && selectedDatasetInfo ? (
            /* Dataset Info Tab */
            <div className="space-y-6">
              {/* Dataset Name */}
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-6 border-2 border-blue-100 shadow-md">
                <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center">
                  <File className="w-5 h-5 mr-3 text-blue-600" />
                  Dataset Name
                </h3>
                <p className="text-xl font-semibold text-blue-700 bg-white px-4 py-3 rounded-xl shadow-sm border border-blue-200">
                  {selectedDatasetInfo.file_name}
                </p>
              </div>

              {/* Description */}
              {selectedDatasetInfo.description && (
                <div className="bg-gradient-to-r from-emerald-50 to-green-50 rounded-2xl p-6 border-2 border-emerald-100 shadow-md">
                  <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center">
                    <FileText className="w-5 h-5 mr-3 text-emerald-600" />
                    Description
                  </h3>
                  <p className="text-gray-700 bg-white px-4 py-3 rounded-xl shadow-sm border border-emerald-200 leading-relaxed">
                    {selectedDatasetInfo.description}
                  </p>
                </div>
              )}

              {/* Summary */}
              {selectedDatasetInfo.summary && (
                <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl p-6 border-2 border-purple-100 shadow-md">
                  <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center">
                    <Database className="w-5 h-5 mr-3 text-purple-600" />
                    Data Summary
                  </h3>
                  <div className="bg-white px-4 py-3 rounded-xl shadow-sm border border-purple-200">
                    <div className="prose prose-sm max-w-none text-gray-700">
                      {selectedDatasetInfo.summary.split('\n').map((line, index) => (
                        <div key={index} className="mb-2">
                          {line.startsWith('**') && line.endsWith('**') ? (
                            <strong className="text-purple-700">{line.slice(2, -2)}</strong>
                          ) : line.startsWith('- **') ? (
                            <div className="ml-4 flex items-start">
                              <span className="text-purple-600 mr-2">•</span>
                              <span dangerouslySetInnerHTML={{ 
                                __html: line.slice(2).replace(/\*\*(.*?)\*\*/g, '<strong class="text-purple-700">$1</strong>') 
                              }} />
                            </div>
                          ) : (
                            <span dangerouslySetInnerHTML={{ 
                              __html: line.replace(/\*\*(.*?)\*\*/g, '<strong class="text-purple-700">$1</strong>') 
                            }} />
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Set Active Button */}
              <div className="sticky bottom-0 bg-white pt-4 border-t border-blue-100">
                <button
                  onClick={async () => {
                    if (currentSession && selectedDatasetInfo) {
                      await setActiveFileForSession(selectedDatasetInfo.file_name);
                      setShowDatasetInfoTab(false);
                      setSelectedDatasetInfo(null);
                    }
                  }}
                  disabled={!currentSession}
                  className="w-full px-6 py-4 bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-600 hover:to-green-700 text-white rounded-2xl transition-all duration-200 font-semibold shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-3"
                >
                  <Database className="w-5 h-5" />
                  <span>Set as Active Dataset</span>
                </button>
              </div>
            </div>
          ) : loadingFiles ? (
            <div className="flex items-center justify-center py-16">
              <div className="flex flex-col items-center space-y-6">
                <div className="w-10 h-10 border-3 border-indigo-500 border-t-transparent rounded-full animate-spin shadow-lg"></div>
                <p className="text-gray-600 font-semibold text-lg">Loading datasets...</p>
              </div>
            </div>
          ) : files.length === 0 ? (
            <div className="text-center py-16">
              <div className="w-20 h-20 bg-blue-100 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-lg">
                <FileText className="w-10 h-10 text-blue-500" />
              </div>
              <h3 className="text-xl font-bold text-gray-700 mb-4">No datasets yet</h3>
              <p className="text-gray-500 text-base leading-relaxed font-medium">
                Upload your first dataset to start analyzing data with ML Agent
              </p>
            </div>
          ) : (
            <>
              <div className="text-blue-600 text-sm font-semibold uppercase tracking-wider mb-6 px-3">
                Available Datasets
              </div>
              <div className="space-y-4">
                {files.map((file, index) => (
                  <div
                    key={file.file_name}
                    className="opacity-0 animate-fade-in"
                    style={{ animationDelay: `${index * 0.05}s`, animationFillMode: 'forwards' }}
                  >
                    <div className={`group relative p-6 rounded-3xl border-2 transition-all duration-300 overflow-hidden shadow-md hover:shadow-xl ${
                        activeFile?.file_name === file.file_name
                          ? 'bg-gradient-to-r from-emerald-50 to-green-50 border-emerald-300 shadow-lg transform scale-[1.02]'
                          : 'bg-white border-blue-100 hover:border-blue-200 hover:shadow-xl hover:bg-blue-50/30 hover:transform hover:scale-[1.02] hover:-translate-y-1'
                      }`}
                    >
                      <div className="flex items-start space-x-5">
                        <div className={`w-14 h-14 rounded-3xl flex items-center justify-center shadow-lg transition-all duration-300 hover:scale-110 ${
                          activeFile?.file_name === file.file_name 
                            ? 'bg-gradient-to-r from-emerald-500 to-green-600 text-white shadow-emerald-500/30' 
                            : 'bg-blue-100 text-blue-600 group-hover:bg-blue-200 group-hover:text-blue-700'
                        }`}>
                          <File className="w-7 h-7" />
                        </div>
                        <div 
                          className="flex-1 min-w-0 cursor-pointer"
                          onClick={() => currentSession && setActiveFileForSession(file.file_name || '')}
                        >
                          <div className="flex items-center space-x-3 mb-2">
                            <span className="font-bold text-gray-800 truncate text-base">
                              {file.file_name}
                            </span>
                            {activeFile?.file_name === file.file_name && (
                              <div className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse shadow-md"></div>
                            )}
                          </div>
                          {file.description && (
                            <p className="text-base text-gray-600 truncate mb-3 leading-6 font-medium">
                              {file.description}
                            </p>
                          )}
                          <div className="flex items-center space-x-4 text-sm">
                            {file.size && (
                              <span className="text-gray-500 font-semibold">
                                {(file.size / 1024 / 1024).toFixed(1)} MB
                              </span>
                            )}
                            {file.upload_time && (
                              <span className="text-blue-500 font-medium">
                                {new Date(file.upload_time).toLocaleDateString('en-US', {
                                  month: 'short',
                                  day: 'numeric'
                                })}
                              </span>
                            )}
                          </div>
                        </div>
                        <div className="flex items-center space-x-3">
                          {settingActiveFile === file.file_name && (
                            <div className="w-6 h-6 border-3 border-emerald-500 border-t-transparent rounded-full animate-spin shadow-md"></div>
                          )}
                          {loadingDatasetInfo && selectedDatasetInfo?.file_name === file.file_name && (
                            <div className="w-6 h-6 border-3 border-blue-500 border-t-transparent rounded-full animate-spin shadow-md"></div>
                          )}
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              getDatasetInfo(file.file_name);
                            }}
                            disabled={loadingDatasetInfo}
                            className="opacity-0 group-hover:opacity-100 p-2.5 rounded-xl transition-all duration-200 shadow-sm hover:bg-blue-100 hover:text-blue-600 hover:shadow-md hover:scale-110"
                            title="View dataset information"
                          >
                            <Info className="w-5 h-5" />
                          </button>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              deleteFile(file);
                            }}
                            disabled={activeFile?.file_name === file.file_name}
                            className={`p-2.5 rounded-xl transition-all duration-200 shadow-sm ${
                              activeFile?.file_name === file.file_name
                                ? 'opacity-30 cursor-not-allowed text-gray-400'
                                : 'opacity-0 group-hover:opacity-100 hover:bg-red-100 hover:text-red-500 hover:shadow-md hover:scale-110'
                            }`}
                            title={activeFile?.file_name === file.file_name ? 'Cannot delete active file' : 'Delete file'}
                          >
                            <Trash2 className="w-5 h-5" />
                          </button>
                        </div>
                      </div>
                      
                      {/* Active indicator */}
                      {activeFile?.file_name === file.file_name && (
                        <div className="absolute left-0 top-1/2 transform -translate-y-1/2 w-2 h-16 bg-gradient-to-b from-emerald-500 to-green-600 rounded-r-full shadow-lg"></div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>

      {/* New Session Modal */}
      {showNewSessionModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">New Chat</h2>
            <input
              type="text"
              value={newSessionName}
              onChange={(e) => {
                setNewSessionName(e.target.value);
                if (newSessionError) setNewSessionError('');
              }}
              placeholder="Enter chat name..."
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent mb-4"
              autoFocus
            />
            {newSessionError && (
              <p className="text-red-600 text-sm mb-4">{newSessionError}</p>
            )}
            <div className="flex space-x-3">
              <button
                onClick={() => {
                  setShowNewSessionModal(false);
                  setNewSessionName('');
                  setNewSessionError('');
                }}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={() => createNewSession(newSessionName)}
                disabled={!newSessionName.trim()}
                className="flex-1 px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                Create
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Upload File Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Upload Dataset</h2>
            
            <div className="space-y-4">
              {!selectedFile ? (
                <div 
                  onClick={() => fileInputRef.current?.click()}
                  className="w-full p-8 border-2 border-dashed border-gray-300 rounded-lg text-center cursor-pointer hover:border-gray-400 transition-colors"
                >
                  <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                  <p className="text-gray-600">Click to select a file</p>
                  <p className="text-sm text-gray-500 mt-1">CSV, JSON, TXT, etc.</p>
                </div>
              ) : (
                <div className="p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <File className="w-5 h-5 text-gray-600" />
                    <div>
                      <div className="font-medium text-gray-900">{selectedFile.name}</div>
                      <div className="text-sm text-gray-500">
                        {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              <input
                ref={fileInputRef}
                type="file"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) {
                    setSelectedFile(file);
                    setFileName(file.name.split('.')[0]);
                  }
                }}
                className="hidden"
                accept=".csv,.json,.txt,.xlsx,.xls"
              />

              <input
                type="text"
                value={fileName}
                onChange={(e) => setFileName(e.target.value)}
                placeholder="Dataset name..."
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
              />

              <textarea
                value={fileDescription}
                onChange={(e) => setFileDescription(e.target.value)}
                placeholder="Description (optional)..."
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent resize-none"
                rows={3}
              />

              {uploadingFile && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Uploading...</span>
                    <span>{uploadProgress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-gray-900 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                </div>
              )}

              {uploadError && (
                <p className="text-red-600 text-sm">{uploadError}</p>
              )}
            </div>

            <div className="flex space-x-3 mt-6">
              <button
                onClick={() => {
                  setShowUploadModal(false);
                  setSelectedFile(null);
                  setFileName('');
                  setFileDescription('');
                  setUploadError('');
                }}
                disabled={uploadingFile}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:opacity-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={uploadFile}
                disabled={!selectedFile || !fileName.trim() || uploadingFile}
                className="flex-1 px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {uploadingFile ? 'Uploading...' : 'Upload'}
              </button>
            </div>
          </div>
        </div>
      )}
      

      {/* Delete Session Confirmation Modal */}
      {showDeleteSessionModal && sessionToDelete && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md mx-4 animate-modal-in">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Delete Session</h2>
            <p className="text-gray-600 mb-6">
              Are you sure you want to delete the session <strong>&ldquo;{sessionToDelete.title}&rdquo;</strong>? 
              This action cannot be undone and all messages in this session will be permanently lost.
            </p>
            <div className="flex space-x-3">
              <button
                onClick={() => {
                  setShowDeleteSessionModal(false);
                  setSessionToDelete(null);
                }}
                disabled={deletingSession}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:opacity-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={confirmDeleteSession}
                disabled={deletingSession}
                className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-red-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
              >
                {deletingSession ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Deleting...
                  </>
                ) : (
                  'Delete Session'
                )}
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Delete File Confirmation Modal */}
      {showDeleteFileModal && fileToDelete && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md mx-4 animate-modal-in">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Delete File</h2>
            <p className="text-gray-600 mb-6">
              Are you sure you want to delete the file <strong>&ldquo;{fileToDelete.file_name}&rdquo;</strong>? 
              This action cannot be undone and the file will be permanently removed from your account.
            </p>
            <div className="flex space-x-3">
              <button
                onClick={() => {
                  setShowDeleteFileModal(false);
                  setFileToDelete(null);
                }}
                disabled={deletingFile}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:opacity-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={confirmDeleteFile}
                disabled={deletingFile}
                className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-red-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
              >
                {deletingFile ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Deleting...
                  </>
                ) : (
                  'Delete File'
                )}
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Enhanced CSS Animations */}
      <style jsx>{`
        @keyframes fade-in {
          from { 
            opacity: 0; 
            transform: translateY(10px); 
          }
          to { 
            opacity: 1; 
            transform: translateY(0); 
          }
        }
        
        @keyframes slide-in {
          from { 
            opacity: 0; 
            transform: translateX(-10px); 
          }
          to { 
            opacity: 1; 
            transform: translateX(0); 
          }
        }
        
        @keyframes modal-in {
          from { 
            opacity: 0; 
            transform: scale(0.95) translateY(10px); 
          }
          to { 
            opacity: 1; 
            transform: scale(1) translateY(0); 
          }
        }
        
        .animate-fade-in {
          animation: fade-in 0.6s ease-out forwards;
        }
        
        .animate-slide-in {
          animation: slide-in 0.5s ease-out forwards;
        }
        
        .animate-modal-in {
          animation: modal-in 0.3s ease-out forwards;
        }
        
        /* Custom scrollbar */
        .overflow-y-auto::-webkit-scrollbar {
          width: 6px;
        }
        
        .overflow-y-auto::-webkit-scrollbar-track {
          background: transparent;
        }
        
        .overflow-y-auto::-webkit-scrollbar-thumb {
          background: rgba(148, 163, 184, 0.4);
          border-radius: 3px;
        }
        
        .overflow-y-auto::-webkit-scrollbar-thumb:hover {
          background: rgba(148, 163, 184, 0.6);
        }
        
        /* Backdrop blur for better glass effect */
        .backdrop-blur-sm {
          backdrop-filter: blur(8px);
        }
        
        .backdrop-blur-md {
          backdrop-filter: blur(12px);
        }
        
        .backdrop-blur-xl {
          backdrop-filter: blur(20px);
        }
      `}</style>
    </div>
  );
};

export default ChatPage;