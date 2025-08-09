#!/bin/bash

# SheConnect AI - Push to GitHub Script
echo "🚀 Pushing SheConnect AI to GitHub..."

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Initialize git repository (if not already done)
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
fi

# Add all files
echo "📦 Adding files to Git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Initial commit: SheConnect AI Django project

- Django 5.2.5 with Python 3.13
- Custom user management with profiles
- AI service models and conversation tracking
- Beautiful responsive UI
- Environment-based configuration
- MySQL/SQLite database support
- Admin interface with comprehensive models
- Health check API endpoint"

# Add GitHub remote
echo "🔗 Adding GitHub remote..."
git remote add origin https://github.com/yathushakulenthiran/SheConnect-AI.git

# Push to GitHub
echo "⬆️ Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "✅ Successfully pushed to GitHub!"
echo "🌐 View your repository at: https://github.com/yathushakulenthiran/SheConnect-AI"
