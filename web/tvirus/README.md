# Cache-Confusion

- REST API with cache mappings installed after the first database fetch
- Cache Fingerprint: `UNAME:sha256:<SHA256(Username)[:6]>UA:sha256:<SHA256(Admin UserAgent)[:16]>URI:sha256:<SHA256(URI)[:16]>`
- Cache fingerprint algorithm revealed by HTTP Header.
- Admin username revealed by IDOR on user's page.
- Server UserAgent revealed by SSRF.
- Get /flag when you have username collision and user agent
