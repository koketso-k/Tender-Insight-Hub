# Tender Insight Hub - Troubleshooting Guide

## Table of Contents
1. [Quick Diagnostics](#quick-diagnostics)
2. [Authentication Issues](#authentication-issues)
3. [Search & Discovery Problems](#search--discovery-problems)
4. [Document Analysis Issues](#document-analysis-issues)
5. [Readiness Scoring Problems](#readiness-scoring-problems)
6. [Workspace & Collaboration Issues](#workspace--collaboration-issues)
7. [Performance Issues](#performance-issues)
8. [API Integration Problems](#api-integration-problems)
9. [Premium Features Issues](#premium-features-issues)
10. [Data Sync & Storage Issues](#data-sync--storage-issues)
11. [Browser & Compatibility Issues](#browser--compatibility-issues)
12. [Emergency Procedures](#emergency-procedures)

---

## Quick Diagnostics

### System Status Check
Before troubleshooting, check if the issue is system-wide:

1. **Platform Status Page**: Visit https://status.tenderinsighthub.co.za
2. **Service Health**: Check individual service status
3. **Maintenance Windows**: Look for scheduled maintenance
4. **Known Issues**: Review current incident reports

### Basic Health Check
```bash
# Test API connectivity
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.tenderinsighthub.co.za/v1/health

# Expected response
{
  "status": "healthy",
  "timestamp": "2025-08-01T10:30:00Z",
  "response_time_ms": 45
}
```

### Browser Console Check
1. Open browser developer tools (F12)
2. Check Console tab for JavaScript errors
3. Check Network tab for failed requests
4. Look for CORS or authentication errors

---

## Authentication Issues

### Problem: "Invalid API Key" Error

**Symptoms:**
- HTTP 401 Unauthorized responses
- "Invalid API key" error messages
- Unable to access any API endpoints

**Common Causes & Solutions:**

**1. Incorrect API Key Format**
```bash
# ❌ Wrong format
Authorization: YOUR_API_KEY

# ✅ Correct format
Authorization: Bearer YOUR_API_KEY
```

**2. Expired API Key**
- Check expiration date in dashboard: Settings > API Access
- Generate new API key if expired
- Update applications with new key

**3. Revoked or Deleted Key**
- Verify key exists in your dashboard
- Check if team admin revoked access
- Generate replacement key

**4. Wrong Environment**
```bash
# ❌ Using production key on staging
https://api-staging.tenderinsighthub.co.za/v1/

# ✅ Match environment
Production: https://api.tenderinsighthub.co.za/v1/
Staging: https://api-staging.tenderinsighthub.co.za/v1/
```

### Problem: "Insufficient Permissions" Error

**Symptoms:**
- HTTP 403 Forbidden responses
- Access denied to specific endpoints
- Some features unavailable

**Solutions:**
1. **Check API Key Permissions**
   - Go to Settings > API Access
   - Verify required permissions are enabled
   - Contact team admin to update permissions

2. **Plan Limitations**
   - Verify your subscription plan includes the feature
   - Upgrade to higher tier if needed
   - Check usage limits haven't been exceeded

### Problem: Session Timeout Issues

**Symptoms:**
- Frequent login prompts
- Session expires quickly
- "Session invalid" errors

**Solutions:**
1. **Browser Settings**
   - Enable cookies for the domain
   - Check if browser is in private/incognito mode
   - Clear browser cache and cookies

2. **Network Issues**
   - Check for proxy/firewall interference
   - Verify stable internet connection
   - Try different network if possible

---

## Search & Discovery Problems

### Problem: No Search Results Found

**Symptoms:**
- Empty result sets for valid queries
- "No tenders found" messages
- Previously working searches return nothing

**Diagnostic Steps:**
1. **Check Search Parameters**
```bash
# Test basic search without filters
GET /tenders/search?q=construction

# Gradually add filters to isolate issue
GET /tenders/search?q=construction&province=gauteng
```

2. **Verify Data Availability**
```bash
# Check total tender count
GET /tenders/stats

{
  "total_tenders": 1234,
  "last_updated": "2025-08-01T06:00:00Z",
  "active_tenders": 567
}
```

**Common Solutions:**

**1. Overly Restrictive Filters**
- Remove filters one by one to identify culprit
- Check date ranges aren't excluding all results
- Verify budget ranges are realistic

**2. Cached Data Issues**
- API cache refreshes every 24 hours
- Try search after cache refresh time
- Contact support for manual cache refresh

**3. Keywords Too Specific**
```bash
# ❌ Too specific
q="very specific technical term xyz-123"

# ✅ Broader terms
q="construction OR building OR infrastructure"
```

### Problem: Poor Search Result Relevance

**Symptoms:**
- Irrelevant results at top of list
- Missing obviously relevant tenders
- Scoring seems incorrect

**Solutions:**

**1. Improve Search Query**
```bash
# Use multiple relevant keywords
q="road construction highway infrastructure"

# Include synonyms
q="construction OR building OR development"

# Use sector-specific terms
q="civil engineering AND gauteng"
```

**2. Update Company Profile**
- Ensure services are accurately described
- Add relevant keywords to capabilities
- Update sector classifications

**3. Use Advanced Scoring**
```json
POST /tenders/search/scored
{
  "query": "construction",
  "scoring": {
    "boost_factors": {
      "sector_match": 2.0,
      "location_preference": 1.5
    }
  }
}
```

### Problem: Search Results Not Updating

**Symptoms:**
- Same results returned repeatedly
- New tenders not appearing
- Stale data in results

**Solutions:**
1. **Check Cache Headers**
```bash
curl -I "https://api.tenderinsighthub.co.za/v1/tenders/search?q=test"

# Look for cache headers
Cache-Control: max-age=3600
Last-Modified: Wed, 01 Aug 2025 06:00:00 GMT
```

2. **Force Cache Refresh**
```bash
# Add cache-busting parameter
GET /tenders/search?q=construction&_t=1722499200
```

3. **Browser Cache Issues**
- Hard refresh (Ctrl+F5)
- Clear browser cache
- Use incognito mode to test

---

## Document Analysis Issues

### Problem: Document Upload Failures

**Symptoms:**
- Upload progress stops/fails
- "File upload error" messages
- Timeout during upload

**Common Causes & Solutions:**

**1. File Size Issues**
```python
# Check file size before upload
import os
file_size = os.path.getsize('document.pdf')
max_size = 10 * 1024 * 1024  # 10MB

if file_size > max_size:
    print(f"File too large: {file_size} bytes")
    # Compress or split file
```

**2. Unsupported File Format**
- **Supported**: PDF, ZIP (containing PDFs)
- **Unsupported**: DOC, DOCX, images, etc.
- Convert documents to PDF before upload

**3. Network Issues**
```python
# Implement retry logic for uploads
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def upload_with_retry(file_path, max_retries=3):
    session = requests.Session()
    retry_strategy = Retry(
        total=max_retries,
        status_forcelist=[500, 502, 503, 504],
        backoff_factor=1
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    
    with open(file_path, 'rb') as f:
        response = session.post(
            "https://api.tenderinsighthub.co.za/v1/documents/analyze",
            files={'document': f},
            headers={'Authorization': 'Bearer YOUR_API_KEY'},
            timeout=300  # 5 minute timeout
        )
    return response
```

### Problem: AI Summarization Failures

**Symptoms:**
- "Analysis failed" errors
- Empty or incomplete summaries
- Long processing times without results

**Diagnostic Steps:**
1. **Check Document Quality**
```bash
# Verify document was processed
GET /documents/{document_id}/status

{
  "status": "failed",
  "error": "Text extraction failed - document may be image-based",
  "pages_processed": 0
}
```

2. **Text Extraction Issues**
- Scanned PDFs without OCR won't work
- Password-protected PDFs will fail
- Corrupted files cause processing errors

**Solutions:**

**1. Document Preprocessing**
```python
# Check if PDF has extractable text
import pdfplumber

def check_pdf_text(file_path):
    with pdfplumber.open(file_path) as pdf:
        text_length = sum(len(page.extract_text() or '') for page in pdf.pages)
        return text_length > 100  # Minimum viable text

if not check_pdf_text('document.pdf'):
    print("Document needs OCR processing")
```

**2. Model-Specific Issues**
```bash
# Check AI model status
GET /system/models/status

{
  "summarization_model": {
    "name": "bart-large-cnn",
    "status": "healthy",
    "last_update": "2025-08-01T00:00:00Z"
  }
}
```

**3. Large Document Handling**
- Split large documents into smaller sections
- Focus on specific sections (technical specs, terms)
- Use batch processing for multiple documents

### Problem: Poor Summary Quality

**Symptoms:**
- Summaries miss key information
- Irrelevant content highlighted
- Technical details lost

**Solutions:**

**1. Document Structure Optimization**
- Ensure clear headings and sections
- Key information should be in main text, not footnotes
- Avoid overly complex formatting

**2. Feedback Loop**
```python
# Provide feedback to improve future summaries
feedback_data = {
    "document_id": "doc_123",
    "summary_quality": 3,  # 1-5 scale
    "missing_info": ["budget details", "deadline specifics"],
    "irrelevant_info": ["background history"],
    "suggestions": "Focus more on technical requirements"
}

requests.post(
    "https://api.tenderinsighthub.co.za/v1/documents/feedback",
    json=feedback_data,
    headers={'Authorization': 'Bearer YOUR_API_KEY'}
)
```

**3. Manual Review Process**
- Always review AI summaries manually
- Add supplementary notes for critical details
- Use summary as starting point, not final analysis

---

## Readiness Scoring Problems

### Problem: Inconsistent or Low Scores

**Symptoms:**
- Scores don't match expectations
- Similar tenders have very different scores
- All scores are consistently low

**Diagnostic Steps:**
1. **Profile Completeness Check**
```bash
GET /company/profile/validation

{
  "overall_score": 45,  # Low completeness affects scoring
  "missing_critical_fields": [
    "certifications",
    "recent_experience", 
    "sector_classification"
  ]
}
```

2. **Score Breakdown Analysis**
```bash
GET /tenders/{tender_id}/readiness-score/detailed

{
  "total_score": 65,
  "components": {
    "technical_fit": 45,      # Low - need better service descriptions
    "experience_match": 75,   # Good
    "compliance_status": 30,  # Low - missing certifications
    "capacity_assessment": 85 # Good
  }
}
```

**Solutions:**

**1. Complete Company Profile**
```json
// Add missing critical information
{
  "services": [
    "Road construction and maintenance",
    "Highway infrastructure development", 
    "Bridge construction and repair",
    "Traffic management systems"
  ],
  "certifications": [
    {
      "name": "CIDB Grade 7 CE",
      "number": "CIDB123456",
      "expiry_date": "2026-01-15"
    }
  ],
  "experience": [
    {
      "project_name": "N3 Highway Section Upgrade",
      "value": 25000000,
      "completion_date": "2024-06-30",
      "client": "SANRAL"
    }
  ]
}
```

**2. Keyword Optimization**
- Use industry-standard terminology
- Include technical specifications in service descriptions
- Match language used in tender documents

**3. Regular Profile Updates**
- Review profile monthly
- Add completed projects promptly
- Update certifications before expiry

### Problem: Score Calculation Delays

**Symptoms:**
- Scores take long time to appear
- "Calculating..." status persists
- Scores don't update after profile changes

**Solutions:**

**1. Check Processing Queue**
```bash
GET /scoring/queue-status

{
  "queue_length": 45,
  "estimated_wait_minutes": 3,
  "your_position": 12
}
```

**2. Manual Score Refresh**
```bash
POST /tenders/{tender_id}/readiness-score/recalculate
{
  "force_refresh": true,
  "priority": "high"
}
```

**3. Profile Change Propagation**
- Profile updates can take 5-10 minutes to affect scores
- Clear browser cache after profile updates
- Check profile version timestamp

### Problem: Score Explanations Unclear

**Symptoms:**
- Don't understand why score is low/high
- Recommendations not actionable
- Missing context for scoring decisions

**Solutions:**

**1. Request Detailed Explanation**
```bash
GET /tenders/{tender_id}/readiness-score/explanation

{
  "score": 72,
  "strengths": [
    "Strong sector alignment (construction/civil engineering)",
    "Appropriate company size for project scale",
    "Recent relevant experience in highway projects"
  ],
  "weaknesses": [
    "Missing CIDB Grade 8 certification (required)",
    "No experience with specific bridge construction",
    "Limited working capital for project size"
  ],
  "recommendations": [
    "Obtain CIDB Grade 8 certification before bidding",
    "Consider joint venture with bridge specialist",
    "Secure additional financing or bonding"
  ]
}
```

**2. Score Comparison**
```bash
# Compare with similar tenders
GET /tenders/compare-scores?tender_ids=TND-001,TND-002,TND-003
```

---

## Workspace & Collaboration Issues

### Problem: Team Members Can't Access Shared Tenders

**Symptoms:**
- Saved tenders not visible to team
- "Access denied" errors for team members
- Inconsistent data between users

**Solutions:**

**1. Check Team Membership**
```bash
GET /team/members

{
  "members": [
    {
      "user_id": "user_123",
      "email": "john@company.com",
      "role": "member",
      "status": "active",
      "last_active": "2025-08-01T14:30:00Z"
    }
  ]
}
```

**2. Verify Permissions**
```bash
GET /team/permissions

{
  "user_permissions": {
    "read:tenders": true,
    "write:workspace": true,
    "manage:team": false
  }
}
```

**3. Multi-Tenant Isolation Issues**
- Ensure all team members use same team domain
- Check for accidentally created duplicate accounts
- Verify API keys are team-scoped

### Problem: Activity Logs Missing or Incomplete

**Symptoms:**
- User actions not recorded
- Missing timestamps or details
- Incomplete audit trail

**Solutions:**

**1. Check Activity Retention**
```bash
GET /workspace/activity?days=30&include_details=true

{
  "retention_policy": "90_days",
  "total_activities": 156,
  "oldest_record": "2025-05-01T00:00:00Z"
}
```

**2. Activity Filtering**
```bash
# Filter by specific user or action
GET /workspace/activity?user_id=user_123&action=save_tender
```

**3. Export Activity Data**
```bash
# Generate comprehensive activity report
POST /reports/generate
{
  "type": "activity_audit",
  "period": {"start": "2025-07-01", "end": "2025-07-31"},
  "format": "csv"
}
```

### Problem: Tender Status Updates Not Syncing

**Symptoms:**
- Status changes don't appear for all team members
- Conflicting tender statuses
- Updates lost or overwritten

**Solutions:**

**1. Check Sync Status**
```bash
GET /workspace/sync-status

{
  "last_sync": "2025-08-01T15:30:00Z",
  "pending_updates": 0,
  "sync_conflicts": []
}
```

**2. Force Sync**
```bash
POST /workspace/force-sync
{
  "clear_cache": true,
  "resolve_conflicts": "latest_wins"
}
```

**3. Conflict Resolution**
```bash
# Resolve specific conflicts
PATCH /workspace/tenders/{tender_id}/resolve-conflict
{
  "resolution_strategy": "merge",
  "keep_fields": ["status", "notes"],
  "discard_fields": ["old_priority"]
}
```

---

## Performance Issues

### Problem: Slow Page Load Times

**Symptoms:**
- Pages take >5 seconds to load
- Browser appears frozen
- Partial content loading

**Diagnostic Steps:**

**1. Network Analysis**
```bash
# Test API response times
curl -w "@curl-format.txt" -s -o /dev/null \
     -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.tenderinsighthub.co.za/v1/tenders/search?q=test

# curl-format.txt content:
#     time_namelookup:  %{time_namelookup}\n
#     time_connect:     %{time_connect}\n
#     time_appconnect:  %{time_appconnect}\n
#     time_pretransfer: %{time_pretransfer}\n
#     time_redirect:    %{time_redirect}\n
#     time_starttransfer: %{time_starttransfer}\n
#     time_total:       %{time_total}\n
```

**2. Browser Performance**
- Open Developer Tools > Performance tab
- Record page load and analyze bottlenecks
- Check for memory leaks or excessive DOM elements

**Solutions:**

**1. Browser Optimization**
```javascript
// Clear browser cache programmatically
if ('caches' in window) {
    caches.keys().then(names => {
        names.forEach(name => {
            caches.delete(name);
        });
    });
}

// Disable browser extensions temporarily
// Check if ad blockers are interfering
```

**2. Connection Issues**
- Try different internet connection
- Use VPN if corporate firewall is blocking
- Check DNS resolution issues

**3. Pagination and Data Limiting**
```bash
# Reduce data per request
GET /tenders/search?q=construction&limit=10&fields=id,title,deadline

# Use pagination instead of loading all data
GET /tenders/search?offset=0&limit=20
```

### Problem: API Rate Limit Exceeded

**Symptoms:**
- HTTP 429 responses
- "Rate limit exceeded" errors
- Temporary API access blocks

**Solutions:**

**1. Implement Rate Limiting**
```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests=100, time_window=3600):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    def can_make_request(self):
        now = time.time()
        # Remove old requests outside time window
        while self.requests and self.requests[0] <= now - self.time_window:
            self.requests.popleft()
        
        return len(self.requests) < self.max_requests
    
    def make_request(self):
        if self.can_make_request():
            self.requests.append(time.time())
            return True
        return False

# Usage
limiter = RateLimiter(max_requests=100, time_window=3600)
if limiter.make_request():
    # Make API call
    response = requests.get(url, headers=headers)
else:
    print("Rate limit reached, waiting...")
    time.sleep(60)
```

**2. Request Optimization**
```bash
# Batch multiple operations
POST /batch
{
  "operations": [
    {"method": "GET", "path": "/tenders/TND-001"},
    {"method": "GET", "path": "/tenders/TND-002"},
    {"method": "GET", "path": "/tenders/TND-003"}
  ]
}

# Use field selection to reduce response size
GET /tenders/search?fields=id,title,deadline,budget
```

**3. Caching Strategy**
```python
import redis
import json

# Redis caching to reduce API calls
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cached_api_call(endpoint, params, cache_ttl=3600):
    cache_key = f"api:{endpoint}:{hash(str(params))}"
    
    # Check cache first
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)
    
    # Make API call
    response = requests.get(f"{BASE_URL}{endpoint}", params=params, headers=headers)
    result = response.json()
    
    # Cache result
    redis_client.setex(cache_key, cache_ttl, json.dumps(result))
    return result
```

### Problem: Document Processing Timeouts

**Symptoms:**
- Analysis never completes
- Timeout errors after long waits
- Processing stuck at partial completion

**Solutions:**

**1. Document Size Management**
```python
def optimize_pdf_for_analysis(input_path, output_path, max_pages=50):
    import PyPDF2
    
    with open(input_path, 'rb') as infile:
        reader = PyPDF2.PdfFileReader(infile)
        writer = PyPDF2.PdfFileWriter()
        
        # Only process first N pages for faster analysis
        for i in range(min(reader.numPages, max_pages)):
            writer.addPage(reader.getPage(i))
        
        with open(output_path, 'wb') as outfile:
            writer.write(outfile)
```

**2. Async Processing with Status Checks**
```python
def analyze_document_async(file_path, timeout=300):
    # Start analysis
    response = requests.post(
        f"{BASE_URL}/documents/analyze",
        files={'document': open(file_path, 'rb')},
        headers=headers
    )
    
    document_id = response.json()['document_id']
    
    # Poll for completion
    start_time = time.time()
    while time.time() - start_time < timeout:
        status_response = requests.get(
            f"{BASE_URL}/documents/{document_id}/status",
            headers=headers
        )
        
        status = status_response.json()['status']
        if status == 'completed':
            return requests.get(
                f"{BASE_URL}/documents/{document_id}/analysis",
                headers=headers
            ).json()
        elif status == 'failed':
            raise Exception("Document analysis failed")
        
        time.sleep(10)  # Wait 10 seconds before checking again
    
    raise TimeoutError("Document analysis timed out")
```

---

## API Integration Problems

### Problem: CORS Errors in Browser

**Symptoms:**
- "CORS policy" error messages
- API calls fail from web applications
- Preflight OPTIONS requests failing

**Solutions:**

**1. Check Domain Configuration**
```bash
# Verify your domain is allowlisted
GET /team/cors-domains

{
  "allowed_domains": [
    "https://yourapp.com",
    "https://staging.yourapp.com"
  ]
}

# Add domain if missing
POST /team/cors-domains
{
  "domain": "https://yourapp.com"
}
```

**2. Proper CORS Headers**
```javascript
// Frontend CORS configuration
const response = await fetch('https://api.tenderinsighthub.co.za/v1/tenders/search', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  mode: 'cors',
  credentials: 'same-origin'
});
```

**3. Server-Side Proxy (Alternative)**
```javascript
// If CORS issues persist, use server-side proxy
app.get('/api/tenders/*', async (req, res) => {
  const apiResponse = await fetch(
    `https://api.tenderinsighthub.co.za/v1${req.path}`,
    {
      headers: {
        'Authorization': `Bearer ${process.env.TENDER_API_KEY}`,
        'Content-Type': 'application/json'
      }
    }
  );
  
  const data = await apiResponse.json();
  res.json(data);
});
```

### Problem: Webhook Delivery Failures

**Symptoms:**
- Webhooks not reaching your endpoint
- Intermittent webhook delivery
- Webhook verification failures

**Diagnostic Steps:**

**1. Test Webhook Endpoint**
```bash
# Test your webhook endpoint manually
curl -X POST https://yourapp.com/webhook/tender-insights \
  -H "Content-Type: application/json" \
  -H "X-Signature: sha256=test" \
  -d '{
    "event": "tender.new",
    "timestamp": "2025-08-01T15:30:00Z",
    "data": {"tender_id": "test"}
  }'
```

**2. Check Webhook Configuration**
```bash
GET /webhooks

{
  "webhooks": [
    {
      "id": "webhook_123",
      "url": "https://yourapp.com/webhook/tender-insights",
      "events": ["tender.new", "analysis.completed"],
      "status": "active",
      "last_success": "2025-08-01T14:30:00Z",
      "last_failure": null,
      "failure_count": 0
    }
  ]
}
```

**Solutions:**

**1. Webhook Verification**
```python
import hmac
import hashlib

def verify_webhook_signature(payload, signature, secret):
    # Calculate expected signature
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures
    expected = f"sha256={expected_signature}"
    return hmac.compare_digest(expected, signature)

# Flask example
@app.route('/webhook/tender-insights', methods=['POST'])
def handle_webhook():
    payload = request.get_data(as_text=True)
    signature = request.headers.get('X-Signature')
    
    if not verify_webhook_signature(payload, signature, WEBHOOK_SECRET):
        return 'Invalid signature', 401
    
    # Process webhook data
    data = request.get_json()
    process_tender_event(data)
    
    return 'OK', 200
```

**2. Retry Logic and Error Handling**
```python
# Webhook endpoint with proper error handling
@app.route('/webhook/tender-insights', methods=['POST'])
def handle_webhook():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('event') or not data.get('data'):
            return 'Invalid payload', 400
        
        # Process event
        result = process_webhook_event(data)
        
        if result:
            return 'OK', 200
        else:
            return 'Processing failed', 500
            
    except Exception as e:
        # Log error for debugging
        logger.error(f"Webhook processing failed: {str(e)}")
        return 'Internal error', 500
```

**3. Webhook Testing and Debugging**
```bash
# Test webhook delivery manually
POST /webhooks/{webhook_id}/test
{
  "event": "tender.new",
  "test_data": true
}

# Check webhook delivery logs
GET /webhooks/{webhook_id}/deliveries?limit=10
```

### Problem: SDK Integration Issues

**Symptoms:**
- SDK methods not working as expected
- Version compatibility problems
- Missing or outdated documentation

**Solutions:**

**1. Version Management**
```bash
# Check SDK version
pip show tender-insight-sdk

# Update to latest version
pip install --upgrade tender-insight-sdk

# Install specific version if needed
pip install tender-insight-sdk==1.2.3
```

**2. SDK Configuration**
```python
from tender_insight import TenderInsightClient, TenderInsightError

# Proper SDK initialization with error handling
try:
    client = TenderInsightClient(
        api_key=os.getenv('TENDER_API_KEY'),
        base_url='https://api.tenderinsighthub.co.za/v1',
        timeout=30,
        retry_attempts=3
    )
    
    # Test connection
    health = client.get_health()
    print(f"API Status: {health.status}")
    
except TenderInsightError as e:
    print(f"SDK Error: {e.message}")
    print(f"Error Code: {e.code}")
```

**3. Fallback to Direct API Calls**
```python
# If SDK fails, use direct API calls
import requests

class TenderAPIClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def search_tenders(self, query, **filters):
        params = {'q': query, **filters}
        response = self.session.get(f'{self.base_url}/tenders/search', params=params)
        response.raise_for_status()
        return response.json()
```

---

## Premium Features Issues

### Problem: Analytics Dashboard Not Loading

**Symptoms:**
- Dashboard shows loading indefinitely
- Charts not rendering
- Data not appearing despite valid subscription

**Solutions:**

**1. Check Subscription Status**
```bash
GET /team/subscription

{
  "plan": "pro",
  "status": "active",
  "features": {
    "advanced_analytics": true,
    "report_generation": true,
    "api_access": true
  },
  "usage": {
    "analytics_queries": 45,
    "monthly_limit": 1000
  }
}
```

**2. Browser Compatibility**
```javascript
// Check if browser supports required features
const browserSupport = {
  webgl: !!window.WebGLRenderingContext,
  canvas: !!document.createElement('canvas').getContext,
  svg: !!(document.createElementNS && document.createElementNS('http://www.w3.org/2000/svg', 'svg').createSVGRect),
  flexbox: CSS.supports('display', 'flex')
};

console.log('Browser support:', browserSupport);
```
