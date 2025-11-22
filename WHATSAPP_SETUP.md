# 📱 Meta WhatsApp Configuration

## ✅ Your Webhook URL (PERMANENT)
```
https://hygen-re-mvp.onrender.com/webhook/whatsapp
```

## 🔑 Verify Token
```
mySecureToken123
```

## 📋 Configuration Details

### Render Environment Variables (Already Set)
```
DATABASE_URL = postgresql://hygen_re_db_user:BR3GSAazNpAQBQVtoBtBhoxMOq60uPb4@dpg-d4go1j9r0fns739ohjg0-a/hygen_re_db
WHATSAPP_VERIFY_TOKEN = mySecureToken123
WHATSAPP_ACCESS_TOKEN = EAAWE3OH9q40BQMKDs55ojZBZBkqmh5GfZBoDRnZAiQahUgOEBfnCZBlRKvKpMPZBa7ZBZAS4FuDGf1zK97Tfnm5obtLkgZBVW9ebK6jyQQkA47qumJ6lLypyx7hX30ihgSTfBZAQG1CgZB8c8GmMAhN8fg0E65wlHiBPldRXNOeHFEw8pJ5h6J58WQoP49iZAy9OKqp9s7nhYErqZCzXk80B3InMS35IJT4QSpNa7ZC7BB4hAXfRTIonqQdYWu3a4ZCiEjc6WDloGVPAtSlZC17YLFrbrZCQa45ZAaLfA4B4sGnttonvkL
WHATSAPP_PHONE_NUMBER_ID = 746103891921531
DEFAULT_PROJECT_ID = 1
```

### WhatsApp Credentials
```
Phone Number ID: 746103891921531
Access Token: EAAWE3OH9q40BQMKDs55ojZBZBkqmh5GfZBoDRnZAiQahUgOEBfnCZBlRKvKpMPZBa7ZBZAS4FuDGf1zK97Tfnm5obtLkgZBVW9ebK6jyQQkA47qumJ6lLypyx7hX30ihgSTfBZAQG1CgZB8c8GmMAhN8fg0E65wlHiBPldRXNOeHFEw8pJ5h6J58WQoP49iZAy9OKqp9s7nhYErqZCzXk80B3InMS35IJT4QSpNa7ZC7BB4hAXfRTIonqQdYWu3a4ZCiEjc6WDloGVPAtSlZC17YLFrbrZCQa45ZAaLfA4B4sGnttonvkL
```

---

## 🚀 Steps to Configure Meta WhatsApp Business

### 1. Go to Meta Business Manager
- URL: https://business.facebook.com
- Navigate to: **Your App** → **WhatsApp** → **Configuration**

### 2. Configure Webhook

In the **Webhook** section:

**Callback URL:**
```
https://hygen-re-mvp.onrender.com/webhook/whatsapp
```

**Verify Token:**
```
mySecureToken123
```

Click **"Verify and Save"**

### 3. Subscribe to Webhook Fields

After verification, subscribe to:
- ✅ **messages** (Required - to receive incoming messages)

### 4. Test the Webhook

**Option A: Use Meta's Test Button**
- Click "Test" button in Meta dashboard
- You should see a success message

**Option B: Send a Real Message**
1. Add a test phone number in Meta dashboard
2. Send a message from that number to your WhatsApp Business number
3. Check Render logs to see the incoming message

---

## 🔍 Verify Deployment

### Check Health Endpoint
```bash
curl https://hygen-re-mvp.onrender.com/health
```
Should return: `{"status":"ok"}`

### Check API Documentation
```
https://hygen-re-mvp.onrender.com/docs
```

### View Render Logs
1. Go to: https://dashboard.render.com
2. Click on: **hygen-re-mvp**
3. Click on: **Logs** tab
4. Watch for incoming webhook requests

---

## 🗄️ Database Schema Setup

**IMPORTANT:** Before testing, create the database schema!

### Method 1: Use Render Shell (Recommended)
1. Go to your database: **hygen-re-db**
2. Click **"Shell"** tab
3. Paste and run the SQL from `schema.sql` file

### Method 2: Use psql with External URL
1. Go to database settings
2. Find **"External Database URL"**
3. Run: `psql <EXTERNAL_URL> -f schema.sql`

---

## ✅ Testing Checklist

Before going live:

- [ ] Render service deployed successfully
- [ ] Health endpoint returns `{"status":"ok"}`
- [ ] Database schema created
- [ ] Environment variables set in Render
- [ ] Webhook verified in Meta
- [ ] Subscribed to "messages" field
- [ ] Test message sent and received
- [ ] Check Render logs for incoming webhooks

---

## 🆘 Troubleshooting

### Webhook Verification Fails
- Ensure `WHATSAPP_VERIFY_TOKEN` in Render matches what you enter in Meta
- Check Render logs for verification attempts
- Make sure service is deployed and running

### No Messages Received
- Verify webhook is subscribed to "messages"
- Check phone number is approved for sending messages
- View Render logs for incoming requests
- Ensure database schema is created

### Database Errors
- Verify `DATABASE_URL` is correct
- Check database is running in Render
- Ensure schema `hygen_re` exists
- Check tables are created

---

## 📞 Next Steps

1. ✅ Add environment variables to Render
2. ✅ Wait for deployment to complete (~2 minutes)
3. ✅ Create database schema using Render Shell
4. ✅ Configure webhook in Meta
5. ✅ Send test message
6. ✅ Check Render logs
7. ✅ View lead in Streamlit dashboard

---

## 🎯 Your Permanent URLs

- **API**: https://hygen-re-mvp.onrender.com
- **Health**: https://hygen-re-mvp.onrender.com/health
- **Webhook**: https://hygen-re-mvp.onrender.com/webhook/whatsapp
- **Docs**: https://hygen-re-mvp.onrender.com/docs

**These URLs will NEVER change!** ✅
