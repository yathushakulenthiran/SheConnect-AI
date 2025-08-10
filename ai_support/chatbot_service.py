import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple


class MentalHealthChatbot:
    """AI-powered mental health support chatbot specifically for entrepreneurs"""
    
    def __init__(self):
        self.greetings = [
            "Hello entrepreneur! How are you feeling today? Running a business can be challenging, and I'm here to support you.",
            "Hi there! I'm your entrepreneurial mental health companion. How's your business journey affecting your well-being today?",
            "Welcome, business owner! I'm here to help you navigate the mental challenges of entrepreneurship. How are you doing?",
            "Hello! I understand the unique pressures of being an entrepreneur. Let's talk about how you're feeling today."
        ]
        
        self.entrepreneur_mood_responses = {
            'happy': [
                "That's wonderful! Success in business can be incredibly rewarding. What's contributing to your positive mood today?",
                "Your happiness is well-deserved! Entrepreneurship is tough, so celebrate these good moments. What made your day special?",
                "Great to hear you're feeling positive! Business wins can really boost our mental well-being. Keep that momentum going!"
            ],
            'sad': [
                "I understand that entrepreneurship can be emotionally challenging. It's okay to feel down - every business owner goes through tough times. Would you like to talk about what's weighing on you?",
                "Running a business can be lonely and overwhelming. Your feelings are valid, and it's completely normal to have difficult days. What's been particularly challenging lately?",
                "I hear you, and I know how isolating entrepreneurship can feel. Sometimes talking helps. What's been the biggest struggle for you recently?"
            ],
            'anxious': [
                "Entrepreneurial anxiety is very real - the pressure to succeed, financial worries, and uncertainty can be overwhelming. Let's take a deep breath together. What's making you feel anxious about your business?",
                "I understand the anxiety that comes with running a business. The fear of failure, cash flow concerns, and market uncertainty can be paralyzing. What's on your mind?",
                "Business anxiety is tough, but you're stronger than you think. Many successful entrepreneurs have faced these same fears. Let's work through this together."
            ],
            'stressed': [
                "Entrepreneurial stress is intense - juggling multiple responsibilities, making critical decisions, and managing everything can be overwhelming. What's been causing you the most stress lately?",
                "I hear the stress in your voice. Running a business means wearing many hats, and that pressure can be immense. Let's identify what's overwhelming you and find some solutions.",
                "Business stress is your body's way of saying it needs attention. What's been the biggest stressor in your entrepreneurial journey?"
            ],
            'neutral': [
                "A neutral mood is perfectly normal in entrepreneurship. The daily grind of running a business can sometimes leave us feeling 'meh.' How has your business day been so far?",
                "Sometimes neutral is exactly what we need as entrepreneurs. The constant highs and lows can be exhausting. What's been on your mind today?",
                "Neutral feelings are valid too, especially when you're focused on business operations. Is there anything you'd like to explore or discuss?"
            ]
        }
        
        self.entrepreneur_coping_strategies = {
            'anxiety': [
                "Try the 4-7-8 breathing technique: Inhale for 4, hold for 7, exhale for 8. This can help with business decision anxiety.",
                "Break down overwhelming business challenges into smaller, manageable steps. Focus on one task at a time.",
                "Set aside specific 'worry time' each day - 15 minutes to address concerns, then move on to action.",
                "Practice grounding yourself: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste."
            ],
            'stress': [
                "Delegate tasks when possible - you don't have to do everything yourself. What can you outsource or get help with?",
                "Set clear boundaries between work and personal time. Even 30 minutes of 'no business' time daily helps.",
                "Practice progressive muscle relaxation: tense and release each muscle group to release physical tension.",
                "Take regular breaks throughout your workday - even 5-minute walks can reset your stress levels."
            ],
            'sadness': [
                "Connect with other entrepreneurs - they understand the unique challenges you're facing. Consider joining a business support group.",
                "Celebrate small wins, not just big successes. Every step forward in business is worth acknowledging.",
                "Practice self-compassion - treat yourself as you would a business partner who's going through a tough time.",
                "Engage in activities that usually bring you joy, even if you don't feel like it initially."
            ],
            'business_specific': [
                "Review your business metrics objectively - separate your self-worth from business performance.",
                "Create a 'wins journal' - document even small business successes to remind yourself of progress.",
                "Set realistic expectations - entrepreneurship is a marathon, not a sprint.",
                "Build a support network of other entrepreneurs who understand the journey."
            ]
        }
        
        self.entrepreneur_resources = {
            'crisis': [
                "If you're in crisis, please contact the National Mental Health Hotline at 1926 (Sri Lanka) or 1-800-273-8255 (US).",
                "For immediate support, reach out to a trusted friend, family member, or mental health professional.",
                "Remember, it's okay to ask for help. Many successful entrepreneurs have sought mental health support.",
                "Consider reaching out to a business mentor or coach who can provide both business and emotional support."
            ],
            'professional_help': [
                "Consider reaching out to a mental health professional who specializes in working with entrepreneurs.",
                "Many therapists offer sliding scale fees or free initial consultations.",
                "Your primary care doctor can also help connect you with mental health resources.",
                "Look for business coaches who also address mental health and work-life balance."
            ],
            'entrepreneur_support': [
                "Join entrepreneur support groups or networking events where you can connect with others facing similar challenges.",
                "Consider working with a business coach who understands the mental health aspects of entrepreneurship.",
                "Look for mentorship programs that pair you with experienced entrepreneurs who can provide guidance.",
                "Explore coworking spaces where you can build a community of fellow business owners."
            ]
        }

        self.entrepreneur_challenges = {
            'financial_worries': [
                "Financial stress is one of the biggest challenges entrepreneurs face. Have you considered creating a financial buffer or seeking funding options?",
                "Many entrepreneurs struggle with cash flow anxiety. What specific financial concerns are you dealing with?",
                "It's normal to worry about money when running a business. Have you talked to a financial advisor or accountant?"
            ],
            'work_life_balance': [
                "Finding work-life balance as an entrepreneur is incredibly challenging. How are you managing your personal time?",
                "Many business owners struggle with boundaries between work and personal life. What strategies have you tried?",
                "It's okay to prioritize your well-being - a healthy entrepreneur is more effective than a burned-out one."
            ],
            'loneliness': [
                "Entrepreneurial loneliness is very real. How are you building connections with other business owners?",
                "Running a business can be isolating. Have you considered joining entrepreneur groups or networking events?",
                "Many successful entrepreneurs have felt alone in their journey. You're not the only one experiencing this."
            ],
            'imposter_syndrome': [
                "Imposter syndrome is common among entrepreneurs. Remember, everyone starts somewhere, and learning is part of the journey.",
                "Many successful business owners have felt like they don't belong. Your experience and perspective are valuable.",
                "It's normal to doubt yourself when taking on new challenges. What specific doubts are you having?"
            ],
            'failure_fear': [
                "Fear of failure is a natural part of entrepreneurship. What would failure mean to you, and how could you handle it?",
                "Many successful entrepreneurs have failed multiple times before succeeding. Failure is often a stepping stone to success.",
                "It's okay to be afraid of failing. The key is not letting that fear paralyze you from taking action."
            ]
        }

    def analyze_entrepreneur_mood(self, message: str) -> str:
        """Analyze user message to determine mood with entrepreneur context"""
        message_lower = message.lower()
        
        # Entrepreneur-specific indicators
        if any(word in message_lower for word in ['business is good', 'sales up', 'successful', 'profitable', 'growth', 'excited about business']):
            return 'happy'
        
        if any(word in message_lower for word in ['business failing', 'no sales', 'losing money', 'want to quit', 'business is hard']):
            return 'sad'
        
        if any(word in message_lower for word in ['cash flow', 'financial stress', 'market uncertainty', 'competition', 'business anxiety']):
            return 'anxious'
        
        if any(word in message_lower for word in ['overwhelmed', 'too much work', 'burnout', 'work life balance', 'business stress']):
            return 'stressed'
        
        # General mood indicators
        if any(word in message_lower for word in ['happy', 'good', 'great', 'wonderful', 'excited', 'joy', 'pleased']):
            return 'happy'
        
        if any(word in message_lower for word in ['sad', 'depressed', 'down', 'blue', 'miserable', 'hopeless']):
            return 'sad'
        
        if any(word in message_lower for word in ['anxious', 'worried', 'nervous', 'panic', 'fear', 'scared']):
            return 'anxious'
        
        if any(word in message_lower for word in ['stressed', 'overwhelmed', 'pressure', 'tired', 'exhausted']):
            return 'stressed'
        
        return 'neutral'

    def identify_entrepreneur_challenges(self, message: str) -> List[str]:
        """Identify specific entrepreneurial challenges mentioned"""
        message_lower = message.lower()
        challenges = []
        
        if any(word in message_lower for word in ['money', 'cash', 'financial', 'funding', 'revenue', 'profit']):
            challenges.append('financial_worries')
        
        if any(word in message_lower for word in ['work life', 'balance', 'family', 'personal time', 'boundaries']):
            challenges.append('work_life_balance')
        
        if any(word in message_lower for word in ['alone', 'lonely', 'isolated', 'no support', 'no one understands']):
            challenges.append('loneliness')
        
        if any(word in message_lower for word in ['imposter', 'not good enough', 'don\'t belong', 'not qualified']):
            challenges.append('imposter_syndrome')
        
        if any(word in message_lower for word in ['failure', 'fail', 'losing', 'going to fail', 'what if']):
            challenges.append('failure_fear')
        
        return challenges

    def generate_entrepreneur_response(self, message: str, session_history: List[Dict] = None) -> str:
        """Generate appropriate AI response for entrepreneurs"""
        if not session_history:
            session_history = []
        
        # Check for greetings
        if any(word in message.lower() for word in ['hello', 'hi', 'hey', 'start', 'begin']):
            return random.choice(self.greetings)
        
        # Analyze mood with entrepreneur context
        mood = self.analyze_entrepreneur_mood(message)
        
        # Identify specific entrepreneurial challenges
        challenges = self.identify_entrepreneur_challenges(message)
        
        # Generate mood-appropriate response
        mood_response = random.choice(self.entrepreneur_mood_responses.get(mood, self.entrepreneur_mood_responses['neutral']))
        
        # Add entrepreneur-specific coping strategies
        if mood in ['anxious', 'stressed', 'sad']:
            coping_strategy = random.choice(self.entrepreneur_coping_strategies.get(mood, self.entrepreneur_coping_strategies['business_specific']))
            mood_response = f"{mood_response} {coping_strategy}"
        
        # Add challenge-specific responses
        if challenges:
            challenge_response = random.choice(self.entrepreneur_challenges.get(challenges[0], [""]))
            if challenge_response:
                mood_response = f"{mood_response} {challenge_response}"
        
        # Check for crisis indicators
        if any(word in message.lower() for word in ['suicide', 'kill myself', 'end it all', 'no reason to live', 'want to die']):
            return random.choice(self.entrepreneur_resources['crisis'])
        
        # Check for help-seeking
        if any(word in message.lower() for word in ['help', 'therapy', 'counselor', 'professional', 'support']):
            return random.choice(self.entrepreneur_resources['professional_help'])
        
        # Check for entrepreneur-specific help
        if any(word in message.lower() for word in ['mentor', 'coach', 'network', 'other entrepreneurs', 'business support']):
            return random.choice(self.entrepreneur_resources['entrepreneur_support'])
        
        return mood_response

    def suggest_entrepreneur_resources(self, mood: str, stress_level: int, challenges: List[str] = None) -> List[str]:
        """Suggest mental health resources specifically for entrepreneurs"""
        suggestions = []
        
        if stress_level >= 8:
            suggestions.append("Consider reaching out to a mental health professional who specializes in working with entrepreneurs.")
        
        if mood in ['sad', 'anxious']:
            suggestions.append("Connect with other entrepreneurs through networking groups or online communities.")
            suggestions.append("Consider working with a business coach who addresses both business and mental health challenges.")
        
        if stress_level >= 6:
            suggestions.append("Set clear boundaries between work and personal time - even 30 minutes daily helps.")
            suggestions.append("Practice stress management techniques like deep breathing or short walks during work breaks.")
        
        if challenges and 'financial_worries' in challenges:
            suggestions.append("Consider speaking with a financial advisor to create a more stable financial plan.")
        
        if challenges and 'loneliness' in challenges:
            suggestions.append("Join entrepreneur support groups or coworking spaces to build community.")
        
        suggestions.append("Remember, many successful entrepreneurs have faced these same challenges. You're not alone.")
        
        return suggestions[:3]  # Return top 3 suggestions

    def track_mood_trends(self, sessions: List[Dict]) -> Dict:
        """Analyze mood trends from session history"""
        if not sessions:
            return {'trend': 'stable', 'average_mood': 5, 'sessions_count': 0}
        
        recent_sessions = sessions[-7:]  # Last 7 sessions
        mood_scores = [session.get('mood_rating', 5) for session in recent_sessions]
        
        if len(mood_scores) < 2:
            return {'trend': 'stable', 'average_mood': sum(mood_scores) / len(mood_scores), 'sessions_count': len(mood_scores)}
        
        # Calculate trend
        first_half = mood_scores[:len(mood_scores)//2]
        second_half = mood_scores[len(mood_scores)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg + 1:
            trend = 'improving'
        elif second_avg < first_avg - 1:
            trend = 'declining'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'average_mood': sum(mood_scores) / len(mood_scores),
            'sessions_count': len(mood_scores),
            'recent_mood': mood_scores[-1] if mood_scores else 5
        }


# Global chatbot instance
chatbot = MentalHealthChatbot()
