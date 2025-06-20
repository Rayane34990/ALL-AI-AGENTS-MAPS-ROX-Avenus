# ☁️ Cloud Deployment Guide

## 🎯 Free Cloud Stack
- **Database**: Supabase (Free PostgreSQL)
- **Backend**: Render (Free Python hosting)  
- **Frontend**: Vercel (Free React hosting)
- **Automation**: GitHub Actions (Free CI/CD)

## 🚀 Quick Deploy (5 Minutes)

### 1. Database Setup (Supabase)
1. Go to [supabase.com](https://supabase.com) → Create account
2. Create new project → Get connection string
3. Copy: `postgresql://user:pass@db.xxx.supabase.co:5432/postgres`

### 2. Backend Deploy (Render)
1. Go to [render.com](https://render.com) → Sign up with GitHub
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `ai-agent-discovery-api`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
5. Add environment variable: `DATABASE_URL` (from Supabase)
6. Click "Create Web Service"
7. Your API will be live at: `https://ai-agent-discovery-api.onrender.com`

### 3. Frontend Deploy (Vercel)
1. Go to [vercel.com](https://vercel.com) → Import from GitHub
2. Select the `web` folder as root directory
3. Add environment variable: `REACT_APP_API_URL` (from Render)
4. Your frontend will be live at: `https://your-app.vercel.app`

### 4. Automation Setup
1. In GitHub → Settings → Secrets → Actions
2. Add these secrets:
   - `DATABASE_URL`: Your Supabase connection string
   - `RENDER_API_KEY`: From Render dashboard
   - `RENDER_SERVICE_ID`: From Render service settings
   - `VERCEL_TOKEN`: From Vercel dashboard
   - `VERCEL_ORG_ID` & `VERCEL_PROJECT_ID`: From Vercel

## ✅ Result
- 🤖 Auto-ingests data every 6 hours
- 🚀 Auto-deploys on every push
- 💰 Completely free forever (750 hours/month on Render)
- 🌍 Globally available
- 📈 Scales automatically

## 🔧 Monitoring
- Backend health: `https://your-app.onrender.com/health`
- Frontend: `https://your-app.vercel.app`
- GitHub Actions: Check the Actions tab

Your AI discovery platform is now **LIVE** and **SUSTAINABLE**! 🎉
