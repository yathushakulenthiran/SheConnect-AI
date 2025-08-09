# SheConnect AI - Mentorship Platform

**AI-Powered Mentorship & Mental Health Support for Women Entrepreneurs in Sri Lanka**

## 🎯 **Project Overview**

SheConnect AI is a comprehensive mentorship platform designed specifically for early-stage women entrepreneurs in Sri Lanka. The platform combines AI-powered mentor matching with mental health support to create a holistic ecosystem for women's business growth and well-being.

## 🚀 **Core Features**

### **1. Public Mentor Directory**
- Browse verified mentor profiles
- View expertise, experience, and availability
- Filter by industry and business stage
- Contact information and LinkedIn profiles

### **2. Mentee Registration & Onboarding**
- Email/Google login integration
- Comprehensive onboarding questionnaire
- Business stage and industry identification
- Challenge and goal documentation

### **3. AI-Powered Mentor Matching**
- Intelligent matching algorithm
- Business stage alignment
- Industry expertise matching
- Challenge-goal correlation
- Top 3 mentor recommendations

### **4. Connection Management**
- Request/approve mentor connections
- Message exchange system
- Session scheduling
- Progress tracking

### **5. Mental Health Support**
- AI-powered mental health chatbot
- Daily/weekly check-ins
- Stress management tips
- Motivational content
- Local mental health resource directory

## 🛠️ **Technical Stack**

- **Backend**: Django 5.2.5, Python 3.13
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **AI Integration**: OpenAI GPT, Custom NLP models
- **Authentication**: Django built-in auth
- **File Handling**: Pillow for image processing

## 📁 **Project Structure**

```
sheconnect-mentorship/
├── core/                    # Core app with home page and static pages
├── mentors/                 # Mentor profiles and management
├── mentees/                 # Mentee profiles and onboarding
├── ai_support/             # AI matching and mental health features
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── media/                  # Uploaded files (mentor photos)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 **Quick Start**

### **1. Clone and Setup**
```bash
git clone <repository-url>
cd sheconnect-mentorship
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### **2. Database Setup**
```bash
python manage.py migrate
python manage.py createsuperuser
```

### **3. Run Development Server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see your application!

## 🔐 **Admin Access**

**URL:** `http://127.0.0.1:8000/admin/`
- **Username:** `admin`
- **Password:** `admin123`

## 📊 **Database Models**

### **Mentors App**
- **Mentor**: Expert profiles with expertise, experience, availability
- **Admin Interface**: Full mentor management and verification

### **Mentees App**
- **Mentee**: User profiles with business information and goals
- **ConnectionRequest**: Mentor-mentee connection management
- **MentorshipSession**: Session scheduling and tracking

### **AI Support App**
- **MentalHealthSession**: AI chat sessions and mood tracking
- **AIMatchingScore**: AI-powered mentor matching scores
- **MentalHealthResource**: Local mental health resources
- **ChatMessage**: Individual chat messages

## 🎯 **MVP Features (Current)**

✅ **Public Mentor Directory** - Browse mentor profiles
✅ **Mentee Registration** - User onboarding system
✅ **AI Matching Framework** - Matching algorithm structure
✅ **Connection System** - Request/approve connections
✅ **Mental Health Support** - AI chatbot framework
✅ **Admin Interface** - Complete management system

## 🔮 **Future Enhancements**

### **Phase 2: AI Integration**
- OpenAI GPT integration for mental health chat
- Advanced NLP for mentor matching
- Sentiment analysis for mood tracking
- Personalized content recommendations

### **Phase 3: Advanced Features**
- Video call integration
- Payment processing
- Advanced analytics dashboard
- Mobile app development
- Multi-language support

### **Phase 4: Scale & Monetization**
- Subscription models
- Commission-based revenue
- Enterprise partnerships
- International expansion

## 🌟 **Key Benefits**

### **For Women Entrepreneurs:**
- Access to experienced mentors
- AI-powered business guidance
- Mental health support
- Local resource connections
- Community building

### **For Mentors:**
- Impact measurement
- Flexible scheduling
- Professional development
- Network expansion
- Recognition platform

### **For Sri Lanka:**
- Women entrepreneurship growth
- Economic empowerment
- Mental health awareness
- Professional networking
- Innovation ecosystem

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- Women entrepreneurs in Sri Lanka
- Mentorship community
- Mental health professionals
- AI and technology partners
- Supportive ecosystem

## 📞 **Support**

For support, email hello@sheconnect.ai or create an issue in this repository.

---

**Built with ❤️ for Women Entrepreneurs in Sri Lanka**

*Empowering women through AI-powered mentorship and mental health support*
