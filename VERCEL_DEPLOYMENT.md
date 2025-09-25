# ConvertAnything - Vercel Deployment Guide

## 🚀 Deploy to Vercel

This guide will help you deploy the ConvertAnything backend to Vercel for serverless operation.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **OpenAI API Key**: Get one at [platform.openai.com](https://platform.openai.com/api-keys)
3. **Git Repository**: Your code should be in a Git repository

## ⚡ Quick Deploy

### Option 1: Deploy Button (Recommended)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/DaneBentley/Convertanything)

### Option 2: Manual Deployment

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from your project directory**
   ```bash
   cd /path/to/ConvertAnything
   vercel
   ```

4. **Follow the prompts**
   - Link to existing project or create new
   - Set project name
   - Configure environment variables

## 🔐 Environment Variables

Set these in your Vercel dashboard or during deployment:

### Required
- `OPENAI_API_KEY`: Your OpenAI API key for transcription

### Optional
- `MAX_FILE_SIZE`: Maximum file size in MB (default: 10)
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS

## 📁 Project Structure

```
ConvertAnything/
├── api/
│   ├── health.py      # Health check endpoint
│   ├── transcribe.py  # Main transcription endpoint
│   └── models.py      # Available models endpoint
├── vercel.json        # Vercel configuration
├── requirements.txt   # Python dependencies
└── [frontend files]   # HTML, CSS, JS
```

## 🔧 Configuration Files

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/*.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    }
  ],
  "functions": {
    "api/*.py": {
      "maxDuration": 300
    }
  }
}
```

### requirements.txt
```
flask==2.3.3
openai==1.3.5
python-dateutil==2.8.2
```

## 🌐 API Endpoints

Once deployed, your API will be available at:

- **Health Check**: `https://your-project.vercel.app/api/health`
- **Transcribe**: `https://your-project.vercel.app/api/transcribe`
- **Models**: `https://your-project.vercel.app/api/models`

## 🎯 Frontend Configuration

Update your frontend to use the Vercel API:

In `script.js`, change the API URL:
```javascript
// Replace localhost with your Vercel URL
this.apiUrl = 'https://your-project.vercel.app/api';
```

## 📊 Serverless Limitations

### File Size Limits
- **Maximum**: 10MB per file (Vercel limit)
- **Recommended**: Under 5MB for best performance
- **Processing Time**: Up to 5 minutes per request

### Memory Constraints
- **Available RAM**: 1GB (Vercel Pro) or 3GB (Enterprise)
- **CPU Time**: Limited execution time
- **Cold Starts**: First requests may be slower

## 🔄 Deployment Process

### Automatic Deployment
1. **Connect Git Repository** to Vercel
2. **Push to main branch** triggers automatic deployment
3. **Environment variables** are preserved across deployments
4. **Preview deployments** for pull requests

### Manual Deployment
```bash
# Deploy to production
vercel --prod

# Deploy preview
vercel

# Check deployment status
vercel ls

# View logs
vercel logs
```

## 🧪 Testing Your Deployment

### 1. Health Check
```bash
curl https://your-project.vercel.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "ConvertAnything API is running on Vercel",
  "timestamp": "2025-09-25T...",
  "environment": "production"
}
```

### 2. Models Endpoint
```bash
curl https://your-project.vercel.app/api/models
```

### 3. Transcription Test
```bash
curl -X POST https://your-project.vercel.app/api/transcribe \
  -F "audio=@test-audio.mp3" \
  -F "model=whisper-1" \
  -F "speaker_separation=true"
```

## 🛠️ Troubleshooting

### Common Issues

1. **"Function timeout"**
   - Reduce file size
   - Check OpenAI API response time
   - Increase maxDuration in vercel.json

2. **"OpenAI API key not configured"**
   - Set OPENAI_API_KEY in Vercel dashboard
   - Redeploy after setting environment variables

3. **"File too large"**
   - Vercel has strict size limits
   - Consider file compression
   - Use chunked processing for large files

4. **CORS errors**
   - Update ALLOWED_ORIGINS environment variable
   - Check frontend API URL configuration

### Debug Commands
```bash
# View function logs
vercel logs --follow

# Check environment variables
vercel env ls

# Pull environment variables locally
vercel env pull .env.local
```

## 💰 Cost Considerations

### Vercel Pricing
- **Hobby**: Free tier with limitations
- **Pro**: $20/month per user
- **Enterprise**: Custom pricing

### OpenAI API Costs
- **Whisper API**: $0.006 per minute of audio
- **Average cost**: ~$0.36 per hour of audio
- **Monthly estimate**: Varies by usage

## 🔒 Security Best Practices

1. **Environment Variables**
   - Never commit API keys to Git
   - Use Vercel's environment variable system
   - Rotate keys regularly

2. **CORS Configuration**
   - Limit allowed origins
   - Don't use wildcard (*) in production

3. **Rate Limiting**
   - Consider implementing rate limiting
   - Monitor API usage
   - Set up billing alerts

## 📈 Performance Optimization

1. **File Processing**
   - Validate files before processing
   - Implement client-side compression
   - Use appropriate audio formats

2. **Caching**
   - Cache model responses when possible
   - Use CDN for static assets
   - Implement response caching

3. **Monitoring**
   - Set up Vercel Analytics
   - Monitor function execution time
   - Track error rates

## 🚀 Going Live

### Final Steps
1. **Set custom domain** in Vercel dashboard
2. **Configure SSL certificate** (automatic)
3. **Update frontend** with production API URL
4. **Test all functionality** end-to-end
5. **Monitor performance** and errors

### Production Checklist
- [ ] OpenAI API key configured
- [ ] Custom domain set up
- [ ] Frontend updated with production URL
- [ ] CORS properly configured
- [ ] Error monitoring in place
- [ ] Billing alerts configured
- [ ] Performance tested

## 📞 Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **OpenAI API Docs**: [platform.openai.com/docs](https://platform.openai.com/docs)
- **Project Issues**: [GitHub Issues](https://github.com/DaneBentley/Convertanything/issues)

---

**🎵 ConvertAnything - Serverless Deployment Ready!**

Your AI transcription service is now ready for global deployment with Vercel's edge network. 🌍
