# 🚀 Quick Deployment Guide - Render.com

## Your Fixed Webhook URL

Once deployed, your **permanent webhook URL** will be:

```
https://YOUR-SERVICE-NAME.onrender.com/webhook/whatsapp
```

Example: `https://hygen-re-api.onrender.com/webhook/whatsapp`

---

## Step-by-Step Deployment

### Step 1: Push to GitHub

```bash
cd /Users/seenivasan/hygen_re_mvp1

# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Hygen RE MVP"

# Create main branch
git branch -M main

# Add your GitHub repo (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/hygen_re_mvp1.git

# Push to GitHub
git push -u origin main
```

### Step 2: Deploy on Render.com

1. Go to: https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. **Connect GitHub**: Authorize and select your repository `hygen_re_mvp1`
4. **Configure Service**:
   - **Name**: `hygen-re-api` (this will be part of your URL)
   - **Runtime**: `Python 3`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Choose Free (for testing) or Starter ($7/mo for production)

### Step 3: Add Environment Variables

In Render dashboard, go to **Environment** tab and add:

```
DATABASE_URL=postgresql+psycopg2://YOUR_DB_CONNECTION_STRING
WHATSAPP_VERIFY_TOKEN=mySecureToken123
WHATSAPP_ACCESS_TOKEN=your_meta_access_token
WHATSAPP_PHONE_NUMBER_ID=your_meta_phone_number_id
DEFAULT_PROJECT_ID=1
```

### Step 4: Create PostgreSQL Database on Render

1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. **Name**: `hygen-re-db`
3. Choose your plan (Free tier available)
4. Click **"Create Database"**
5. Copy the **Internal Database URL**
6. Go back to your web service → **Environment** → Update `DATABASE_URL` with this URL

### Step 5: Migrate Database Schema

After database is created, run these commands locally:

```bash
# Export schema from local database
pg_dump -U postgres -d HYGEN --schema=hygen_re --schema-only > /tmp/schema.sql

# Export data
pg_dump -U postgres -d HYGEN --schema=hygen_re --data-only > /tmp/data.sql

# Import to Render (get connection details from Render dashboard)
psql <RENDER_DATABASE_URL> < /tmp/schema.sql
psql <RENDER_DATABASE_URL> < /tmp/data.sql
```

Or use the Render Shell:
1. Go to your database in Render → **Shell** tab
2. Manually create tables using SQL from your schema

### Step 6: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (~2-5 minutes)
3. Check logs for any errors

### Step 7: Verify Deployment

Test your API:
```bash
curl https://YOUR-SERVICE-NAME.onrender.com/health
# Should return: {"status":"ok"}
```

Visit in browser:
```
https://YOUR-SERVICE-NAME.onrender.com/docs
```

### Step 8: Configure Meta WhatsApp Manager

1. Go to: https://business.facebook.com
2. Navigate to: **WhatsApp** → **API Setup** → **Configuration**
3. Click **"Edit"** on Webhook
4. **Callback URL**: `https://YOUR-SERVICE-NAME.onrender.com/webhook/whatsapp`
5. **Verify Token**: `mySecureToken123` (same as in Render environment)
6. Click **"Verify and Save"**
7. Subscribe to: **messages** field

---

## 🎯 Your Fixed Webhook URL for Meta

```
https://YOUR-SERVICE-NAME.onrender.com/webhook/whatsapp
```

**This URL will NEVER change!** ✅

---

## ⚙️ Environment Variables Summary

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Get from Render DB |
| `WHATSAPP_VERIFY_TOKEN` | Token to verify webhook | `mySecureToken123` |
| `WHATSAPP_ACCESS_TOKEN` | From Meta Business Manager | `EAAxxxx...` |
| `WHATSAPP_PHONE_NUMBER_ID` | From Meta WhatsApp API | `123456789` |
| `DEFAULT_PROJECT_ID` | Your default project | `1` |

---

## 📊 What You Get

✅ **Fixed URL**: `https://YOUR-SERVICE-NAME.onrender.com`
✅ **Automatic HTTPS**: Secure by default
✅ **Auto-deploy**: Push to GitHub = auto deploy
✅ **Health monitoring**: Built-in health checks
✅ **Logs**: Real-time logs in dashboard
✅ **Free tier**: Good for MVP testing

---

## 🆘 Troubleshooting

**Build fails?**
- Check requirements.txt
- View build logs in Render

**Database connection fails?**
- Verify DATABASE_URL is correct
- Check database is running
- Use Render's internal database URL

**Webhook verification fails?**
- WHATSAPP_VERIFY_TOKEN must match in both Render and Meta
- Check logs for verification attempts
- Make sure service is deployed and healthy

**Service is slow?**
- Free tier spins down after 15min inactivity
- First request after sleep takes ~30-60s
- Upgrade to Starter plan for always-on

---

## 📞 Next Steps

1. ✅ Push code to GitHub
2. ✅ Deploy on Render
3. ✅ Create database on Render
4. ✅ Migrate schema and data
5. ✅ Configure Meta webhook
6. ✅ Test with a WhatsApp message!

---

Your fixed webhook URL will be:
# https://hygen-re-api.onrender.com/webhook/whatsapp
(Replace `hygen-re-api` with your chosen service name)
