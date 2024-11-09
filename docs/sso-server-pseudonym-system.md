# SSO Server Pseudonym Management System

## Overview
The SSO Server implements a privacy-focused OpenID Connect (OIDC) server that generates unique pseudonyms for each user-vendor pair. This ensures vendors never have access to real user identifiers or data, enhancing privacy and security.

## Core Components

### 1. Models
- **Vendor Model**
  - Fields: name, client_id (UUID)
  - Purpose: Stores vendor information and OIDC client credentials

- **Pseudonym Model**
  - Purpose: Maps users to vendor-specific pseudonyms
  - Ensures consistent pseudonym generation per user-vendor pair

### 2. Key Functions
- **userinfo Endpoint** (views.py)
  - Returns pseudonymized user data
  - Handles claims and user parameters
  - Ensures vendors only see pseudonymized information

- **CustomScopeClaims Class** (utils.py)
  - Manages OIDC scope claims
  - Handles vendor and pseudonym creation based on client ID
  - Integrates with token generation

### 3. Admin Interface
- Custom admin interfaces for Profile, Vendor, and Pseudonym models
- Enhanced search and display fields
- Streamlined vendor management

### 4. Authentication Flow
- User logs in with real credentials
- System generates/retrieves vendor-specific pseudonym
- OIDC responses contain only pseudonymized data

## Implementation Status

### Completed Features
1. Core pseudonym generation system
2. Database schema for user-vendor-pseudonym mappings
3. OIDC endpoint modifications
4. Admin interfaces
5. Basic test suite
6. Database migrations

### Pending Features
1. Management command for existing user pseudonym generation
2. Frontend template updates
3. Logging system
4. Documentation updates
5. Security audit
6. Integration with other features

## Epic: Privacy-Focused OIDC Server

### User Stories Status

#### 1. OIDC Protocol Implementation ✓
- [x] Authorization endpoint
- [x] Token endpoint
- [x] Userinfo endpoint
- [x] Standard OIDC scopes
- [x] Discovery endpoint

#### 2. Pseudonym Generation ✓
- [x] Unique pseudonym generation algorithm
- [x] Database schema for mappings
- [x] Consistent pseudonym retrieval

#### 3. Fake Profile Generation (Pending)
- [ ] Fake data generation algorithms
- [ ] Consistent data per pseudonym
- [ ] Data storage and retrieval

#### 4. Encryption Implementation (Pending)
- [ ] Encryption algorithm selection
- [ ] User data encryption
- [ ] Key management system
- [ ] Secure decryption process

#### 5. Authentication Flow (Partial)
- [x] User login system
- [x] Pseudonym selection/generation
- [x] OIDC response pseudonymization
- [ ] Additional flow improvements

#### 6. Vendor Integration API (Partial)
- [x] Basic vendor management
- [ ] API endpoints for registration
- [ ] Client credentials management
- [ ] Integration documentation

#### 7. Compliance Management (Pending)
- [ ] Compliance rule engine
- [ ] Vendor-specific requirements storage
- [ ] Rule application in auth flows

#### 8. Logging and Monitoring (Pending)
- [ ] Comprehensive logging
- [ ] Health/performance monitoring
- [ ] Security alerts

#### 9. Testing and Security (Partial)
- [x] Unit tests for pseudonym system
- [x] Integration tests for auth flows
- [ ] Complete security audit
- [ ] Penetration testing

## Technical Details

### Database Changes
- New migrations for Vendor and Pseudonym models
- Updated relationships with existing User model
- Optimized queries for pseudonym lookup

### Code Organization
- views.py: OIDC endpoint implementations
- models.py: Data models and relationships
- utils.py: OIDC and pseudonym utilities
- admin.py: Administrative interfaces
- tests.py: Comprehensive test suite

### Testing
- Unit tests for models and utilities
- Integration tests for OIDC flows
- Test coverage for pseudonym generation
- Authentication flow testing

## Security Considerations

### Current Implementation
- Unique pseudonyms per user-vendor pair
- No exposure of real user data
- Secure OIDC implementation

### Pending Security Enhancements
1. Encryption for stored user data
2. Audit logging
3. Security monitoring
4. Penetration testing
5. Compliance verification

## Future Development

### Immediate Tasks
1. Generate pseudonyms for existing users
2. Update frontend templates
3. Implement logging system
4. Complete documentation
5. Security audit
6. Integration with remaining features

### Long-term Goals
1. Enhanced compliance management
2. Advanced monitoring
3. Automated security checks
4. Extended vendor API features
5. Improved fake data generation

## Documentation
- Implementation plan in docs/pseudonym_implementation_plan.md
- Epic and user stories in docs/epic_and_user_stories.md
- Additional documentation pending

## Contributing
When contributing to the pseudonym system:
1. Ensure all tests pass
2. Maintain privacy focus
3. Follow existing patterns for pseudonym handling
4. Update documentation
5. Consider security implications

## Related Pull Requests
- PR #2: Initial pseudonym system implementation
  - Added core models and functionality
  - Updated OIDC endpoints
  - Implemented basic testing
  - Created admin interfaces