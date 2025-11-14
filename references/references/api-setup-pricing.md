# Gemini API Setup and Pricing

This reference covers how to obtain and configure your Gemini API key, and details about pricing for Gemini 2.5 Flash Image (Nano Banana).

**Official Documentation**: 
- [Gemini API Keys](https://ai.google.dev/gemini-api/docs/api-key)
- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)

## Obtaining an API Key

### Step 1: Access Google AI Studio

1. Navigate to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google Account credentials

### Step 2: Create API Key

1. Click on the "Get API Key" button (usually at the top-right corner)
2. Review and accept the terms of service
3. Choose to create the API key in an existing Google Cloud project or create a new one
4. Once generated, copy your API key immediately
5. **Important**: Store your API key securely - you won't be able to view it again after closing the dialog

### Step 3: Store API Key Securely

**Never commit API keys to version control!** Use one of these secure storage methods:

#### Option 1: macOS Keychain (Recommended for this project)

Store your API key in macOS Keychain using the `security` command:

```bash
security add-generic-password \
  -a "production" \
  -s "GEMINI_API_KEY" \
  -w "your_api_key_here"
```

Retrieve it when needed:

```bash
export GEMINI_API_KEY=$(security find-generic-password -a "production" -s "GEMINI_API_KEY" -w)
```

#### Option 2: Environment Variables (Development)

**macOS/Linux (Bash):**
```bash
# Add to ~/.bashrc
export GEMINI_API_KEY="your_api_key_here"

# Apply changes
source ~/.bashrc
```

**macOS (Zsh):**
```bash
# Add to ~/.zshrc
export GEMINI_API_KEY="your_api_key_here"

# Apply changes
source ~/.zshrc
```

**Windows:**
1. Search for "Environment Variables" in Windows search
2. Click "Edit the system environment variables"
3. In System Properties, click "Environment Variables"
4. Under "User variables," click "New"
5. Variable name: `GEMINI_API_KEY`
6. Variable value: Your API key
7. Click "OK" to save

#### Option 3: Environment File (For Local Development)

Create a `.env` file (add to `.gitignore`):

```bash
# .env
GEMINI_API_KEY=your_api_key_here
```

Load it in your application or source it:

```bash
source .env
```

## Verifying API Key Setup

Test that your API key is properly configured:

```bash
# Check if environment variable is set
echo $GEMINI_API_KEY

# Test with a simple API call
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"test"}]}]}'
```

## API Key Security Best Practices

1. **Never share API keys publicly**
   - Don't commit keys to Git repositories
   - Don't include keys in screenshots or documentation
   - Don't share keys via email or chat

2. **Use API key restrictions** (if available)
   - Restrict keys to specific IP addresses when possible
   - Limit keys to specific applications or referrers
   - Use separate keys for development and production

3. **Rotate keys regularly**
   - Generate new keys periodically
   - Revoke old keys when no longer needed
   - Update keys in your secure storage locations

4. **Monitor usage**
   - Regularly check API usage in Google Cloud Console
   - Set up alerts for unusual activity
   - Review billing statements

## Pricing for Gemini 2.5 Flash Image

### Image Generation Pricing

Gemini 2.5 Flash Image uses **token-based pricing** for image output:

| Metric | Price |
|--------|-------|
| **Image Output** | $30 per 1 million tokens |
| **Per Image (flat rate)** | 1290 tokens per image |
| **Effective Cost per Image** | ~$0.0387 per image |

**Important Details:**
- Each generated image consumes **1290 tokens** regardless of aspect ratio or resolution
- This flat token count applies to images up to 1024x1024 pixels
- All supported aspect ratios consume the same token count (1290 tokens)
- Pricing is consistent across all aspect ratios

### Aspect Ratio and Token Consumption

All aspect ratios consume the same token count:

| Aspect Ratio | Resolution | Tokens | Cost per Image |
|-------------|------------|--------|----------------|
| 1:1 | 1024x1024 | 1290 | ~$0.0387 |
| 2:3 | 832x1248 | 1290 | ~$0.0387 |
| 3:2 | 1248x832 | 1290 | ~$0.0387 |
| 3:4 | 864x1184 | 1290 | ~$0.0387 |
| 4:3 | 1184x864 | 1290 | ~$0.0387 |
| 4:5 | 896x1152 | 1290 | ~$0.0387 |
| 5:4 | 1152x896 | 1290 | ~$0.0387 |
| 9:16 | 768x1344 | 1290 | ~$0.0387 |
| 16:9 | 1344x768 | 1290 | ~$0.0387 |
| 21:9 | 1536x672 | 1290 | ~$0.0387 |

**Note:** The token count is fixed at 1290 tokens per image regardless of the aspect ratio you choose.

### Cost Calculation Examples

**Example 1: Generate 100 images**
- Tokens: 100 × 1290 = 129,000 tokens
- Cost: 129,000 ÷ 1,000,000 × $30 = **$3.87**

**Example 2: Generate 1,000 images**
- Tokens: 1,000 × 1290 = 1,290,000 tokens
- Cost: 1,290,000 ÷ 1,000,000 × $30 = **$38.70**

**Example 3: Generate 10,000 images**
- Tokens: 10,000 × 1290 = 12,900,000 tokens
- Cost: 12,900,000 ÷ 1,000,000 × $30 = **$387.00**

### Free Tier and Usage Limits

Google provides a free tier for the Gemini API with usage limits. Check the current free tier limits in the [official pricing documentation](https://ai.google.dev/gemini-api/docs/pricing).

**Important:** Free tier limits may:
- Have daily or monthly request limits
- Apply to specific models or endpoints
- Change over time - always check current documentation

### Input Costs (If Applicable)

If you're sending images or text as input (for image editing or multi-image composition):
- **Text/Image/Video input**: Check current pricing in official docs (varies by model)
- **Audio input**: Typically higher cost than text/image input

**Note:** For Nano Banana image generation, input costs (if any) are typically minimal compared to the fixed 1290 token output cost per image.

### Batch API Pricing

If using batch API endpoints (available for some models):
- Batch requests may have different pricing
- Typically lower cost per request but higher latency
- Check current batch pricing in official documentation

### Cost Optimization Tips

1. **Batch Requests**: If processing multiple images, consider batching requests where supported
2. **Cache Results**: Store generated images locally to avoid regenerating identical images
3. **Iterative Refinement**: Use Nano Banana's conversational editing to refine images instead of generating from scratch
4. **Monitor Usage**: Set up usage alerts in Google Cloud Console
5. **Test with Small Batches**: Verify prompt quality before generating large batches

## Billing and Usage Monitoring

### View Usage in Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" > "Dashboard"
3. Select your project
4. View API usage metrics and billing

### Set Up Billing Alerts

1. Go to "Billing" in Google Cloud Console
2. Navigate to "Budgets & alerts"
3. Create a budget with alerts
4. Set thresholds for spending notifications

### API Quotas and Rate Limits

Check current rate limits and quotas:
- Navigate to "APIs & Services" > "Quotas"
- View per-minute, per-day, and per-project limits
- Request quota increases if needed

## References

- [Gemini API - API Keys Documentation](https://ai.google.dev/gemini-api/docs/api-key)
- [Gemini API - Pricing Documentation](https://ai.google.dev/gemini-api/docs/pricing)
- [Google AI Studio](https://aistudio.google.com/)
- [Google Cloud Console](https://console.cloud.google.com/)

## Quick Reference

**API Key Setup:**
```bash
# Store in macOS Keychain
security add-generic-password -a "production" -s "GEMINI_API_KEY" -w "your_key"

# Retrieve
export GEMINI_API_KEY=$(security find-generic-password -a "production" -s "GEMINI_API_KEY" -w)
```

**Pricing:**
- **Per Image**: 1290 tokens = ~$0.0387
- **Per 1M Tokens**: $30
- **All aspect ratios**: Same cost (1290 tokens/image)

**Useful Links:**
- [Get API Key](https://aistudio.google.com/app/apikey)
- [View Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Monitor Usage](https://console.cloud.google.com/)

