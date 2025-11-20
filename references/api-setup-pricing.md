# Google Gemini API Setup and Pricing

Complete guide to setting up and understanding pricing for Google Gemini image generation API.

## Table of Contents

- [API Setup](#api-setup)
- [Authentication Methods](#authentication-methods)
- [Pricing Details](#pricing-details)
- [Rate Limits](#rate-limits)
- [Cost Optimization](#cost-optimization)

## API Setup

### 1. Get API Key (Developer API)

**Recommended for**: Development, testing, small projects

**Steps**:
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Copy your API key

**Set Environment Variable**:
```bash
# Option 1: GEMINI_API_KEY (recommended)
export GEMINI_API_KEY="your-api-key-here"

# Option 2: GOOGLE_API_KEY
export GOOGLE_API_KEY="your-api-key-here"

# Make permanent (add to ~/.zshrc or ~/.bashrc)
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**Test**:
```bash
gemini-nano-banana-tool generate "test prompt" -o test.png
```

### 2. Vertex AI Setup (Enterprise)

**Recommended for**: Production, enterprise, GCP integration

**Prerequisites**:
- Google Cloud Project
- Billing enabled
- Vertex AI API enabled

**Steps**:

1. **Install gcloud CLI**:
   ```bash
   # macOS
   brew install google-cloud-sdk

   # Or download from: https://cloud.google.com/sdk/docs/install
   ```

2. **Authenticate**:
   ```bash
   gcloud auth application-default login
   ```

3. **Set Environment Variables**:
   ```bash
   export GOOGLE_GENAI_USE_VERTEXAI=true
   export GOOGLE_CLOUD_PROJECT="your-project-id"
   export GOOGLE_CLOUD_LOCATION="us-central1"  # or preferred region
   ```

4. **Enable Vertex AI API**:
   ```bash
   gcloud services enable aiplatform.googleapis.com --project=your-project-id
   ```

5. **Test**:
   ```bash
   gemini-nano-banana-tool generate "test prompt" -o test.png --use-vertex
   ```

## Authentication Methods

### Method 1: Developer API (Simplest)

**Pros**:
- Easy setup (just an API key)
- No GCP project required
- Free tier available
- Quick to get started

**Cons**:
- Lower rate limits
- Less suitable for production
- No enterprise features

**Usage**:
```bash
export GEMINI_API_KEY="your-key"
gemini-nano-banana-tool generate "prompt" -o output.png
```

### Method 2: Vertex AI (Enterprise)

**Pros**:
- Higher rate limits
- Enterprise support
- Better SLAs
- Integration with GCP services
- Better monitoring/logging

**Cons**:
- Requires GCP project
- More complex setup
- Requires billing account

**Usage**:
```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT="your-project"
export GOOGLE_CLOUD_LOCATION="us-central1"
gemini-nano-banana-tool generate "prompt" -o output.png --use-vertex
```

### Method 3: Override with CLI Flag

**Override API key per command**:
```bash
gemini-nano-banana-tool generate "prompt" -o output.png \
  --api-key "different-key"
```

**Override to use Vertex AI**:
```bash
gemini-nano-banana-tool generate "prompt" -o output.png \
  --use-vertex \
  --project "your-project" \
  --location "us-central1"
```

## Pricing Details

### Free Tier

**Developer API**:
- **Rate Limit**: ~15 requests per minute (RPM)
- **Daily Limit**: Check current limits at [pricing page](https://ai.google.dev/pricing)
- **Cost**: FREE
- **Best For**: Development, testing, learning, small personal projects

**Limitations**:
- Lower priority during high demand
- Rate limits may be adjusted
- Not recommended for production

### Paid Tier - Flash Model (2.5)

**Model**: `gemini-2.5-flash-image`

**Pricing Structure**:
- **Rate**: $30.00 per 1 million output tokens
- **Cost per token**: $0.00003
- **Typical token usage**: ~1,290 tokens per image
- **Cost per image**: **$0.039** (1,290 × $0.00003)
- **Resolution**: Up to 1024×1024 pixels (fixed)
- **Speed**: Fast (seconds per image)

**Example Costs**:
```
10 images    = $0.39
100 images   = $3.90
1,000 images = $39.00
10,000 images = $390.00
```

**Best For**:
- Quick iterations and prototyping
- Cost-effective production
- High-volume generation
- Content that doesn't require maximum quality

### Paid Tier - Pro Model (3.0)

**Model**: `gemini-3-pro-image-preview`

**Pricing Structure**:
- **Rate**: $120.00 per 1 million output tokens
- **Cost per token**: $0.00012
- **Resolution-based token usage**:
  - **1K/2K** (1024×1024px to 2048×2048px): ~1,120 tokens → **$0.134 per image**
  - **4K** (up to 4096×4096px): ~2,000 tokens → **$0.24 per image**
- **Speed**: Slower (better quality)

**Example Costs (1K/2K Resolution)**:
```
10 images    = $1.34
100 images   = $13.40
1,000 images = $134.00
10,000 images = $1,340.00
```

**Example Costs (4K Resolution)**:
```
10 images    = $2.40
100 images   = $24.00
1,000 images = $240.00
10,000 images = $2,400.00
```

**Best For**:
- Professional asset production
- High-quality requirements
- Complex scenes with fine details
- Projects requiring Google Search grounding
- Text accuracy critical applications

### Vertex AI Pricing

**Additional Costs**:
- Same per-image costs as above
- Plus: Cloud infrastructure costs (minimal)
- Plus: Potential egress charges (if images stored in Cloud Storage)

**Benefits**:
- Higher rate limits
- Better SLAs
- Enterprise support
- Monitoring/logging included

### Pricing Notes

**Important**:
1. Pricing is **approximate** and subject to change
2. Always verify current pricing at: https://ai.google.dev/pricing
3. Reference images don't add extra cost (included in base price)
4. Failed generations may still count toward quota
5. Rate limits apply to both free and paid tiers

**Factors Affecting Cost**:
- Model choice (Flash vs Pro)
- Volume (potential discounts)
- Region (Vertex AI)
- Additional GCP services used

## Rate Limits

### Developer API

**Free Tier**:
- ~15 requests per minute (RPM)
- May vary based on demand
- Subject to daily quotas

**Paid Tier**:
- Higher limits (varies by usage)
- Contact sales for enterprise limits

### Vertex AI

**Higher Limits**:
- Significantly higher than Developer API
- Configurable based on project needs
- Better for production workloads

### Handling Rate Limits

**Best Practices**:
1. Implement retry logic with exponential backoff
2. Batch operations when possible
3. Cache results to avoid regeneration
4. Monitor usage in Google Cloud Console
5. Request quota increases if needed

**Error Handling**:
```bash
# CLI automatically handles basic retries
# For heavy use, implement application-level batching
```

## Cost Optimization

### 1. Choose the Right Model

**Use Flash (2.5) for**:
- Prototyping and testing
- High-volume generation
- Simple to moderate complexity
- Cost-sensitive projects

**Use Pro (3.0) for**:
- Final production images
- Complex scenes requiring detail
- Critical text rendering
- Professional/commercial work

### 2. Prompt Optimization

**Save costs by**:
- Getting it right the first time (iterate prompts in AI Studio first)
- Using specific, clear prompts (reduce trial and error)
- Batch similar generations
- Reuse successful prompts

### 3. Caching and Storage

**Strategies**:
- Cache generated images to avoid regeneration
- Store successful prompts for reuse
- Use local storage vs cloud storage (no egress costs)
- Implement deduplication for similar requests

### 4. Development vs Production

**Development**:
- Use free tier for testing
- Test prompts in [AI Studio](https://aistudio.google.com/) first
- Use Flash model for iterations
- Limit test batch sizes

**Production**:
- Use paid tier with appropriate model
- Implement robust error handling
- Monitor costs in real-time
- Set up billing alerts

### 5. Reference Images

**Efficient Use**:
- Reference images don't add cost (included in base price)
- Use them to reduce prompt iteration
- More references = fewer generation attempts
- Test reference combinations in Studio first

### 6. Monitoring Costs

**Google Cloud Console**:
1. Go to [GCP Billing](https://console.cloud.google.com/billing)
2. Set up budget alerts
3. Monitor API usage
4. Track costs per project/service

**CLI Monitoring**:
```bash
# Log generation costs (implement in your scripts)
echo "Generated image: output.png, Model: flash, Approx cost: $0.01"
```

## Cost Examples

### Scenario 1: Personal Project

**Usage**: 100 images/month
**Model**: Flash (2.5)
**Cost**: $0.10 - $1.00/month
**Recommendation**: Free tier may be sufficient

### Scenario 2: Small Business

**Usage**: 1,000 images/month
**Model**: Mix of Flash and Pro
**Cost**: $5 - $50/month
**Recommendation**: Paid tier, mostly Flash with Pro for key images

### Scenario 3: Enterprise

**Usage**: 100,000 images/month
**Model**: Primarily Flash with Pro for critical content
**Cost**: $500 - $5,000/month
**Recommendation**: Vertex AI with volume discounts, dedicated support

### Scenario 4: Content Creator

**Usage**: 50 images/day (1,500/month)
**Model**: Flash for iterations, Pro for finals
**Cost**: $10 - $100/month
**Recommendation**: Paid tier, optimize prompts to reduce iterations

## Billing Setup

### Developer API

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Navigate to billing/payment settings
3. Add payment method
4. Starts charging automatically when free tier exceeded

### Vertex AI

1. Go to [GCP Console](https://console.cloud.google.com/)
2. Navigate to Billing
3. Create/link billing account
4. Enable Vertex AI API
5. Set up budget alerts (recommended)

### Budget Alerts

**Recommended Setup**:
```
Alert at: 50%, 90%, 100% of budget
Notifications to: your-email@example.com
Monthly budget: Set based on expected usage
```

## Resources

### Documentation
- **Pricing**: https://ai.google.dev/pricing
- **API Docs**: https://ai.google.dev/gemini-api/docs
- **Vertex AI**: https://cloud.google.com/vertex-ai/docs

### Tools
- **AI Studio**: https://aistudio.google.com/ (test prompts, get API keys)
- **GCP Console**: https://console.cloud.google.com/ (billing, monitoring)
- **API Reference**: https://ai.google.dev/api

### Support
- **Community**: https://discuss.ai.google.dev/
- **Enterprise**: Contact Google Cloud sales
- **Documentation**: Comprehensive guides at ai.google.dev

## Frequently Asked Questions

**Q: Is there a completely free option?**
A: Yes, the Developer API free tier allows ~15 requests/minute with daily quotas.

**Q: What happens if I exceed free tier limits?**
A: You'll need to add billing to continue. Set up billing alerts to monitor.

**Q: Are reference images charged separately?**
A: No, reference images are included in the base image generation cost.

**Q: Which is cheaper: Flash or Pro?**
A: Flash is approximately 10x cheaper than Pro model.

**Q: Can I get volume discounts?**
A: Yes, contact Google Cloud sales for enterprise volume pricing.

**Q: Do failed generations count toward quota?**
A: Usually yes, check current policy in documentation.

**Q: How do I estimate my costs?**
A: Use: (expected images/month) × (cost per image based on model)

**Q: Can I set a hard spending limit?**
A: GCP budget alerts notify but don't stop spending. Implement application-level limits.

---

**Last Updated**: 2025-11-20
**Official Pricing**: https://ai.google.dev/pricing
**Tool**: gemini-nano-banana-tool

**Note**: All pricing is approximate and subject to change. Always verify current pricing at official Google AI documentation before making budgeting decisions.
