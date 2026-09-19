# Security Architecture & Posture Documentation: FC-05

This document specifies the security controls, cryptographic protections, threat mitigations, and architectural boundaries implemented in the **FC-05 Real-Time Financial Fraud Detection Engine**.

---

## 1. Authentication & Identity Management
- **Password Hashing**: Passwords are never stored in plaintext. They are hashed using **native Bcrypt** with 12 salt rounds (`bcrypt.gensalt(12)`). Bcrypt's 72-byte truncation boundary is enforced explicitly to prevent payload manipulation.
- **Multi-Factor Authentication (MFA)**: Authenticated sessions require a two-step challenge. For prototype demonstration, a simulated OTP flow (`123456`) verifies the cryptographic handshake without relying on third-party SMS/telecom gateways.
- **JSON Web Tokens (JWT)**:
  - Tokens are signed with HMAC-SHA256 (`HS256`) using a strong secret loaded from environment variables (`JWT_SECRET`).
  - Strict expiration timestamps (`exp`) are embedded and validated on every request.
  - Active session invalidation on logout is achieved via a server-side token revocation blacklist (`REVOKED_TOKENS`).

---

## 2. Authorization & Role-Based Access Control (RBAC)
Every incoming request to a protected endpoint passes through FastAPI security dependencies (`require_roles`):
- **CUSTOMER**: Restricted to own account transactions (`/transactions`).
- **FRAUD_ANALYST**: Authorized to triage alerts (`/fraud-alerts`), inspect dossiers (`/investigation/{id}`), and query the RAG forensic assistant (`/ai/investigate`).
- **MANAGER**: Authorized to review aggregate risk statistics, audit logs, and compliance reporting.
- **ADMIN**: Authorized to reassign operator roles (`/admin/users/{id}/role`) and monitor SIEM telemetry.
- **Backend Enforcement**: Authorization is enforced strictly on the server; client UI hides buttons purely for usability.

---

## 3. API Security & Threat Defense
- **Input Validation**: Handled via Pydantic v2 schemas:
  - Positive numeric bounds on transaction amounts (`0 < amount <= 10,000,000`).
  - Geographic boundaries (`-90 <= latitude <= 90`, `-180 <= longitude <= 180`).
  - Regex pattern matching on statuses and risk classifications.
  - Reject oversized request payloads (> 2MB) via `RequestSizeLimitMiddleware` to prevent memory exhaustion DoS.
- **SQL Injection Defense**: All database operations use SQLAlchemy ORM parameterized queries. Raw user strings are never concatenated into SQL statements.
- **Safe Error Handling**: Global exception handlers catch unhandled server exceptions, log detailed technical traces internally, and return sanitized, generic error messages to the client (e.g., `"An internal error occurred. Technical details have been securely logged."`). Raw stack traces, database credentials, or file paths are never exposed.
- **Rate Limiting**:
  - Sliding-window in-memory rate limiter protects endpoints against brute-force attacks and denial-of-service.
  - Authentication routes (`/auth/login`, `/auth/verify-mfa`) are throttled at 15 requests/minute.
  - General API routes are throttled at 60 requests/minute.
  - Breaching rate limits returns `HTTP 429 Too Many Requests` with a `Retry-After` header and records an automated SIEM security event.

---

## 4. Network & Transport Layer (HTTPS/TLS)
- In production configurations, traffic terminates over TLS 1.3.
- Application includes `Strict-Transport-Security` (`HSTS`: `max-age=31536000; includeSubDomains`).
- Cross-Origin Resource Sharing (CORS) enforces an explicit origin whitelist (`http://localhost:5173`, `http://127.0.0.1:5173`). Wildcard `*` origins are forbidden.

---

## 5. Defense-in-Depth Security Headers
The following HTTP security response headers are injected on all outgoing responses via `SecurityHeadersMiddleware`:
```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self' http://localhost:8000 http://127.0.0.1:8000 http://localhost:5173 http://127.0.0.1:5173;
```

---

## 6. Sensitive Data Protection & Minimization
- **Account Number Masking**: Account numbers are masked across API responses, frontend dashboards, and audit logs keeping only the last 4 digits visible:
  `XXXX-XXXX-XXXX-4521`
- **Email Masking**: User emails in telemetry records are obfuscated (`a*****t@finsecure.com`).
- **Credential Sanitization**: The `sanitize_for_logging` utility scrubs passwords, tokens, and keys before writing to application log streams.

---

## 7. AI & RAG Security Layer
- **No Hallucinated Facts**: The AI assistant (`/ai/investigate`) is prevented from inventing transaction amounts, devices, or IDs. All factual assertions are derived strictly from database records and the computed fraud engine output.
- **Untrusted RAG Content**: Retrieved SOP policy documents are treated strictly as data citations, never as executable code or system instructions.
- **Prompt Injection Defense**: Inputs are sanitized against jailbreak vectors (`ignore previous instructions`, `admin override`, `system:`, `exec()`).
- **Zero Financial Execution Capability**: The LLM model has zero autonomous capability to trigger settlements, alter balances, or bypass backend authorization rules.

---

## 8. Immutable Audit Logging & SIEM Monitoring
- Every authentication attempt, password failure, role update, fraud analysis, and AI inquiry generates an immutable entry in `audit_logs` capturing:
  - Subject User ID & Email
  - Action Event
  - Target Resource
  - Client IP Address
  - Masked Telemetry JSON
  - UTC Timestamp
- Security events (failed logins, rate limit breaches, rapid transaction bursts) trigger dedicated SIEM records viewable in the Security Operations dashboard.

---

## 9. Known Limitations & Production Requirements
As a hackathon prototype, this system uses synthetic financial data. Production deployment would require:
1. Hardware Security Module (HSM) or KMS for cryptographic key lifecycle management.
2. Enterprise Redis cluster for distributed rate limiting across multi-region server pools.
3. Multi-channel real-time SMS/FIDO2 WebAuthn hardware keys for biometric MFA.
4. PCI-DSS Level 1 compliance validation and SOC 2 Type II controls.
5. End-to-end TLS certificate pinning on client mobile applications.
