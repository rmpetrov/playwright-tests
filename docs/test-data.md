# Local App Test Data

## Default Dashboard Scenario
- Route: `/app.html`
- Behavior: authenticated users see the populated dashboard with overview cards and three transaction rows.
- Coverage focus: row formatting, required values, header consistency, and logout/session behavior.

## Empty Dashboard Scenario
- Route: `/app.html?scenario=empty`
- Behavior: authenticated users still reach the dashboard, but the transactions table body has zero rows.
- UI signal: `No recent transactions to display.`
- Coverage focus: successful page load, visible empty state, and absence of phantom transaction rows.

## Auth and Session Expectations
- `/app.html` is protected and redirects unauthenticated users to `/`.
- Successful login sets the auth cookie and redirects to `/app.html`.
- `Remember Me` adds a durable cookie.
- Login without `Remember Me` remains session-only and does not persist across browser restart.
- `POST /logout` clears the auth cookie and returns the user to `/`.

## Local API Validation Scenario
- Endpoint: `POST /api/feedback`
- Required JSON fields: `subject`, `message`
- Success response: `201 Created` with JSON body and `application/json` content type.
- Deterministic error cases:
  - missing required fields
  - empty string values
  - invalid field types
  - malformed JSON
  - unsupported content type
- Error response shape: `{"error": {"code": ..., "message": ..., "details": [...]}}`
