# Gemini Model Troubleshooting Guide

## Empty Response Issue - November 2025

This document captures critical troubleshooting findings for Gemini API empty response issues encountered during promptgen command development.

## Issue Summary

**Date**: November 20, 2025
**Issue**: HTTP 200 OK responses with empty `response.candidates` or `response.content.parts`
**Error Message**: "Empty response from model" with `finish_reason=STOP`

## Models Tested

### ❌ Failed Models (Empty Responses)

1. **gemini-3-pro-preview**
   - Status: Preview (Released Nov 18, 2025)
   - Temperature tested: 0.7, 1.0
   - Result: Empty responses with both temperature settings
   - Known Issue: GitHub reports similar problems with grounded search

2. **gemini-2.5-flash**
   - Status: Stable
   - Temperature tested: 1.0
   - Result: Empty responses
   - Expected: Should be stable, but experiencing issues

### ✅ Working Model (Confirmed)

**gemini-2.0-flash-exp**
- Status: Experimental
- Temperature: **0.7** (critical)
- Result: Successful prompt generation
- Original implementation: Commit 1bca76d
- User confirmation: "this worked!"

## Root Cause Analysis

### Temperature Requirements

Different Gemini models have different temperature requirements:

| Model | Required Temperature | Notes |
|-------|---------------------|-------|
| gemini-2.0-flash-exp | 0.7 | Original working config |
| gemini-2.5-flash | 0.7-1.0 | Expected to work, but experiencing issues |
| gemini-3-pro-preview | 1.0 | **Must be 1.0**, but still returns empty responses |

### Known GitHub Issues

From googleapis/python-genai repository:

> "Running Gemini 2.5 Pro with grounded search sometimes returns empty response.text with finish_reason of STOP and no other reason. When I inspect the response dict it shows evidence of the search with some web meta information, but nothing else."

**Key Finding**:
- Gemini 3 Pro requires `temperature=1.0`
- Values below 1.0 cause "looping or degraded performance"
- **However**, even with correct temperature, empty responses still occur

### Additional Context

User reported:
> "This issue is not only present in 3.0, but my retry work-around no longer works. I am working with our account team and will post any findings. The key here is that response.text and response.candidates are None, along with most of the other fields."

## Working Configuration

```python
# promptgen.py
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=system_prompt + "\n\n" + user_prompt,
    config=types.GenerateContentConfig(
        temperature=0.7,  # Some creativity but consistent
        max_output_tokens=500,  # Enough for detailed prompts
    ),
)
```

## Attempted Fixes (Did Not Work)

1. ❌ Changing model to gemini-3-pro-preview
2. ❌ Setting temperature to 1.0 for Gemini 3 Pro
3. ❌ Switching to gemini-2.5-flash
4. ❌ Various temperature adjustments (0.7, 1.0)

## Resolution

**Revert to original working configuration:**
- Model: `gemini-2.0-flash-exp`
- Temperature: `0.7`
- Commit reference: `1bca76d` (original implementation)

## Timeline of Changes

1. **1bca76d** - Original working implementation (gemini-2.0-flash-exp, temp=0.7) ✅
2. **ec4e86d** - Upgraded to gemini-3-pro (broke functionality)
3. **ca00f86** - Fixed model ID to gemini-3-pro-preview (still broken)
4. **7454b5e** - Added cost tracking (functionality still broken)
5. **808feb1** - Set temperature to 1.0 for Gemini 3 Pro (still broken)
6. **98ceddc** - Switched to gemini-2.5-flash (still broken)
7. **d066849** - Reverted to original working config ✅

## Debugging Steps Taken

### 1. Added Multi-Level Verbosity Logging

```bash
gemini-nano-banana-tool promptgen "test" --json -vvv
```

Output showed:
- HTTP 200 OK response
- Empty `response.candidates`
- Empty `response.content.parts`
- `finish_reason=STOP` (normal completion, but no content)

### 2. Checked API Response

```
[DEBUG] HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent "HTTP/1.1 200 OK"
[ERROR] Generation error: Prompt generation failed: Empty response from model
```

### 3. Historical Analysis

Compared current code with original working commit:
```bash
git show 1bca76d:gemini_nano_banana_tool/core/promptgen.py | grep -A 10 "def generate_prompt"
```

Found original configuration was different from current.

## Lessons Learned

1. **Not All Stable Models Are Stable**: gemini-2.5-flash is marked stable but experiencing issues
2. **Preview Models Have Issues**: gemini-3-pro-preview has persistent empty response problems
3. **Temperature Matters**: Different models have different temperature requirements
4. **Experimental Can Be More Stable**: gemini-2.0-flash-exp is more reliable than newer models
5. **Don't Assume Newer Is Better**: Original working configuration often best
6. **Version Control Is Critical**: Git history helped identify working configuration

## Recommendations

### For Production Use

**Recommended Model**: `gemini-2.0-flash-exp`
- Proven stability for text generation
- Works reliably with temperature=0.7
- Free during preview period
- No known empty response issues

**Alternative**: `gemini-1.5-flash-002`
- Previous generation stable model
- Well-tested and documented
- May be more reliable than 2.5/3.0 for some use cases

### Configuration

```python
# Recommended for prompt generation
config = types.GenerateContentConfig(
    temperature=0.7,  # Balance between creativity and consistency
    max_output_tokens=500,  # Sufficient for detailed prompts
)
```

### When to Use Other Models

- **gemini-2.5-flash**: Wait for stability improvements, monitor GitHub issues
- **gemini-3-pro-preview**: Avoid until empty response issue resolved
- **gemini-1.5-pro**: Use for tasks requiring maximum quality over speed

## Monitoring

Watch these resources for updates:

1. **GitHub Issues**: https://github.com/googleapis/python-genai/issues
2. **Official Docs**: https://ai.google.dev/gemini-api/docs/models
3. **Gemini 3 Guide**: https://ai.google.dev/gemini-api/docs/gemini-3
4. **Status Page**: https://status.ai.google.dev/

## Cost Implications

| Model | Price per 1M tokens | Typical 300 token prompt |
|-------|-------------------|------------------------|
| gemini-2.0-flash-exp | Free (preview) | $0.00 |
| gemini-2.5-flash | $0.30 | $0.00009 |
| gemini-3-pro-preview | $12.00 | $0.0036 |

**Recommendation**: Stick with gemini-2.0-flash-exp for cost-effective, reliable prompt generation.

## Future Actions

1. Monitor Google's issue tracker for fixes to 2.5/3.0 models
2. Test periodically with newer models to see if issues resolved
3. Keep gemini-2.0-flash-exp as fallback option
4. Document any new working configurations discovered

## References

- Original working commit: `1bca76d` (feat: Add AI-powered promptgen command)
- Revert commit: `d066849` (fix: Revert to original working configuration)
- GitHub Issue: "Running Gemini 2.5 Pro with grounded search sometimes returns empty response.text"
- Model docs: https://ai.google.dev/gemini-api/docs/models
- Pricing: https://ai.google.dev/pricing

---

**Last Updated**: November 20, 2025
**Status**: Resolved - Using gemini-2.0-flash-exp
**Maintainer**: gemini-nano-banana-tool team
