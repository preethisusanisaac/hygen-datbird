# Render.com Deployment Guide for Hygen RE MVP1

## 🚀 Deployment Steps

### 1. Push Code to GitHub (if not already done)

```bash
cd /Users/seenivasan/hygen_re_mvp1
git init
git add .
git commit -m "Initial commit - Hygen RE MVP1"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/hygen_re_mvp1.git
git push -u origin main
```

### 2. Deploy on Render.com

1. **Log in to Render.com**: https://render.com
2. **Click "New +"** → Select **"Web Service"**
3. **Connect your GitHub repository**: `hygen_re_mvp1`
4. **Configure the service**:
   - **Name**: `hygen-re-api` (or your preferred name)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (for testing) or Starter (for production)

### 3. Set Environment Variables on Render

Go to **Environment** tab and add these variables:

```
DATABASE_URL=postgresql+psycopg2://hygen_user:Hygen123@YOUR_DB_HOST:5432/HYGEN?options=-csearch_path=hygen_re
WHATSAPP_VERIFY_TOKEN=your_secure_verify_token_here
WHATSAPP_ACCESS_TOKEN=your_whatsapp_access_token_from_meta
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_from_meta
DEFAULT_PROJECT_ID=1
```

**IMPORTANT**: You'll need to either:
- Use Render's PostgreSQL database (recommended), OR
- Make your local PostgreSQL accessible (not recommended for production)

### 4. Database Options on Render

**Option A: Use Render PostgreSQL (Recommended)**
1. Create a new PostgreSQL database on Render
2. Get the connection string from Render
3. Update `DATABASE_URL` environment variable
4. Migrate your schema and data to the new database

**Option B: Use External PostgreSQL**
- Your database must be publicly accessible
- Use the public IP/hostname in DATABASE_URL
- Not recommended for security reasons

### 5. Deploy

1. Click **"Create Web Service"**
2. Render will automatically build and deploy
3. Wait for deployment to complete (~2-5 minutes)

### 6. Get Your Fixed Webhook URL

After deployment, your fixed URL will be:
```
https://hygen-re-api.onrender.com
```

**Webhook URL for Meta WhatsApp Manager:**
```
https://hygen-re-api.onrender.com/webhook/whatsapp
```

### 7. Test Your Deployment

**Health Check:**
```bash
curl https://hygen-re-api.onrender.com/health
# Should return: {"status":"ok"}
```

**API Documentation:**
```
https://hygen-re-api.onrender.com/docs
```

### 8. Configure Meta WhatsApp Manager

1. Go to **Meta Business Manager** → **WhatsApp** → **Configuration**
2. Add Webhook:
   - **Callback URL**: `https://hygen-re-api.onrender.com/webhook/whatsapp`
   - **Verify Token**: (use the same value as `WHATSAPP_VERIFY_TOKEN` in Render)
3. Subscribe to webhook fields: **messages**
4. Save and verify

## 📝 Important Notes

### Database Migration

If you create a new Render PostgreSQL database, you'll need to:

1. **Export your local schema**:
```bash
pg_dump -U postgres -d HYGEN --schema=hygen_re --schema-only > schema.sql
```

2. **Export your data**:
```bash
pg_dump -U postgres -d HYGEN --schema=hygen_re --data-only > data.sql
```

3. **Import to Render database**:
```bash
psql -h YOUR_RENDER_DB_HOST -U YOUR_RENDER_USER -d YOUR_RENDER_DB < schema.sql
psql -h YOUR_RENDER_DB_HOST -U YOUR_RENDER_USER -d YOUR_RENDER_DB < data.sql
```

### Free Tier Limitations

- Free services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30-60 seconds
- Upgrade to Starter plan ($7/month) for always-on service

### Logs and Monitoring

- View logs in Render dashboard: **Logs** tab
- Set up alerts for failures
- Monitor health check endpoint

## 🔒 Security Checklist

- ✅ Use strong `WHATSAPP_VERIFY_TOKEN`
- ✅ Never commit `.env` file to git
- ✅ Use environment variables for all secrets
- ✅ Enable HTTPS (automatic on Render)
- ✅ Restrict database access to Render IPs only

## 🆘 Troubleshooting

### Build Fails
- Check `requirements.txt` is correct
- Verify Python version compatibility

### Database Connection Issues
- Verify `DATABASE_URL` is correct
- Check database is accessible from Render
- Test connection with: `psql <DATABASE_URL>`

### Webhook Not Working
- Verify URL is publicly accessible
- Check Render logs for incoming requests
- Verify `WHATSAPP_VERIFY_TOKEN` matches Meta configuration
- Test webhook manually with curl

## 📞 Support

- Render Docs: https://render.com/docs
- Meta WhatsApp API: https://developers.facebook.com/docs/whatsapp
