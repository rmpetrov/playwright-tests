# Architecture

## Overview
This project is structured around a clear separation of tests, page objects, fixtures, and configuration. UI and API automation live in the same repository but use separate suites and dependencies.

## High-Level Flow
```mermaid
flowchart LR
  subgraph UI
    UT[UI tests] --> FX[pytest fixtures]
    FX --> POM[page objects]
    POM --> PW[Playwright]
    FX --> CFG[config]
  end

  subgraph API
    AT[API tests] --> CL[API clients]
    CL --> SCH[Pydantic schemas]
    CL --> HTTP[requests]
    AT --> MCK[responses mocks]
  end
```

## Folder Map
```text
playwright-tests/
  local_app/        # Deterministic HTTP application
  pages/            # UI page objects
  tests/            # UI test suite
  api_tests/        # API test suite
  config.py         # Environment-based settings
  docs/             # Documentation
  scripts/          # CI helper scripts
```

## Key Components
- `pages/`: Page Object Model classes that encapsulate UI behavior
- `tests/`: UI tests and Playwright fixtures
- `api_tests/clients/`: Typed API client methods
- `api_tests/schemas/`: Pydantic models for request and response validation
- `config.py`: Single source of truth for environment settings

## Execution Model
- UI tests rebuild per-browser auth state once per session and use isolated contexts per test
- Plugin-managed contexts retain failure artifacts; manual persistent contexts have limited diagnostics
- API tests combine mocked user responses and real HTTP feedback checks on an isolated local server
- Lint, API, and the three UI browser jobs run independently; publishing waits for all to pass

## Design Rationale
- POM keeps UI interactions reusable and readable
- Central fixtures reduce duplicated setup and improve stability
- Typed schemas make API contract checks explicit and maintainable
