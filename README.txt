
import React, { useState, useEffect } from "react";
import { StudySession, Task, Exam, MoodEntry, Flashcard } from "@/entities/all";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { createPageUrl } from "@/utils";
import { 
  Clock, 
  Target, 
  Calendar, 
  TrendingUp, 
  BookOpen, 
  Brain,
  Heart,
  Users,
  Plus,
  ArrowRight,
  BarChart3 // Added BarChart3 import
} from "lucide-react";
import { format, isToday, differenceInDays, startOfWeek, endOfWeek } from "date-fns";
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer, BarChart, Bar } from "recharts";

export default function Dashboard() {
  const [studySessions, setStudySessions] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [exams, setExams] = useState([]);
  const [moodEntries, setMoodEntries] = useState([]);
  const [flashcards, setFlashcards] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [sessionsData, tasksData, examsData, moodData, flashcardsData] = await Promise.all([
        StudySession.list("-created_date", 50),
        Task.list("-created_date", 20),
        Exam.list("exam_date", 10),
        MoodEntry.list("-created_date", 30),
        Flashcard.list("-created_date", 100)
      ]);

      setStudySessions(sessionsData);
      setTasks(tasksData);
      setExams(examsData);
      setMoodEntries(moodData);
      setFlashcards(flashcardsData);
    } catch (error) {
      console.error("Error loading data:", error);
    }
    setIsLoading(false);
  };

  const getWeeklyStats = () => {
    const weekStart = startOfWeek(new Date());
    const weekEnd = endOfWeek(new Date());
    
    const thisWeekSessions = studySessions.filter(session => {
      const sessionDate = new Date(session.date);
      return sessionDate >= weekStart && sessionDate <= weekEnd;
    });

    const totalMinutes = thisWeekSessions.reduce((sum, session) => sum + session.duration_minutes, 0);
    const avgProductivity = thisWeekSessions.length > 0 
      ? thisWeekSessions.reduce((sum, session) => sum + session.productivity_rating, 0) / thisWeekSessions.length 
      : 0;

    return { totalMinutes, avgProductivity, sessionCount: thisWeekSessions.length };
  };

  const getUpcomingExams = () => {
    return exams
      .filter(exam => new Date(exam.exam_date) >= new Date())
      .sort((a, b) => new Date(a.exam_date) - new Date(b.exam_date))
      .slice(0, 3);
  };

  const getTodaysTasks = () => {
    return tasks.filter(task => 
      isToday(new Date(task.due_date)) && task.status !== 'completed'
    );
  };

  const getRecentMood = () => {
    return moodEntries[0] || null;
  };

  const { totalMinutes, avgProductivity, sessionCount } = getWeeklyStats();
  const upcomingExams = getUpcomingExams();
  const todaysTasks = getTodaysTasks();
  const recentMood = getRecentMood();

  if (isLoading) {
    return (
      <div className="p-6 space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-slate-200 dark:bg-slate-700 rounded w-64 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {Array(4).fill(0).map((_, i) => (
              <div key={i} className="h-32 bg-slate-200 dark:bg-slate-800 rounded-xl"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-50">Welcome back!</h1>
          <p className="text-slate-600 dark:text-slate-400 mt-1">Here's your study overview for today</p>
        </div>
        <Link to={createPageUrl("AIChat")}>
          <Button className="bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 shadow-lg">
            <Brain className="w-4 h-4 mr-2" />
            Ask AI for Help
          </Button>
        </Link>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="border-none shadow-lg bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-slate-800 dark:to-slate-900 dark:shadow-none dark:border dark:border-slate-700/60">
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-slate-700 dark:text-slate-300">This Week</CardTitle>
              <Clock className="w-5 h-5 text-blue-500" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-slate-900 dark:text-slate-50">{Math.floor(totalMinutes / 60)}h {totalMinutes % 60}m</div>
            <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">{sessionCount} study sessions</p>
          </CardContent>
        </Card>

        <Card className="border-none shadow-lg bg-gradient-to-br from-green-50 to-emerald-50 dark:from-slate-800 dark:to-green-950/30 dark:shadow-none dark:border dark:border-slate-700/60">
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-slate-700 dark:text-slate-300">Productivity</CardTitle>
              <TrendingUp className="w-5 h-5 text-green-500" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-slate-900 dark:text-slate-50">{avgProductivity.toFixed(1)}/5</div>
            <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">Average this week</p>
          </CardContent>
        </Card>

        <Card className="border-none shadow-lg bg-gradient-to-br from-orange-50 to-red-50 dark:from-slate-800 dark:to-orange-950/30 dark:shadow-none dark:border dark:border-slate-700/60">
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-slate-700 dark:text-slate-300">Next Exam</CardTitle>
              <Target className="w-5 h-5 text-orange-500" />
            </div>
          </CardHeader>
          <CardContent>
            {upcomingExams[0] ? (
              <>
                <div className="text-2xl font-bold text-slate-900 dark:text-slate-50">
                  {differenceInDays(new Date(upcomingExams[0].exam_date), new Date())} days
                </div>
                <p className="text-sm text-slate-600 dark:text-slate-400 mt-1 truncate">{upcomingExams[0].subject}</p>
              </>
            ) : (
              <div className="text-2xl font-bold text-slate-900 dark:text-slate-50">-</div>
            )}
          </CardContent>
        </Card>

        <Card className="border-none shadow-lg bg-gradient-to-br from-purple-50 to-pink-50 dark:from-slate-800 dark:to-purple-950/30 dark:shadow-none dark:border dark:border-slate-700/60">
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-slate-700 dark:text-slate-300">Today's Mood</CardTitle>
              <Heart className="w-5 h-5 text-purple-500" />
            </div>
          </CardHeader>
          <CardContent>
            {recentMood ? (
              <>
                <div className="text-2xl font-bold text-slate-900 dark:text-slate-50">{recentMood.mood_score}/10</div>
                <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">Feeling good!</p>
              </>
            ) : (
              <div className="text-2xl font-bold text-slate-900 dark:text-slate-50">-</div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Main Content Grid */}
      <div className="grid lg:grid-cols-3 gap-8">
        {/* Left Column */}
        <div className="lg:col-span-2 space-y-6">
          {/* Today's Tasks */}
          <Card className="border-none shadow-lg bg-white dark:bg-slate-800 dark:shadow-none dark:border dark:border-slate-700/60">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2 text-slate-900 dark:text-slate-100">
                  <Calendar className="w-5 h-5 text-blue-500" />
                  Today's Tasks
                </CardTitle>
                <Link to={createPageUrl("Planner")}>
                  <Button variant="outline" size="sm" className="bg-transparent dark:bg-slate-700/50 dark:text-slate-300 dark:border-slate-600 dark:hover:bg-slate-700">
                    View All <ArrowRight className="w-4 h-4 ml-1" />
                  </Button>
                </Link>
              </div>
            </CardHeader>
            <CardContent>
              {todaysTasks.length > 0 ? (
                <div className="space-y-3">
                  {todaysTasks.slice(0, 3).map(task => (
                    <div key={task.id} className="flex items-center gap-3 p-3 bg-slate-50 dark:bg-slate-700/50 rounded-lg">
                      <div className={`w-3 h-3 rounded-full ${
                        task.priority === 'urgent' ? 'bg-red-500' :
                        task.priority === 'high' ? 'bg-orange-500' :
                        task.priority === 'medium' ? 'bg-yellow-500' : 'bg-green-500'
                      }`} />
                      <div className="flex-1">
                        <p className="font-medium text-slate-900 dark:text-slate-100">{task.title}</p>
                        <p className="text-sm text-slate-600 dark:text-slate-400">{task.subject}</p>
                      </div>
                      <span className="text-xs bg-slate-200 dark:bg-slate-600 dark:text-slate-300 px-2 py-1 rounded-full">
                        {task.estimated_duration}min
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-slate-600 dark:text-slate-400 text-center py-8">No tasks due today! 🎉</p>
              )}
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card className="border-none shadow-lg bg-white dark:bg-slate-800 dark:shadow-none dark:border dark:border-slate-700/60">
            <CardHeader>
              <CardTitle className="text-slate-900 dark:text-slate-100">Quick Actions</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4">
                <Link to={createPageUrl("Planner")}>
                  <Button variant="outline" className="w-full h-16 flex-col bg-transparent text-slate-700 dark:bg-slate-700/50 dark:text-slate-300 dark:border-slate-600 dark:hover:bg-slate-700">
                    <Plus className="w-5 h-5 mb-1" />
                    Add Task
                  </Button>
                </Link>
                <Link to={createPageUrl("Flashcards")}>
                  <Button variant="outline" className="w-full h-16 flex-col bg-transparent text-slate-700 dark:bg-slate-700/50 dark:text-slate-300 dark:border-slate-600 dark:hover:bg-slate-700">
                    <BookOpen className="w-5 h-5 mb-1" />
                    Study Cards
                  </Button>
                </Link>
                <Link to={createPageUrl("StudyGroups")}>
                  <Button variant="outline" className="w-full h-16 flex-col bg-transparent text-slate-700 dark:bg-slate-700/50 dark:text-slate-300 dark:border-slate-600 dark:hover:bg-slate-700">
                    <Users className="w-5 h-5 mb-1" />
                    Find Group
                  </Button>
                </Link>
                <Link to={createPageUrl("MoodTracker")}>
                  <Button variant="outline" className="w-full h-16 flex-col bg-transparent text-slate-700 dark:bg-slate-700/50 dark:text-slate-300 dark:border-slate-600 dark:hover:bg-slate-700">
                    <Heart className="w-5 h-5 mb-1" />
                    Track Mood
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Upcoming Exams */}
          <Card className="border-none shadow-lg bg-white dark:bg-slate-800 dark:shadow-none dark:border dark:border-slate-700/60">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2 text-slate-900 dark:text-slate-100">
                  <Target className="w-5 h-5 text-orange-500" />
                  Upcoming Exams
                </CardTitle>
                <Link to={createPageUrl("Exams")}>
                  <Button variant="outline" size="sm" className="bg-transparent dark:bg-slate-700/50 dark:text-slate-300 dark:border-slate-600 dark:hover:bg-slate-700">View All</Button>
                </Link>
              </div>
            </CardHeader>
            <CardContent>
              {upcomingExams.length > 0 ? (
                <div className="space-y-3">
                  {upcomingExams.map(exam => (
                    <div key={exam.id} className="p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-100 dark:border-orange-800/50">
                      <div className="flex items-start justify-between">
                        <div>
                          <p className="font-medium text-slate-900 dark:text-slate-100">{exam.subject}</p>
                          <p className="text-sm text-slate-600 dark:text-slate-400">{exam.exam_name}</p>
                          <p className="text-xs text-orange-600 dark:text-orange-400 font-medium mt-1">
                            {format(new Date(exam.exam_date), "MMM d, yyyy")}
                          </p>
                        </div>
                        <span className="text-lg font-bold text-orange-600 dark:text-orange-400">
                          {differenceInDays(new Date(exam.exam_date), new Date())}d
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-slate-600 dark:text-slate-400 text-center py-4">No upcoming exams</p>
              )}
            </CardContent>
          </Card>

          {/* Study Stats */}
          <Card className="border-none shadow-lg bg-white dark:bg-slate-800 dark:shadow-none dark:border dark:border-slate-700/60">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-slate-900 dark:text-slate-100">
                <BarChart3 className="w-5 h-5 text-blue-500" />
                Weekly Progress
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-600 dark:text-slate-400">Total Flashcards</span>
                  <span className="font-semibold text-slate-900 dark:text-slate-200">{flashcards.length}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-600 dark:text-slate-400">Completed Tasks</span>
                  <span className="font-semibold text-green-600 dark:text-green-400">{tasks.filter(t => t.status === 'completed').length}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-600 dark:text-slate-400">Study Sessions</span>
                  <span className="font-semibold text-slate-900 dark:text-slate-200">{sessionCount}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

import React, { useState, useRef, useEffect } from "react";
import { InvokeLLM } from "@/integrations/Core";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Send, Bot, User, Sparkles, BookOpen, Calculator, Lightbulb } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const STUDY_PROMPTS = [
  {
    icon: BookOpen,
    title: "Explain a concept",
    prompt: "Can you explain [topic] in simple terms with examples?"
  },
  {
    icon: Calculator,
    title: "Solve a problem",
    prompt: "Help me solve this step by step: [problem]"
  },
  {
    icon: Lightbulb,
    title: "Study tips",
    prompt: "What are the best study techniques for [subject]?"
  },
  {
    icon: Sparkles,
    title: "Quiz me",
    prompt: "Create a practice quiz on [topic] with 5 questions"
  }
];

export default function AIChat() {
  const [messages, setMessages] = useState([
    {
      type: 'assistant',
      content: "Hi! I'm your AI study assistant. I can help you understand concepts, solve problems, create study plans, and much more. What would you like to study today?",
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (messageText) => {
    if (!messageText.trim() || isLoading) return;

    const userMessage = {
      type: 'user',
      content: messageText,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await InvokeLLM({
        prompt: `You are an AI study assistant helping a student. Be helpful, encouraging, and educational. Break down complex topics into digestible parts. Use examples and analogies when helpful. 

Student question: ${messageText}

Please provide a comprehensive, helpful response that aids their learning.`,
        add_context_from_internet: true
      });

      const assistantMessage = {
        type: 'assistant',
        content: response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error getting AI response:", error);
      const errorMessage = {
        type: 'assistant',
        content: "I'm sorry, I encountered an error. Please try asking your question again.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    }

    setIsLoading(false);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(input);
  };

  const handlePromptClick = (prompt) => {
    setInput(prompt);
    inputRef.current?.focus();
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-900 dark:via-slate-900 dark:to-blue-950">
      {/* Header */}
      <div className="bg-white/90 dark:bg-slate-900/90 backdrop-blur-sm border-b border-slate-200/60 dark:border-slate-700/60 p-6 shadow-sm">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-50">AI Study Assistant</h1>
              <p className="text-slate-600 dark:text-slate-400">Get instant help with your studies</p>
            </div>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-auto p-6">
        <div className="max-w-4xl mx-auto space-y-6">
          {/* Quick Prompts - Show only at the beginning */}
          {messages.length <= 1 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8"
            >
              {STUDY_PROMPTS.map((prompt, index) => (
                <Card
                  key={index}
                  className="p-4 cursor-pointer hover:shadow-lg dark:hover:bg-slate-700 transition-all duration-200 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-slate-200/60 dark:border-slate-700/60"
                  onClick={() => handlePromptClick(prompt.prompt)}
                >
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-100 to-indigo-100 dark:from-blue-900/50 dark:to-indigo-900/50 rounded-lg flex items-center justify-center">
                      <prompt.icon className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-slate-900 dark:text-slate-100">{prompt.title}</h3>
                      <p className="text-sm text-slate-600 dark:text-slate-400">{prompt.prompt}</p>
                    </div>
                  </div>
                </Card>
              ))}
            </motion.div>
          )}

          {/* Chat Messages */}
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex gap-4 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {message.type === 'assistant' && (
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                )}
                
                <div className={`max-w-3xl ${message.type === 'user' ? 'order-first' : ''}`}>
                  <Card className={`p-4 ${
                    message.type === 'user' 
                      ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white border-none' 
                      : 'bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm border-slate-200/60 dark:border-slate-700/60 text-slate-800 dark:text-slate-200'
                  }`}>
                    <div className="whitespace-pre-wrap">{message.content}</div>
                    <div className={`text-xs mt-2 opacity-70 ${
                      message.type === 'user' ? 'text-blue-100' : 'text-slate-500 dark:text-slate-400'
                    }`}>
                      {message.timestamp.toLocaleTimeString()}
                    </div>
                  </Card>
                </div>

                {message.type === 'user' && (
                  <div className="w-8 h-8 bg-gradient-to-br from-slate-400 to-slate-600 dark:from-slate-600 dark:to-slate-700 rounded-full flex items-center justify-center flex-shrink-0">
                    <User className="w-4 h-4 text-white" />
                  </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Loading indicator */}
          {isLoading && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex gap-4 justify-start"
            >
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center">
                <Bot className="w-4 h-4 text-white" />
              </div>
              <Card className="p-4 bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm border-slate-200/60 dark:border-slate-700/60">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-slate-400 dark:bg-slate-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-slate-400 dark:bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-slate-400 dark:bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </Card>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="bg-white/90 dark:bg-slate-900/90 backdrop-blur-sm border-t border-slate-200/60 dark:border-slate-700/60 p-6">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="flex gap-4">
            <Input
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me anything about your studies..."
              className="flex-1 bg-white/80 dark:bg-slate-800 border-slate-200/60 dark:border-slate-700 text-slate-900 dark:text-slate-100 placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:ring-2 focus:ring-blue-500/20"
              disabled={isLoading}
            />
            <Button 
              type="submit" 
              disabled={isLoading || !input.trim()}
              className="bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 shadow-lg"
            >
              <Send className="w-4 h-4" />
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}

import React, { useState, useEffect } from "react";
import { Task } from "@/entities/Task";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Calendar, Plus, Filter } from "lucide-react";
import { format, startOfWeek, endOfWeek, startOfMonth, endOfMonth, isToday, parseISO } from "date-fns";

import TaskForm from "../components/planner/TaskForm";
import TaskList from "../components/planner/TaskList";
import WeekView from "../components/planner/WeekView";
import MonthView from "../components/planner/MonthView";

export default function Planner() {
  const [tasks, setTasks] = useState([]);
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [activeView, setActiveView] = useState("day");
  const [selectedDate, setSelectedDate] = useState(new Date());

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    const data = await Task.list("-due_date", 100);
    setTasks(data);
  };

  const handleTaskSubmit = async (taskData) => {
    if (editingTask) {
      await Task.update(editingTask.id, taskData);
    } else {
      await Task.create(taskData);
    }
    setShowTaskForm(false);
    setEditingTask(null);
    loadTasks();
  };

  const handleTaskUpdate = async (taskId, updates) => {
    await Task.update(taskId, updates);
    loadTasks();
  };

  const handleTaskDelete = async (taskId) => {
    await Task.delete(taskId);
    loadTasks();
  };

  const getFilteredTasks = () => {
    const now = new Date();
    switch (activeView) {
      case "day":
        return tasks.filter(task => isToday(parseISO(task.due_date)));
      case "week":
        const weekStart = startOfWeek(selectedDate);
        const weekEnd = endOfWeek(selectedDate);
        return tasks.filter(task => {
          const taskDate = parseISO(task.due_date);
          return taskDate >= weekStart && taskDate <= weekEnd;
        });
      case "month":
        const monthStart = startOfMonth(selectedDate);
        const monthEnd = endOfMonth(selectedDate);
        return tasks.filter(task => {
          const taskDate = parseISO(task.due_date);
          return taskDate >= monthStart && taskDate <= monthEnd;
        });
      default:
        return tasks;
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-50">Study Planner</h1>
          <p className="text-slate-600 dark:text-slate-400 mt-1">Organize your tasks and assignments</p>
        </div>
        <Button
          onClick={() => setShowTaskForm(true)}
          className="bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 shadow-lg"
        >
          <Plus className="w-4 h-4 mr-2" />
          Add Task
        </Button>
      </div>

      <div className="grid lg:grid-cols-4 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-3">
          <Tabs value={activeView} onValueChange={setActiveView} className="w-full">
            <TabsList className="grid w-full grid-cols-3 mb-6 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
              <TabsTrigger value="day" className="data-[state=active]:bg-white data-[state=active]:text-slate-900 data-[state=active]:shadow-md dark:data-[state=active]:bg-slate-700 dark:data-[state=active]:text-slate-100">Today</TabsTrigger>
              <TabsTrigger value="week" className="data-[state=active]:bg-white data-[state=active]:text-slate-900 data-[state=active]:shadow-md dark:data-[state=active]:bg-slate-700 dark:data-[state=active]:text-slate-100">This Week</TabsTrigger>
              <TabsTrigger value="month" className="data-[state=active]:bg-white data-[state=active]:text-slate-900 data-[state=active]:shadow-md dark:data-[state=active]:bg-slate-700 dark:data-[state=active]:text-slate-100">This Month</TabsTrigger>
            </TabsList>

            <TabsContent value="day">
              <Card className="border-none shadow-lg bg-white dark:bg-slate-800 dark:shadow-none dark:border dark:border-slate-700/60">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-slate-900 dark:text-slate-100">
                    <Calendar className="w-5 h-5 text-blue-500" />
                    Today's Tasks - {format(new Date(), "MMMM d, yyyy")}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <TaskList 
                    tasks={getFilteredTasks()}
                    onTaskUpdate={handleTaskUpdate}
                    onTaskEdit={setEditingTask}
                    onTaskDelete={handleTaskDelete}
                  />
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="week">
              <WeekView 
                tasks={getFilteredTasks()}
                selectedDate={selectedDate}
                onTaskUpdate={handleTaskUpdate}
                onTaskEdit={setEditingTask}
              />
            </TabsContent>

            <TabsContent value="month">
              <MonthView 
                tasks={getFilteredTasks()}
                selectedDate={selectedDate}
                onDateSelect={setSelectedDate}
                onTaskUpdate={handleTaskUpdate}
              />
            </TabsContent>
          </Tabs>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Stats */}
          <Card className="border-none shadow-lg bg-white dark:bg-slate-800 dark:shadow-none dark:border dark:border-slate-700/60">
            <CardHeader>
              <CardTitle className="text-lg text-slate-900 dark:text-slate-100">Quick Stats</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between">
                <span className="text-slate-600 dark:text-slate-400">Total Tasks</span>
                <span className="font-semibold text-slate-900 dark:text-slate-200">{tasks.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-600 dark:text-slate-400">Completed</span>
                <span className="font-semibold text-green-600 dark:text-green-400">
                  {tasks.filter(t => t.status === 'completed').length}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-600 dark:text-slate-400">In Progress</span>
                <span className="font-semibold text-blue-600 dark:text-blue-400">
                  {tasks.filter(t => t.status === 'in_progress').length}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-600 dark:text-slate-400">Overdue</span>
                <span className="font-semibold text-red-600 dark:text-red-400">
                  {tasks.filter(t => t.status !== 'completed' && new Date(t.due_date) < new Date()).length}
                </span>
              </div>
            </CardContent>
          </Card>

          {/* Subject Breakdown */}
          <Card className="border-none shadow-lg bg-white dark:bg-slate-800 dark:shadow-none dark:border dark:border-slate-700/60">
            <CardHeader>
              <CardTitle className="text-lg text-slate-900 dark:text-slate-100">By Subject</CardTitle>
            </CardHeader>
            <CardContent>
              {Object.entries(
                tasks.reduce((acc, task) => {
                  const subject = task.subject || 'Other';
                  acc[subject] = (acc[subject] || 0) + 1;
                  return acc;
                }, {})
              ).map(([subject, count]) => (
                <div key={subject} className="flex justify-between items-center py-2">
                  <span className="text-slate-600 dark:text-slate-400">{subject}</span>
                  <span className="font-semibold text-slate-900 dark:text-slate-200">{count}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Task Form Modal */}
      {(showTaskForm || editingTask) && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-y-auto">
            <TaskForm
              task={editingTask}
              onSubmit={handleTaskSubmit}
              onCancel={() => {
                setShowTaskForm(false);
                setEditingTask(null);
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

import React, { useState, useEffect } from "react";
import { Task } from "@/entities/Task";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Calendar, Plus, Filter } from "lucide-react";
import { format, startOfWeek, endOfWeek, startOfMonth, endOfMonth, isToday, parseISO } from "date-fns";

import TaskForm from "../components/planner/TaskForm";
import TaskList from "../components/planner/TaskList";
import WeekView from "../components/planner/WeekView";
import MonthView from "../components/planner/MonthView";

export default function Planner() {
  const [tasks, setTasks] = useState([]);
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [activeView, setActiveView] = useState("day");
  const [selectedDate, setSelectedDate] = useState(new Date());

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    const data = await Task.list("-due_date", 100);
    setTasks(data);
  };

  const handleTaskSubmit = async (taskData) => {
    if (editingTask) {
      await Task.update(editingTask.id, taskData);
    } else {
      await Task.create(taskData);
    }
    setShowTaskForm(false);
    setEditingTask(null);
    loadTasks();
  };

  const handleTaskUpdate = async (taskId, updates) => {
    await Task.update(taskId, updates);
    loadTasks();
  };

  const handleTaskDelete = async (taskId) => {
    await Task.delete(taskId);
    loadTasks();
  };

  const getFilteredTasks = () => {
    const now = new Date();
    switch (activeView) {
      case "day":
        return tasks.filter(task => isToday(parseISO(task.due_date)));
      case "week":
        const weekStart = startOfWeek(selectedDate);
        const weekEnd = endOfWeek(selectedDate);
        return tasks.filter(task => {
          const taskDate = parseISO(task.due_date);
          return taskDate >= weekStart && taskDate <= weekEnd;
        });
      case "month":
        const monthStart = startOfMonth(selectedDate);
        const monthEnd = endOfMonth(selectedDate);
        return tasks.filter(task => {
          const taskDate = parseISO(task.due_date);
          return taskDate >= monthStart && taskDate <= monthEnd;
        });
      default:
        return tasks;
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-50">Study Planner</h1>
          <p className="text-slate-600 dark:text-slate-400 mt-1">Organize your tasks and assignments</p>
        </div>
        <Button
          onClick={() => setShowTaskForm(true)}
          className="bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 shadow-lg"
        >
          <Plus className="w-4 h-4 mr-2" />
          Add Task
        </Button>
      </div>

      <div className="grid lg:grid-cols-4 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-3">
          <Tabs value={activeView} onValueChange={setActiveView} className="w-full">
            <TabsList className="grid w-full grid-cols-3 mb-6 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
              <TabsTrigger value="day" className="data-[state=active]:bg-white data-[state=active]:text-slate-900 data-[state=active]:shadow-md dark:data-[state=active]:bg-slate-700 dark:data-[state=active]:text-slate-100">Today</TabsTrigger>
              <TabsTrigger value="week" className="data-[state=active]:bg-white data-[state=active]:text-slate-900 data-[state=active]:shadow-md dark:data-[state=active]:bg-slate-700 dark:data-[state=active]:text-slate-100">This Week</TabsTrigger>
              <TabsTrigger value="month" className="data-[state=active]:bg-white data-[state=active]:text-slate-900 data-[state=active]:shadow-md dark:data-[state=active]:bg-slate-700 dark:data-[state=active]:text-slate-100">This Month</TabsTrigger>
            </TabsList>

            <TabsContent value="day">
              <Card className="border-none shadow-lg bg-white dark:bg-slate-800 dark:shadow-none dark:border dark:border-slate-700/60">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-slate-900 dark:text-slate-100">
                    <Calendar className="w-5 h-5 text-blue-500" />
                    Today's Tasks - {format(new Date(), "MMMM d, yyyy")}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <TaskList 
                    tasks={getFilteredTasks()}
                    onTaskUpdate={handleTaskUpdate}
                    onTaskEdit={setEditingTask}
                    onTaskDelete={handleTaskDelete}
                  />
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="week">
              <WeekView 
                tasks={getFilteredTasks()}
                selectedDate={selectedDate}
                onTaskUpdate={handleTaskUpdate}
                onTaskEdit={setEditingTask}
              />
            </TabsContent>

            <TabsContent value="month">
              <MonthView 
                tasks={getFilteredTasks()}
                selectedDate={selectedDate}
                onDateSelect={setSelectedDate}
                onTaskUpdate={handleTaskUpdate}
              />
            </TabsContent>
          </Tabs>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Stats */}
          <Card className="border-none shadow-lg bg-white dark:bg-slate-800 dark:shadow-none dark:border dark:border-slate-700/60">
            <CardHeader>
              <CardTitle className="text-lg text-slate-900 dark:text-slate-100">Quick Stats</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between">
                <span className="text-slate-600 dark:text-slate-400">Total Tasks</span>
                <span className="font-semibold text-slate-900 dark:text-slate-200">{tasks.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-600 dark:text-slate-400">Completed</span>
                <span className="font-semibold text-green-600 dark:text-green-400">
                  {tasks.filter(t => t.status === 'completed').length}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-600 dark:text-slate-400">In Progress</span>
                <span className="font-semibold text-blue-600 dark:text-blue-400">
                  {tasks.filter(t => t.status === 'in_progress').length}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-600 dark:text-slate-400">Overdue</span>
                <span className="font-semibold text-red-600 dark:text-red-400">
                  {tasks.filter(t => t.status !== 'completed' && new Date(t.due_date) < new Date()).length}
                </span>
              </div>
            </CardContent>
          </Card>

          {/* Subject Breakdown */}
          <Card className="border-none shadow-lg bg-white dark:bg-slate-800 dark:shadow-none dark:border dark:border-slate-700/60">
            <CardHeader>
              <CardTitle className="text-lg text-slate-900 dark:text-slate-100">By Subject</CardTitle>
            </CardHeader>
            <CardContent>
              {Object.entries(
                tasks.reduce((acc, task) => {
                  const subject = task.subject || 'Other';
                  acc[subject] = (acc[subject] || 0) + 1;
                  return acc;
                }, {})
              ).map(([subject, count]) => (
                <div key={subject} className="flex justify-between items-center py-2">
                  <span className="text-slate-600 dark:text-slate-400">{subject}</span>
                  <span className="font-semibold text-slate-900 dark:text-slate-200">{count}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Task Form Modal */}
      {(showTaskForm || editingTask) && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-y-auto">
            <TaskForm
              task={editingTask}
              onSubmit={handleTaskSubmit}
              onCancel={() => {
                setShowTaskForm(false);
                setEditingTask(null);
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
{
  "name": "Exam",
  "type": "object",
  "properties": {
    "subject": {
      "type": "string",
      "description": "Exam subject"
    },
    "exam_name": {
      "type": "string",
      "description": "Name of the exam"
    },
    "exam_date": {
      "type": "string",
      "format": "date",
      "description": "Date of the exam"
    },
    "exam_time": {
      "type": "string",
      "description": "Time of the exam"
    },
    "location": {
      "type": "string",
      "description": "Exam location"
    },
    "preparation_status": {
      "type": "string",
      "enum": [
        "not_started",
        "in_progress",
        "well_prepared",
        "ready"
      ],
      "default": "not_started",
      "description": "Preparation status"
    },
    "topics_to_cover": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "List of topics to cover"
    },
    "target_grade": {
      "type": "string",
      "description": "Target grade for the exam"
    }
  },
  "required": [
    "subject",
    "exam_name",
    "exam_date"
  ]
}{
  "name": "MoodEntry",
  "type": "object",
  "properties": {
    "mood_score": {
      "type": "number",
      "minimum": 1,
      "maximum": 10,
      "description": "Mood rating from 1-10"
    },
    "energy_level": {
      "type": "number",
      "minimum": 1,
      "maximum": 10,
      "description": "Energy level from 1-10"
    },
    "stress_level": {
      "type": "number",
      "minimum": 1,
      "maximum": 10,
      "description": "Stress level from 1-10"
    },
    "motivation": {
      "type": "number",
      "minimum": 1,
      "maximum": 10,
      "description": "Motivation level from 1-10"
    },
    "notes": {
      "type": "string",
      "description": "Additional notes about mood"
    },
    "date": {
      "type": "string",
      "format": "date",
      "description": "Date of mood entry"
    }
  },
  "required": [
    "mood_score",
    "energy_level",
    "stress_level",
    "motivation",
    "date"
  ]
}# EDU-Buddy
