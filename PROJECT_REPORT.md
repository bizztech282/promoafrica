# Project Report: Skiza Spin & Win

## 1. Executive Summary
The "Skiza Spin & Win" project is a Django-based web application designed to run a promotional campaign where users spin a virtual wheel to win prizes (currently hardcoded to Kshs 800) and are then guided to subscribe to a Skiza service via USSD to claim their winnings. The application is designed for the Kenyan market, integrating local phone number formats and USSD codes.

## 2. Technical Stack
- **Backend Framework**: Django 4.2+
- **Database**: SQLite (Development) / PostgreSQL-ready (Production via `dj_database_url`)
- **Frontend**: HTML5, JavaScript (Vanilla), Tailwind CSS
- **Deployment**: Configured for Render (Procfile, render.yaml, build.sh)

## 3. Codebase Analysis

### 3.1 Project Structure
- **`skiza_project/`**: Core project configuration including settings, URL routing, and WSGI application.
- **`wheel_spin/`**: The main application handling all logic.
  - **`views.py`**: Contains the business logic for the spin, withdrawal, and subscription flow.
  - **`models.py`**: Defines the `WithdrawalRequest` model (currently bypassed in logic).
  - **`urls.py`**: Application-specific routing.
  - **`templates/wheel_spin/`**: HTML templates including `landing.html` which contains the core UI/UX.

### 3.2 Key Features & Implementation
- **Spin Wheel**: Implemented using HTML5 `<canvas>` and JavaScript in `landing.html`. It is visually rich with animations and sound effects (implied by logic, though assets not verified).
- **Session Management**: Uses `django.contrib.sessions.backends.signed_cookies` to manage user state without requiring a database, facilitating a smoother high-traffic flow.
- **AJAX Flow**: The application relies heavily on `fetch` API calls to endpoints like `/api/spin/` and `/api/submit-withdrawal/` to avoid page reloads and maintain a seamless user experience.
- **Modal System**: A dynamic modal in `landing.html` guides the user through the Win -> Phone Entry -> USSD Instructions flow without page navigation.

### 3.3 Current Logic Flow
1.  **Landing**: User visits page, checks session for previous spins.
2.  **Spin**: JS calls `/api/spin/`. Server always returns 800. Session updated (`has_spun=True`).
3.  **Withdrawal**: User enters phone number in modal. JS calls `/api/submit-withdrawal/`.
4.  **Processing**: Server validates phone number but **does not save to database**. It returns a success response with USSD code.
5.  **Subscription**: Modal updates to show USSD code `*860*860#` and "Dial" button.

### 4. Key Findings & Issues

#### 4.1 'Dummy ID' Logic Mismatch
- **Issue**: In `views.py`, `submit_withdrawal` sets `request.session['withdrawal_id'] = 'dummy_id'`. However, `processing_confirmation` view attempts to do `WithdrawalRequest.objects.get(id=withdrawal_id)`.
- **Impact**: If a user were to navigate to `/confirmation/`, the view would fail to look up 'dummy_id' as a primary key or simply fail to find the object. It is caught by `DoesNotExist`, but the logic is inconsistent.
- **Status**: Non-critical as long as the tailored AJAX flow in `landing.html` keeps the user on the page, but represents technical debt.

#### 4.2 Disabled Persistence
- **Observation**: `submit_withdrawal` explicitly has database saving commented out: `# withdrawal = WithdrawalRequest.objects.create(...)`.
- **Implication**: No record of user spins or phone numbers is being kept in the database. This means no analytics or verification of who actually spun/won.

#### 4.3 Hardcoded Winning
- **Observation**: Winning amount is hardcoded to 800 in `views.py`.
- **Note**: This is likely by design for the campaign but should be noted for future maintainability.

## 5. Recommendations
1.  **Clean Up Legacy Views**: If `processing_confirmation` is no longer needed due to the modal flow, it should be removed or updated to handle the "no-database" state gracefully.
2.  **Re-enable Optional Logging**: Even if the core flow doesn't require a DB transaction to succeed (for speed/reliability), logging the attempt (phone number + timestamp) to the database asynchronously or safely would be valuable for analytics.
3.  **Security**: Ensure the USSD code and critical logic are not easily tampered with, though the low stakes (everyone wins 800) mitigates some risk.
