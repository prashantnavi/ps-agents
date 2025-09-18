---
title: Career Conversation AI
emoji: 💼
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
short_description: AI-powered career conversation assistant with PDF resume analysis
---

# Career Conversation AI 💼

An intelligent career conversation assistant that can analyze your resume/LinkedIn profile and provide personalized career advice, interview preparation, and professional guidance.

## Features

- 📄 **PDF Resume Analysis**: Upload and analyze your resume or LinkedIn profile
- 💬 **Intelligent Conversations**: Get personalized career advice and guidance
- 🎯 **Interview Preparation**: Practice interview questions and get feedback
- 📊 **Career Insights**: Receive tailored recommendations based on your profile
- 🔄 **Learning System**: The AI learns from conversations to provide better advice

## How to Use

1. **Upload Your Resume**: Upload a PDF of your resume or LinkedIn profile
2. **Start Chatting**: Ask questions about your career, job search, or professional development
3. **Get Personalized Advice**: Receive tailored recommendations based on your background
4. **Practice Interviews**: Use the AI to practice interview questions and scenarios

## Example Questions

- "What are my strengths based on my resume?"
- "How can I improve my LinkedIn profile?"
- "What interview questions should I prepare for a software engineer role?"
- "What career path would suit my background?"
- "How can I negotiate a better salary?"

## Technical Details

- Built with Gradio for easy web interface
- Uses OpenAI's GPT models for intelligent conversations
- PDF processing with PyPDF for resume analysis
- SQLite database for conversation history
- Environment variables for secure API key management

## Setup

The app requires an OpenAI API key to function. Make sure to set your `OPENAI_API_KEY` environment variable.

## Privacy

Your conversations and uploaded documents are processed securely and are not stored permanently. The AI learns from the conversation context but doesn't retain personal information beyond the session.

---

*Built with ❤️ for career development and professional growth*