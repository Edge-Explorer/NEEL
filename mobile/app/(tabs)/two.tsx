import React, { useState, useRef, useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  Animated
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, SPACING } from '../../constants/Theme';
import { Brain, Sparkles, Send, ShieldCheck, User } from 'lucide-react-native';
import apiClient from '../../services/api';

interface Message {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
  status?: 'sending' | 'sent' | 'error';
  thinkingSteps?: string[];
}

export default function IntelligenceScreen() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [thinkingStep, setThinkingStep] = useState(0);
  const scrollViewRef = useRef<ScrollView>(null);
  const typingOpacity = useRef(new Animated.Value(0)).current;

  const thinkingSteps = [
    "🔍 Evaluating logged activity...",
    "🧠 Brainstorming personalized advice...",
    "🛡️ Performing safety audit...",
    "✨ Finalizing guidance..."
  ];

  useEffect(() => {
    let interval: any;
    if (loading) {
      setThinkingStep(0);
      interval = setInterval(() => {
        setThinkingStep(prev => (prev < thinkingSteps.length - 1 ? prev + 1 : prev));
      }, 2000);

      Animated.loop(
        Animated.sequence([
          Animated.timing(typingOpacity, {
            toValue: 1,
            duration: 600,
            useNativeDriver: true,
          }),
          Animated.timing(typingOpacity, {
            toValue: 0.3,
            duration: 600,
            useNativeDriver: true,
          }),
        ])
      ).start();
    } else {
      typingOpacity.setValue(0);
      if (interval) clearInterval(interval);
    }
    return () => { if (interval) clearInterval(interval); };
  }, [loading]);

  const handleSendMessage = async () => {
    if (!query.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: query.trim(),
      timestamp: new Date(),
      status: 'sending'
    };

    setMessages(prev => [...prev, userMessage]);
    setQuery('');
    setLoading(true);

    // Scroll to bottom
    setTimeout(() => {
      scrollViewRef.current?.scrollToEnd({ animated: true });
    }, 100);

    try {
      const response = await apiClient.post('/api/intelligence/analyze', {
        query: userMessage.content
      });

      // Update user message status
      setMessages(prev => prev.map(msg =>
        msg.id === userMessage.id ? { ...msg, status: 'sent' } : msg
      ));

      // Add AI response
      const aiContent = response.data.analysis || response.data.message || "I've analyzed your data, but couldn't generate a specific response. Try logging more activities!";

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: aiContent,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);

      // Scroll to bottom
      setTimeout(() => {
        scrollViewRef.current?.scrollToEnd({ animated: true });
      }, 100);

    } catch (error) {
      console.error('Analysis failed:', error);

      // Update user message status to error
      setMessages(prev => prev.map(msg =>
        msg.id === userMessage.id ? { ...msg, status: 'error' } : msg
      ));

      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: "I apologize, but I encountered an error processing your request. Please try again.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const renderMessage = (message: Message) => {
    const isUser = message.type === 'user';

    return (
      <View
        key={message.id}
        style={[
          styles.messageContainer,
          isUser ? styles.userMessageContainer : styles.aiMessageContainer
        ]}
      >
        {!isUser && (
          <View style={styles.aiAvatar}>
            <Brain color={COLORS.secondary} size={20} />
          </View>
        )}

        <View style={[
          styles.messageBubble,
          isUser ? styles.userBubble : styles.aiBubble
        ]}>
          {!isUser && (
            <Text style={styles.aiLabel}>NEEL AI</Text>
          )}
          <Text style={[
            styles.messageText,
            isUser ? styles.userMessageText : styles.aiMessageText
          ]}>
            {message.content}
          </Text>
          <Text style={[
            styles.timestamp,
            isUser ? styles.userTimestamp : styles.aiTimestamp
          ]}>
            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            {isUser && message.status === 'sending' && ' • Sending...'}
            {isUser && message.status === 'error' && ' • Failed'}
          </Text>
        </View>

        {isUser && (
          <View style={styles.userAvatar}>
            <User color="#fff" size={20} />
          </View>
        )}
      </View>
    );
  };

  const renderTypingIndicator = () => (
    <Animated.View style={[styles.messageContainer, styles.aiMessageContainer, { opacity: typingOpacity }]}>
      <View style={styles.aiAvatar}>
        <Brain color={COLORS.secondary} size={20} />
      </View>
      <View style={[styles.messageBubble, styles.aiBubble, styles.typingBubble]}>
        <View style={styles.thinkingStepsContainer}>
          <ActivityIndicator size="small" color={COLORS.secondary} style={{ marginRight: 10 }} />
          <Text style={styles.typingText}>{thinkingSteps[thinkingStep]}</Text>
        </View>
        <View style={styles.typingDots}>
          <View style={styles.dot} />
          <View style={styles.dot} />
          <View style={styles.dot} />
        </View>
      </View>
    </Animated.View>
  );

  return (
    <LinearGradient colors={['#0F172A', '#050505']} style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={{ flex: 1 }}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
      >
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.aiBadge}>
            <Sparkles color={COLORS.secondary} size={16} />
            <Text style={styles.aiBadgeText}>Quantum Reasoning Engine</Text>
          </View>
          <Text style={styles.title}>AI Intelligence</Text>
        </View>

        {/* Messages Area */}
        <ScrollView
          ref={scrollViewRef}
          style={styles.messagesArea}
          contentContainerStyle={styles.messagesContent}
          showsVerticalScrollIndicator={false}
        >
          {messages.length === 0 ? (
            <View style={styles.emptyState}>
              <Brain color={COLORS.surfaceLight} size={80} strokeWidth={1} />
              <Text style={styles.emptyText}>
                Hi! I'm NEEL, your AI life coach. Ask me anything about your productivity, goals, or habits.
              </Text>
              <View style={styles.suggestionsContainer}>
                <TouchableOpacity
                  style={styles.suggestionChip}
                  onPress={() => setQuery("What should be my priorities for today?")}
                >
                  <Text style={styles.suggestionText}>📋 Today's priorities</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={styles.suggestionChip}
                  onPress={() => setQuery("How can I improve my productivity?")}
                >
                  <Text style={styles.suggestionText}>⚡ Boost productivity</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={styles.suggestionChip}
                  onPress={() => setQuery("Analyze my recent progress")}
                >
                  <Text style={styles.suggestionText}>📊 Check progress</Text>
                </TouchableOpacity>
              </View>
            </View>
          ) : (
            <>
              {messages.map(renderMessage)}
              {loading && renderTypingIndicator()}
            </>
          )}
        </ScrollView>

        {/* Input Area */}
        <View style={styles.inputContainer}>
          <View style={styles.inputWrapper}>
            <TextInput
              style={styles.input}
              placeholder="Ask NEEL anything..."
              placeholderTextColor={COLORS.textSecondary}
              value={query}
              onChangeText={setQuery}
              multiline
              maxLength={500}
              onSubmitEditing={handleSendMessage}
            />
            <TouchableOpacity
              style={[styles.sendButton, (!query.trim() || loading) && styles.sendButtonDisabled]}
              onPress={handleSendMessage}
              disabled={!query.trim() || loading}
            >
              <LinearGradient
                colors={query.trim() && !loading ? [COLORS.secondary, '#0891B2'] : ['#334155', '#1E293B']}
                style={styles.sendGradient}
              >
                <Send color="#fff" size={20} />
              </LinearGradient>
            </TouchableOpacity>
          </View>
        </View>
      </KeyboardAvoidingView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    paddingHorizontal: SPACING.lg,
    paddingTop: 60,
    paddingBottom: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255, 255, 255, 0.05)',
  },
  aiBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(6, 182, 212, 0.1)',
    alignSelf: 'flex-start',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    marginBottom: 8,
    borderWidth: 1,
    borderColor: 'rgba(6, 182, 212, 0.2)',
  },
  aiBadgeText: {
    color: COLORS.secondary,
    fontSize: 12,
    fontWeight: '700',
    marginLeft: 6,
    textTransform: 'uppercase',
  },
  title: {
    fontSize: 28,
    color: '#fff',
    fontWeight: '900',
  },
  messagesArea: {
    flex: 1,
  },
  messagesContent: {
    padding: SPACING.lg,
    paddingBottom: SPACING.xl,
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: SPACING.xxl,
    paddingHorizontal: SPACING.lg,
  },
  emptyText: {
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginTop: 20,
    fontSize: 16,
    lineHeight: 24,
    marginBottom: SPACING.xl,
  },
  suggestionsContainer: {
    gap: SPACING.sm,
    width: '100%',
  },
  suggestionChip: {
    backgroundColor: 'rgba(6, 182, 212, 0.1)',
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: 'rgba(6, 182, 212, 0.2)',
  },
  suggestionText: {
    color: COLORS.secondary,
    fontSize: 14,
    fontWeight: '600',
  },
  messageContainer: {
    flexDirection: 'row',
    marginBottom: SPACING.md,
    alignItems: 'flex-end',
  },
  userMessageContainer: {
    justifyContent: 'flex-end',
  },
  aiMessageContainer: {
    justifyContent: 'flex-start',
  },
  aiAvatar: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: 'rgba(6, 182, 212, 0.15)',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.sm,
    borderWidth: 1,
    borderColor: 'rgba(6, 182, 212, 0.3)',
  },
  userAvatar: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: SPACING.sm,
  },
  messageBubble: {
    maxWidth: '75%',
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    borderRadius: 20,
  },
  userBubble: {
    backgroundColor: COLORS.primary,
    borderBottomRightRadius: 4,
  },
  aiBubble: {
    backgroundColor: COLORS.surface,
    borderBottomLeftRadius: 4,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.05)',
  },
  aiLabel: {
    color: COLORS.secondary,
    fontSize: 11,
    fontWeight: '700',
    marginBottom: 4,
    textTransform: 'uppercase',
  },
  messageText: {
    fontSize: 15,
    lineHeight: 22,
  },
  userMessageText: {
    color: '#fff',
  },
  aiMessageText: {
    color: COLORS.text,
  },
  timestamp: {
    fontSize: 11,
    marginTop: 4,
  },
  userTimestamp: {
    color: 'rgba(255, 255, 255, 0.6)',
    textAlign: 'right',
  },
  aiTimestamp: {
    color: COLORS.textSecondary,
  },
  typingBubble: {
    paddingVertical: SPACING.md,
    minWidth: 200,
  },
  thinkingStepsContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  typingDots: {
    flexDirection: 'row',
    gap: 6,
    marginBottom: 6,
  },
  dot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: COLORS.secondary,
  },
  typingText: {
    color: COLORS.textSecondary,
    fontSize: 12,
    fontStyle: 'italic',
  },
  inputContainer: {
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    borderTopWidth: 1,
    borderTopColor: 'rgba(255, 255, 255, 0.05)',
    backgroundColor: '#0F172A',
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    backgroundColor: COLORS.surface,
    borderRadius: 24,
    padding: 8,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.1)',
  },
  input: {
    flex: 1,
    color: '#fff',
    fontSize: 16,
    paddingHorizontal: 16,
    paddingVertical: 12,
    maxHeight: 120,
  },
  sendButton: {
    width: 48,
    height: 48,
    borderRadius: 20,
    overflow: 'hidden',
  },
  sendButtonDisabled: {
    opacity: 0.5,
  },
  sendGradient: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
