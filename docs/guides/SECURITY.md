# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by:

1. **Do NOT open a public issue**
2. Email the maintainers directly
3. Include details:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We take security seriously and will respond within 48 hours.

## Security Best Practices

When using this project:

### API Keys
- **Never commit API keys** to version control
- Use `.env` file (already in .gitignore)
- Rotate keys regularly
- Use environment-specific keys (dev vs prod)

### Authentication State
- `auth_state.json` contains session cookies
- Keep this file secure and never commit
- Rotate sessions regularly
- Use separate auth for different environments

### Dependencies
- Keep dependencies updated
- Run `pip audit` to check for vulnerabilities
- Review dependency updates before installing

### Logs
- Log files may contain sensitive information
- Logs directory is in .gitignore
- Review logs before sharing
- Sanitize logs in production

### Network Security
- Use HTTPS for all API calls
- Validate SSL certificates
- Be cautious with proxy settings
- Limit network access in production

## Known Security Considerations

1. **LLM API Keys**: Required for operation, keep secure
2. **Browser Sessions**: Authentication state persists, rotate regularly
3. **Generated Code**: Review AI-generated tests before production use
4. **Logs**: May contain application URLs and element references
5. **MCP Tools**: Have filesystem access, use in trusted environments

## Updates

Security updates will be released as patch versions (1.0.x).
Subscribe to repository releases for notifications.
