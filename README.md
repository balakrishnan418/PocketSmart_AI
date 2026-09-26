# 🤖 PocketSmart AI

> **AI-powered personal planning assistant built with FastAPI, PostgreSQL and Gemini AI.**

## 🌐 Live Website

👉 **[Open PocketSmart AI] https://pocket-smart-ai-snowy.vercel.app/**

PocketSmart AI is a smart web application designed to help users generate personalized recommendations and plans using Artificial Intelligence.

The application combines a **FastAPI backend**, **Neon PostgreSQL database**, and **Google Gemini AI** to provide an interactive and data-driven user experience.

---

## ✨ Features

- 🔐 **User Authentication**
  - User registration
  - Secure login
  - JWT-based authentication
  - Session management

- 🤖 **AI-Powered Recommendations**
  - Gemini AI integration
  - Personalized recommendation generation
  - AI-powered planning workflows

- 📊 **User Dashboard**
  - Personalized dashboard
  - Session information
  - User-specific data

- 📝 **Recommendation History**
  - Save generated recommendations
  - View previous results
  - User-specific history

- 🗄️ **PostgreSQL Database**
  - Neon PostgreSQL integration
  - Persistent user data
  - Recommendation storage

- ☁️ **Cloud Deployment**
  - Vercel deployment support
  - Production environment variables
  - Serverless-friendly FastAPI architecture

---

## 🛠️ Tech Stack

| Technology                 | Purpose                    |
| -------------------------- | -------------------------- |
| 🐍 Python                  | Core programming language  |
| ⚡ FastAPI                 | Backend API framework      |
| 🐘 PostgreSQL              | Database                   |
| ☁️ Neon                    | Cloud PostgreSQL           |
| 🤖 Google Gemini AI        | AI-powered recommendations |
| 🔐 JWT                     | Authentication             |
| 🌐 HTML / CSS / JavaScript | Frontend                   |
| ☁️ Vercel                  | Deployment                 |
| 🔧 Git & GitHub            | Version control            |

---

## 🏗️ Project Architecture

```text
PocketSmart_AI/
│
├── backend/
│   ├── database.py
│   ├── security.py
│   │
│   └── routes/
│       └── api.py
│
├── frontend/
│   └── ...
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔄 Application Flow

```text
              ┌──────────────────┐
              │      User        │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │    Frontend      │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │     FastAPI      │
              │     Backend      │
              └──────┬─────┬─────┘
                     │     │
             ┌───────┘     └────────┐
             ▼                      ▼
    ┌─────────────────┐    ┌─────────────────┐
    │ Neon PostgreSQL │    │   Gemini AI     │
    │     Database    │    │ Recommendation  │
    └─────────────────┘    └─────────────────┘
```

---

## 🔐 Authentication

PocketSmart AI uses JWT-based authentication to protect user sessions.

```text
Register
   ↓
User stored in PostgreSQL
   ↓
Login
   ↓
JWT Token
   ↓
Authenticated Session
   ↓
Dashboard
```

Passwords are stored using secure password hashing rather than plain text.

---

## 🗄️ Database

PocketSmart AI uses **PostgreSQL hosted on Neon**.

Main database entities include:

### Users

Stores registered user information.

```text
users
├── id
├── name
├── email
├── password_hash
└── created_at
```

### Recommendations

Stores AI-generated recommendation history.

```text
recommendations
├── id
├── user_id
├── planner
├── input_json
├── result_json
└── created_at
```

---

## 🤖 Gemini AI Integration

PocketSmart AI uses Google Gemini to generate AI-powered recommendations.

The API key is loaded through an environment variable.

```env
GEMINI_API_KEY=your_api_key_here
```

> ⚠️ **Never commit your real Gemini API key to GitHub.**

---

## ⚙️ Environment Variables

Create a `.env` file locally.

Example:

```env
DATABASE_URL=your_neon_postgresql_connection_string

SECRET_KEY=your_secure_secret_key

GEMINI_API_KEY=your_gemini_api_key

GEMINI_MODEL=your_gemini_model

COOKIE_SECURE=false
```

For production deployment, configure these variables through the hosting platform's environment-variable settings.

### 🔒 Security

Never commit:

```text
.env
DATABASE_URL
GEMINI_API_KEY
SECRET_KEY
```

The repository includes `.gitignore` rules to keep sensitive configuration files out of Git.

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/balakrishnan418/PocketSmart_AI.git
```

### 2. Move into the project

```bash
cd PocketSmart_AI
```

### 3. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

### 4. Activate the virtual environment

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```powershell
pip install -r requirements.txt
```

### 6. Configure environment variables

Create:

```text
.env
```

and add the required values described above.

### 7. Start the application

```powershell
python app.py
```

The application will be available at:

```text
http://127.0.0.1:8000
```

---

## ☁️ Deployment

PocketSmart AI can be deployed using Vercel.

Production environment variables should be configured in the Vercel project settings.

Required variables include:

```text
DATABASE_URL
SECRET_KEY
GEMINI_API_KEY
GEMINI_MODEL
COOKIE_SECURE
```

For production:

```env
COOKIE_SECURE=true
```

After changing environment variables, create a new deployment so the updated configuration is loaded.

---

## 📌 API Functionality

The backend provides functionality for:

```text
Authentication
├── Register
├── Login
├── Session information
└── Session data

AI Planning
├── Generate recommendations
├── Save recommendations
└── Retrieve recommendation history

User Data
└── Manage user-specific recommendation history
```

---

## 🧪 Current Project Status

```text
✅ User Registration
✅ User Login
✅ JWT Authentication
✅ Session Management
✅ FastAPI Backend
✅ Neon PostgreSQL
✅ Gemini AI Integration
✅ AI Recommendation Generation
✅ Recommendation History
✅ GitHub Repository
✅ Vercel Deployment Support
```

---

## 🔮 Future Improvements

Possible future enhancements include:

- 📈 Advanced financial analytics
- 📊 Interactive charts and reports
- 💬 AI conversational assistant
- 🎯 Personalized financial goals
- 📱 Improved mobile responsiveness
- 🔔 Smart reminders and notifications
- 📤 Export reports
- 🧠 More personalized AI recommendations

---

## 🔐 Security Notes

This project follows basic security practices including:

- JWT authentication
- Password hashing
- Environment-based secrets
- PostgreSQL persistence
- `.gitignore` protection for sensitive files

**Never expose API keys, database passwords, JWT secrets, or other credentials publicly.**

---

## 📂 Repository

**GitHub:**
https://github.com/balakrishnan418/PocketSmart_AI

---

## 👨‍💻 Author

**Balakrishnan C**

Computer Science Student & Developer

Interested in:

- Python
- AI / Machine Learning
- Backend Development
- FastAPI
- PostgreSQL
- Generative AI

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is created for learning, development, and portfolio purposes.

## 🌐 Visit the Website

🚀 **[PocketSmart AI – Live Website] https://pocket-smart-ai-snowy.vercel.app/**