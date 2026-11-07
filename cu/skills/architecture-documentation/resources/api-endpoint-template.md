---
endpoint_id: API-NNN
endpoint_path: '/api/v1/resource'
http_method: GET
api_version: v1
status: draft
author: ''
created: YYYY-MM-DD
last_modified: YYYY-MM-DD
category: ''
authentication_required: true
rate_limit: ''
deprecated: false
related_endpoints: []
tags: []
---

## Endpoint Overview

**Path**: `[HTTP METHOD] /api/v1/resource/{param}`

**Description**: [One-sentence description of what this endpoint does]

**Use Case**: [Brief description of when and why to use this endpoint]

**Business Value**: [How this endpoint supports business goals or user needs]

---

## Authentication & Authorisation

**Authentication Method**: [JWT Bearer Token / API Key / OAuth2 / Session / None]

**Required Permissions**:

- [Permission/Role 1]: [Description of what this permission allows]
- [Permission/Role 2]: [Description of what this permission allows]

**Authorisation Rules**:

- [Rule 1]: Users can only access their own resources
- [Rule 2]: Admin role required for modification
- [Row-Level Security]: [Enabled/Disabled] **[RLS]**

**Authentication Header Example**:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Request Specification

### HTTP Method & Path

```http
[GET|POST|PUT|PATCH|DELETE] /api/v1/resource/{resourceId}
```

**Path Parameters**: | Parameter | Type | Required | Description | Validation |
|-----------|------|----------|-------------|------------| | `resourceId` | string (UUID) | Yes |
Unique resource identifier | Must be valid UUID v4 | | `[param]` | [type] | [Yes/No] | [Description]
| [Validation rules] |

**Query Parameters**: | Parameter | Type | Required | Default | Description | Validation |
|-----------|------|----------|---------|-------------|------------| | `page` | integer | No | 1 |
Page number for pagination | Min: 1, Max: 1000 | | `limit` | integer | No | 20 | Items per page |
Min: 1, Max: 100 | | `sort` | string | No | created_at | Sort field | Allowed: [created_at,
updated_at, name] | | `order` | string | No | desc | Sort order | Allowed: [asc, desc] | | `filter`
| string | No | null | Filter criteria | Max length: 255 chars |

### Request Headers

**Required Headers**:

```http
Content-Type: application/json
Authorization: Bearer {token}
X-Request-ID: {uuid}      # For request tracing
```

**Optional Headers**:

```http
Accept-Language: en-US     # Localisation (EN/FR/DE supported)
X-API-Version: v1          # API version override
```

### Request Body

**Content-Type**: `application/json`

**Schema** (JSON Schema):

```json
{
  "type": "object",
  "required": ["field1", "field2"],
  "properties": {
    "field1": {
      "type": "string",
      "minLength": 1,
      "maxLength": 255,
      "description": "Brief description of field1"
    },
    "field2": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100,
      "description": "Brief description of field2"
    },
    "field3": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Optional array field"
    },
    "nested": {
      "type": "object",
      "properties": {
        "subfield": {
          "type": "string"
        }
      }
    }
  },
  "additionalProperties": false
}
```

**Example Request Body**:

```json
{
  "field1": "example value",
  "field2": 42,
  "field3": ["item1", "item2"],
  "nested": {
    "subfield": "nested value"
  }
}
```

**Validation Rules** [IV]:

- All required fields must be present
- Field types must match schema
- String length constraints enforced
- Numeric ranges validated
- No additional properties allowed (strict schema)
- Special characters sanitised to prevent injection attacks

---

## Response Specification

### Success Response (200 OK / 201 Created / 204 No Content)

**Status Code**: `200 OK` (for GET, PUT, PATCH) | `201 Created` (for POST) | `204 No Content` (for
DELETE)

**Response Headers**:

```http
Content-Type: application/json
X-Request-ID: {uuid}
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1635724800
```

**Response Body Schema**:

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier"
    },
    "field1": {
      "type": "string",
      "description": "Same field from request"
    },
    "createdAt": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp"
    },
    "updatedAt": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp"
    }
  }
}
```

**Example Success Response (200 OK)**:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "field1": "example value",
  "field2": 42,
  "field3": ["item1", "item2"],
  "nested": {
    "subfield": "nested value"
  },
  "createdAt": "2025-10-26T14:30:00Z",
  "updatedAt": "2025-10-26T14:30:00Z",
  "links": {
    "self": "/api/v1/resource/550e8400-e29b-41d4-a716-446655440000",
    "related": "/api/v1/resource/550e8400-e29b-41d4-a716-446655440000/related"
  }
}
```

**Example Success Response (201 Created)**:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "field1": "example value",
  "createdAt": "2025-10-26T14:30:00Z",
  "links": {
    "self": "/api/v1/resource/550e8400-e29b-41d4-a716-446655440000"
  }
}
```

### Pagination Response (for List Endpoints)

**Envelope Format**:

```json
{
  "data": [
    {
      "id": "uuid1",
      "field1": "value1"
    },
    {
      "id": "uuid2",
      "field1": "value2"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "totalPages": 5,
    "totalItems": 97,
    "hasNext": true,
    "hasPrevious": false
  },
  "links": {
    "self": "/api/v1/resource?page=1&limit=20",
    "next": "/api/v1/resource?page=2&limit=20",
    "previous": null,
    "first": "/api/v1/resource?page=1&limit=20",
    "last": "/api/v1/resource?page=5&limit=20"
  }
}
```

---

## Error Responses

### Error Response Format (Standardised) [REH]

**General Structure**:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "User-friendly error message",
    "details": [
      {
        "field": "fieldName",
        "issue": "Specific issue with this field"
      }
    ],
    "requestId": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-10-26T14:30:00Z",
    "documentation": "https://api.example.com/docs/errors/ERROR_CODE"
  }
}
```

### HTTP Status Codes

**4xx Client Errors**:

#### 400 Bad Request

**Cause**: Invalid request syntax, validation failure **Example**:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "field1",
        "issue": "Field is required but was not provided"
      },
      {
        "field": "field2",
        "issue": "Value must be between 0 and 100"
      }
    ],
    "requestId": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-10-26T14:30:00Z"
  }
}
```

#### 401 Unauthorized

**Cause**: Missing or invalid authentication credentials **Example**:

```json
{
  "error": {
    "code": "AUTHENTICATION_REQUIRED",
    "message": "Authentication credentials are required",
    "requestId": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-10-26T14:30:00Z"
  }
}
```

#### 403 Forbidden

**Cause**: Valid credentials but insufficient permissions **Example**:

```json
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "You do not have permission to perform this action",
    "details": [
      {
        "required": "admin",
        "current": "user"
      }
    ],
    "requestId": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-10-26T14:30:00Z"
  }
}
```

#### 404 Not Found

**Cause**: Resource does not exist **Example**:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource was not found",
    "details": [
      {
        "resourceType": "Resource",
        "resourceId": "550e8400-e29b-41d4-a716-446655440000"
      }
    ],
    "requestId": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-10-26T14:30:00Z"
  }
}
```

#### 409 Conflict

**Cause**: Request conflicts with current state (e.g., duplicate resource) **Example**:

```json
{
  "error": {
    "code": "RESOURCE_CONFLICT",
    "message": "A resource with this identifier already exists",
    "details": [
      {
        "field": "email",
        "conflict": "Email address already registered"
      }
    ],
    "requestId": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-10-26T14:30:00Z"
  }
}
```

#### 422 Unprocessable Entity

**Cause**: Valid syntax but semantic errors (business rule violations) **Example**:

```json
{
  "error": {
    "code": "BUSINESS_RULE_VIOLATION",
    "message": "Cannot process request due to business rule violation",
    "details": [
      {
        "rule": "minimum_balance",
        "issue": "Account balance cannot go below zero"
      }
    ],
    "requestId": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-10-26T14:30:00Z"
  }
}
```

#### 429 Too Many Requests

**Cause**: Rate limit exceeded **Example**:

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "details": [
      {
        "limit": 1000,
        "remaining": 0,
        "resetAt": "2025-10-26T15:00:00Z"
      }
    ],
    "requestId": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-10-26T14:30:00Z"
  }
}
```

**5xx Server Errors**:

#### 500 Internal Server Error

**Cause**: Unexpected server-side error **Example**:

```json
{
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "An unexpected error occurred. Please try again later.",
    "requestId": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-10-26T14:30:00Z"
  }
}
```

#### 503 Service Unavailable

**Cause**: Service temporarily unavailable (maintenance, overload) **Example**:

```json
{
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "Service is temporarily unavailable. Please try again later.",
    "details": [
      {
        "retryAfter": 60,
        "reason": "scheduled_maintenance"
      }
    ],
    "requestId": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-10-26T14:30:00Z"
  }
}
```

---

## Rate Limiting [RL]

**Rate Limit Configuration**:

- **Limit**: [1000 requests per hour] per user/API key
- **Window**: [1 hour sliding window]
- **Scope**: [Per user / Per IP / Per API key]

**Rate Limit Headers** (in all responses):

```http
X-RateLimit-Limit: 1000          # Maximum requests allowed
X-RateLimit-Remaining: 999       # Requests remaining in window
X-RateLimit-Reset: 1635728400    # Unix timestamp when limit resets
Retry-After: 3600                # Seconds until retry (only on 429)
```

**Rate Limit Exceeded Behaviour**:

- HTTP 429 Too Many Requests returned
- Response includes `Retry-After` header
- Clients should implement exponential backoff

---

## Examples

### cURL Examples

**Example 1: Successful Request**

```bash
curl -X GET "https://api.example.com/api/v1/resource/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: $(uuidgen)"
```

**Example 2: Create Resource**

```bash
curl -X POST "https://api.example.com/api/v1/resource" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: $(uuidgen)" \
  -d '{
    "field1": "example value",
    "field2": 42,
    "field3": ["item1", "item2"]
  }'
```

**Example 3: Paginated List**

```bash
curl -X GET "https://api.example.com/api/v1/resource?page=2&limit=50&sort=created_at&order=desc" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json"
```

### JavaScript (Fetch API) Example

```javascript
const response = await fetch('https://api.example.com/api/v1/resource', {
  method: 'POST',
  headers: {
    Authorization: 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
    'Content-Type': 'application/json',
    'X-Request-ID': crypto.randomUUID(),
  },
  body: JSON.stringify({
    field1: 'example value',
    field2: 42,
    field3: ['item1', 'item2'],
  }),
});

if (!response.ok) {
  const error = await response.json();
  console.error('API Error:', error);
  throw new Error(error.error.message);
}

const data = await response.json();
console.log('Success:', data);
```

### Python (requests) Example

```python
import requests
import uuid

url = 'https://api.example.com/api/v1/resource'
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
    'Content-Type': 'application/json',
    'X-Request-ID': str(uuid.uuid4())
}
payload = {
    'field1': 'example value',
    'field2': 42,
    'field3': ['item1', 'item2']
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 201:
    data = response.json()
    print('Success:', data)
else:
    error = response.json()
    print('Error:', error['error']['message'])
```

---

## Testing & Validation

### Test Scenarios

**Happy Path Tests**:

- [ ] Valid request with all required fields returns 200/201
- [ ] Response schema matches specification
- [ ] Response includes all expected fields
- [ ] Timestamps are in ISO 8601 format
- [ ] Links (HATEOAS) are correctly formatted

**Validation Tests** [IV]:

- [ ] Missing required field returns 400 with clear error message
- [ ] Invalid field type returns 400 with validation details
- [ ] Field length exceeds maximum returns 400
- [ ] Invalid enum value returns 400
- [ ] Additional properties rejected (strict schema enforcement)

**Authentication Tests**:

- [ ] Missing auth header returns 401
- [ ] Invalid token returns 401
- [ ] Expired token returns 401
- [ ] Valid token with insufficient permissions returns 403

**Error Handling Tests** [REH]:

- [ ] Non-existent resource returns 404
- [ ] Duplicate resource creation returns 409
- [ ] Rate limit exceeded returns 429 with Retry-After header
- [ ] Server error returns 500 with error tracking ID

**Performance Tests**:

- [ ] Response time < 200ms (p95) for simple requests
- [ ] Response time < 500ms (p95) for complex queries
- [ ] Pagination works correctly for large datasets
- [ ] Concurrent requests handled correctly (no race conditions)

### Postman Collection

**Collection Location**: `docs-copper/architecture/apis/postman/API-NNN-collection.json`

**Test Scripts Included**:

- Schema validation (using JSON Schema)
- Status code assertions
- Response time checks
- Authentication token management
- Environment variable configuration

---

## OpenAPI Specification

**OpenAPI Spec Location**: `docs-copper/architecture/apis/openapi/API-NNN-spec.yaml`

**Spec Fragment** (YAML):

```yaml
openapi: 3.0.3
info:
  title: [API Name]
  version: v1
  description: [API Description]

paths:
  /api/v1/resource:
    post:
      summary: Create a new resource
      operationId: createResource
      security:
        - bearerAuth: []
      tags:
        - Resources
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ResourceCreate'
      responses:
        '201':
          description: Resource created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    ResourceCreate:
      type: object
      required:
        - field1
        - field2
      properties:
        field1:
          type: string
          minLength: 1
          maxLength: 255
        field2:
          type: integer
          minimum: 0
          maximum: 100

    Resource:
      allOf:
        - $ref: '#/components/schemas/ResourceCreate'
        - type: object
          properties:
            id:
              type: string
              format: uuid
            createdAt:
              type: string
              format: date-time
            updatedAt:
              type: string
              format: date-time

  responses:
    BadRequest:
      description: Bad request (validation error)
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

---

## Performance & Scalability

**Expected Performance**:

- Response time: < 200ms (p95) for simple queries
- Response time: < 500ms (p95) for complex queries
- Throughput: [XXX requests/second]
- Concurrent connections: [XXX simultaneous requests]

**Caching Strategy**:

- Cache-Control headers: [public/private, max-age=XXX]
- ETags: [Enabled/Disabled]
- Conditional requests: [If-None-Match, If-Modified-Since]

**Database Optimisation**:

- Indexes: [List relevant database indexes]
- Query optimisation: [Specific query patterns used]
- Connection pooling: [Configuration details]

---

## Security Considerations [SFT]

**Input Validation** [IV]:

- All inputs validated against schema before processing
- SQL injection prevented via parameterised queries
- XSS prevented via output encoding
- Path traversal prevented via whitelist validation

**Data Protection**:

- Sensitive fields redacted in logs (passwords, tokens, credit cards)
- PII encrypted at rest and in transit
- HTTPS enforced (TLS 1.3 minimum)

**OWASP Top 10 Mitigations**:

- [ ] A01: Broken Access Control - Authorisation checks on all endpoints
- [ ] A02: Cryptographic Failures - Proper encryption of sensitive data
- [ ] A03: Injection - Input validation and parameterised queries
- [ ] A04: Insecure Design - Threat modelling conducted
- [ ] A05: Security Misconfiguration - Secure defaults enforced
- [ ] A07: Identification and Authentication Failures - Strong auth required
- [ ] A08: Software and Data Integrity Failures - Integrity checks in place
- [ ] A09: Security Logging and Monitoring Failures - Comprehensive logging

---

## Deprecation & Versioning

**Current Version**: v1

**Versioning Strategy**:

- URL path versioning: `/api/v1/`, `/api/v2/`
- Backward compatibility maintained within major version
- Breaking changes require new major version

**Deprecation Notice** (if applicable):

```json
{
  "warning": {
    "code": "DEPRECATED",
    "message": "This endpoint will be removed in v3. Please migrate to /api/v2/new-resource",
    "sunsetDate": "2026-10-26",
    "replacement": "/api/v2/new-resource",
    "documentation": "https://api.example.com/docs/migration-guide"
  },
  "data": {
    ...
  }
}
```

**Sunset Headers** (for deprecated endpoints):

```http
Sunset: Sat, 26 Oct 2026 00:00:00 GMT
Link: </api/v2/new-resource>; rel="alternate"
```

---

**Endpoint Status**: [draft | in-review | active | deprecated | sunset] **Last Updated**: YYYY-MM-DD

---

> [!tip]- TEMPLATE USAGE GUIDELINES **To be excluded from the generated API endpoint
> documentation.**
>
> **INSTRUCTIONS FOR COMPLETING THIS TEMPLATE**:
>
> 1. Create endpoint doc at: `docs-copper/architecture/apis/endpoints/API-NNN-name.md`
> 2. Naming convention: `API-NNN-kebab-case-endpoint-name.md`
> 3. Replace all [placeholder text] with actual API details
> 4. Update YAML frontmatter with endpoint metadata
> 5. Document ALL possible HTTP status codes (success + errors)
> 6. Provide realistic request/response examples
> 7. Create matching OpenAPI spec in `docs-copper/architecture/apis/openapi/`
> 8. Create Postman collection in `docs-copper/architecture/apis/postman/`
> 9. Tag all security considerations with principle codes
> 10. Delete this entire callout section before finalising
>
> **WHEN TO CREATE API ENDPOINT DOCUMENTATION**:
>
> - For every new API endpoint (GET, POST, PUT, PATCH, DELETE)
> - When modifying existing endpoint behaviour (breaking or non-breaking)
> - Before deploying API to production
> - When API contracts need to be shared with consumers
> - For internal microservice APIs requiring documentation
>
> **API DOCUMENTATION WORKFLOW**:
>
> **Before Implementation**:
>
> 1. Define endpoint contract (method, path, request, response)
> 2. Design request/response schema (JSON Schema)
> 3. Document authentication and authorisation requirements
> 4. Identify all possible status codes (success + errors)
> 5. Review with stakeholders (product, security, consumers)
>
> **During Implementation**:
>
> 1. Implement endpoint following documented contract
> 2. Write OpenAPI specification matching documentation
> 3. Create Postman collection for testing
> 4. Write unit tests validating schema and behaviour
> 5. Write integration tests covering error scenarios
>
> **Before Deployment**:
>
> 1. Validate OpenAPI spec with linting tools
> 2. Test all examples in Postman collection
> 3. Verify error responses match documentation
> 4. Review security considerations (OWASP Top 10)
> 5. Obtain approval from API consumers
>
> **After Deployment**:
>
> 1. Publish OpenAPI spec to API portal/documentation site
> 2. Share Postman collection with consumers
> 3. Monitor API usage and error rates
> 4. Update documentation for any deviations found
> 5. Maintain changelog for all endpoint changes
>
> **FRONTMATTER FIELD GUIDANCE**:
>
> - `endpoint_id`: Format `API-NNN` (sequential numbering)
> - `endpoint_path`: Full path including version (e.g., `/api/v1/users`)
> - `http_method`: GET | POST | PUT | PATCH | DELETE
> - `api_version`: v1 | v2 | etc.
> - `status`: draft | in-review | active | deprecated | sunset
> - `author`: Primary API developer
> - `created`: YYYY-MM-DD (creation date)
> - `last_modified`: YYYY-MM-DD (last update date)
> - `category`: authentication | users | products | orders | payments | etc.
> - `authentication_required`: true | false
> - `rate_limit`: Requests per time period (e.g., "1000/hour")
> - `deprecated`: true | false
> - `related_endpoints`: Array of related endpoint IDs
> - `tags`: Array of tags for categorisation
>
> **SCHEMA DOCUMENTATION BEST PRACTICES**:
>
> - Use JSON Schema for request/response validation
> - Document all required vs optional fields explicitly
> - Specify data types, formats, lengths, ranges
> - Provide realistic examples (not just "string" or "123")
> - Document nested objects and arrays thoroughly
> - Use `additionalProperties: false` for strict schemas
> - Include descriptions for every field
>
> **ERROR RESPONSE STANDARDS**:
>
> - Always use standardised error format (code, message, details, requestId)
> - Document ALL possible error codes (don't leave any undocumented)
> - Provide clear, actionable error messages for clients
> - Include field-level validation errors in `details` array
> - Return `requestId` for troubleshooting and support
> - Log errors server-side with same `requestId` for correlation
>
> **AUTHENTICATION & AUTHORISATION**:
>
> - Clearly state authentication method (JWT, OAuth2, API Key, etc.)
> - Document required permissions/roles for authorisation
> - Provide example authentication header
> - Explain token format and expiration
> - Document how to obtain and refresh tokens
> - Specify row-level security rules if applicable **[RLS]**
>
> **RATE LIMITING BEST PRACTICES** [RL]:
>
> - Document rate limit (requests per time period)
> - Specify rate limit scope (per user, IP, API key)
> - Include rate limit headers in all responses
> - Document 429 response and retry strategy
> - Recommend exponential backoff for clients
> - Consider different limits for different tiers (free, premium, enterprise)
>
> **TESTING CHECKLIST**:
>
> - [ ] All success scenarios tested (200, 201, 204)
> - [ ] All error scenarios tested (400, 401, 403, 404, 409, 422, 429, 500, 503)
> - [ ] Request schema validation tested (required fields, types, lengths)
> - [ ] Response schema validation tested (structure, types, formats)
> - [ ] Authentication tested (missing, invalid, expired tokens)
> - [ ] Authorisation tested (insufficient permissions)
> - [ ] Rate limiting tested (exceeding limits returns 429)
> - [ ] Performance tested (response times meet targets)
> - [ ] Concurrent requests tested (no race conditions)
> - [ ] Pagination tested (for list endpoints)
>
> **INTEGRATION WITH OTHER ARTEFACTS**:
>
> - **OpenAPI Spec**: Create matching spec in `docs-copper/architecture/apis/openapi/`
> - **Postman Collection**: Create tests in `docs-copper/architecture/apis/postman/`
> - **Technical Design**: Reference from technical design documents
> - **User Stories**: Link to user stories requiring this endpoint
> - **ADRs**: Reference architectural decisions affecting API design
> - **Memory Bank**: Update `techContext.md` with API patterns
>
> **SWISS MARKET BEST PRACTICES**:
>
> - **Precision**: Exact specifications for all fields, no ambiguity
> - **Completeness**: Document every scenario, edge case, error condition
> - **Multilingual**: Support Accept-Language header (EN/FR/DE)
> - **Quality**: Comprehensive testing before documentation approval
> - **Security**: Swiss data protection standards (GDPR-compliant)
> - **Long-term**: API versioning strategy for backward compatibility
>
> **PRINCIPLE CODE USAGE**: Tag API design decisions with relevant principle codes:
>
> - **[IV]** Input Validation: All inputs validated against schema
> - **[SFT]** Security-First Thinking: Authentication, authorisation, encryption
> - **[RL]** Rate Limiting: Rate limits enforced to prevent abuse
> - **[RLS]** Row Level Security: User can only access their own data
> - **[REH]** Robust Error Handling: Comprehensive error responses
> - **[SD]** Strategic Documentation: Complete API documentation
> - **[ISA]** Industry Standards: REST, OpenAPI, HATEOAS compliance
>
> **COMMON PITFALLS TO AVOID**:
>
> 1. **Undocumented Errors**: Always document ALL possible HTTP status codes
> 2. **Vague Schemas**: "string" is not sufficient - specify format, length, pattern
> 3. **Missing Examples**: Provide realistic request/response examples
> 4. **Inconsistent Error Format**: Use standardised error structure everywhere
> 5. **No Authentication Details**: Clearly document auth method and headers
> 6. **Ignoring Rate Limits**: Document limits and include headers
> 7. **No Versioning Strategy**: Plan for API evolution and breaking changes
> 8. **Missing Postman Collection**: Manual testing is slow and error-prone
>
> **OPENAPI SPECIFICATION TIPS**:
>
> - Use OpenAPI 3.0+ (not Swagger 2.0)
> - Validate spec with `openapi-generator validate`
> - Generate client SDKs from spec for testing
> - Use `$ref` to avoid schema duplication
> - Document security schemes comprehensively
> - Include examples in schema definitions
> - Use `operationId` for code generation
> - Tag endpoints for logical grouping

> [!info]- TEMPLATE DATA (YAML BackMatter) For indexing, search, and validation purposes. **To be
> excluded from the generated API endpoint documentation.**
>
> ```yaml
> template_name: 'API Endpoint Documentation Template'
> template_description:
>   'Comprehensive template for documenting REST API endpoints including request/response specs,
>   authentication, error codes, examples, and testing guidance'
> template_scope:
>   'Use for all API endpoints (GET, POST, PUT, PATCH, DELETE) requiring documentation for consumers
>   or internal teams'
> template_version: '1.0.0'
> template_last_updated: '2025-10-26'
> template_status: 'active'
> template_category: 'api'
> template_maintained_by: '[Project Team]'
>
> principle_codes_emphasized:
>   - IV # Input Validation
>   - SFT # Security-First Thinking
>   - RL # Rate Limiting
>   - RLS # Row Level Security
>   - REH # Robust Error Handling
>   - SD # Strategic Documentation
>   - ISA # Industry Standards Adherence
>   - ORG # Organisational Clarity
>   - TST # Test Coverage
>
> cross_references:
>   - 'User Story Template: user-story-template.md'
>   - 'Technical Design Template: technical-design-template.md'
>   - 'ADR Template: adr-template.md'
>   - 'Dev Journal Template: dev-journal-template.md'
>   - 'Memory Bank: docs-copper/memory-bank/'
>   - 'OpenAPI Directory: docs-copper/architecture/apis/openapi/'
>   - 'Postman Collections: docs-copper/architecture/apis/postman/'
>
> applies_to:
>   - 'Backend developers implementing API endpoints'
>   - 'API consumers (frontend developers, third-party integrators)'
>   - 'Product owners defining API requirements'
>   - 'Security engineers reviewing API design'
>   - 'DevOps engineers configuring API gateways'
>   - 'QA engineers testing API functionality'
>
> usage_pattern:
>   when_to_create:
>     - 'For every new API endpoint (GET, POST, PUT, PATCH, DELETE)'
>     - 'When modifying existing endpoint behaviour (breaking or non-breaking)'
>     - 'Before deploying API to production environment'
>     - 'When API contracts need to be shared with consumers'
>     - 'For internal microservice APIs requiring documentation'
>     - 'When generating OpenAPI specifications'
>   naming_convention:
>     pattern: 'API-NNN-kebab-case-endpoint-name.md'
>     examples: 'API-001-create-user.md, API-002-list-products.md'
>   storage_location: 'docs-copper/architecture/apis/endpoints/'
>
> related_workflows:
>   - 'Create OpenAPI spec in docs-copper/architecture/apis/openapi/'
>   - 'Create Postman collection in docs-copper/architecture/apis/postman/'
>   - 'Reference from technical design documents'
>   - 'Link from user stories requiring this API'
>   - 'Update memory-bank/project-context/techContext.md with API patterns'
>   - 'Generate client SDKs from OpenAPI spec'
>   - 'Publish to API documentation portal/site'
>
> api_documentation_standards:
>   request_specification:
>     - 'HTTP method and path clearly stated'
>     - 'Path parameters documented with types and validation'
>     - 'Query parameters with defaults and allowed values'
>     - 'Request headers (required and optional)'
>     - 'Request body schema (JSON Schema)'
>     - 'Realistic request examples (cURL, JavaScript, Python)'
>   response_specification:
>     - 'Success status codes (200, 201, 204)'
>     - 'Response headers (rate limiting, caching)'
>     - 'Response body schema (JSON Schema)'
>     - 'Realistic response examples'
>     - 'Pagination envelope for list endpoints'
>   error_specification:
>     - 'All possible HTTP status codes documented'
>     - 'Standardised error response format'
>     - 'Field-level validation errors in details array'
>     - 'Request ID for troubleshooting'
>     - 'User-friendly error messages'
>   authentication:
>     - 'Authentication method clearly stated'
>     - 'Authorisation rules and required permissions'
>     - 'Example authentication headers'
>     - 'Token format and expiration details'
>   rate_limiting:
>     - 'Rate limit configuration documented'
>     - 'Rate limit headers in responses'
>     - '429 response and retry strategy'
>     - 'Exponential backoff recommendations'
>
> swiss_quality_emphasis:
>   - 'Precision in specifications (exact types, lengths, formats)'
>   - 'Comprehensive error documentation (no undocumented scenarios)'
>   - 'Multilingual support (Accept-Language header for EN/FR/DE)'
>   - 'Security by design (authentication, input validation, rate limiting)'
>   - 'Long-term API versioning strategy for stability'
>   - 'Quality testing before production deployment'
>
> testing_requirements:
>   success_scenarios:
>     - 'Valid requests return expected status codes'
>     - 'Response schemas match specifications'
>     - 'Response includes all documented fields'
>   validation_scenarios:
>     - 'Missing required fields return 400'
>     - 'Invalid field types return 400'
>     - 'Field length violations return 400'
>   authentication_scenarios:
>     - 'Missing auth returns 401'
>     - 'Invalid token returns 401'
>     - 'Insufficient permissions return 403'
>   error_scenarios:
>     - 'Non-existent resource returns 404'
>     - 'Conflicts return 409'
>     - 'Rate limit exceeded returns 429'
>     - 'Server errors return 500'
>   performance_scenarios:
>     - 'Response time < 200ms (p95) for simple queries'
>     - 'Response time < 500ms (p95) for complex queries'
>     - 'Concurrent requests handled correctly'
>
> external_references:
>   - 'OpenAPI Specification: https://swagger.io/specification/'
>   - 'REST API Design: https://restfulapi.net/'
>   - 'JSON Schema: https://json-schema.org/'
>   - 'OWASP API Security: https://owasp.org/www-project-api-security/'
>   - 'HTTP Status Codes: https://httpstatuses.com/'
>   - 'Rate Limiting: https://tools.ietf.org/id/draft-polli-ratelimit-headers-00.html'
> ```
