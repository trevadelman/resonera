# Changelog

All notable changes to the Resonera project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2025-01-28
### Added
- Harmonic overtone generator in `src/resonera/audio/harmonics.py`:
  - Multiple harmonic generation with configurable limits
  - Amplitude decay control for natural sound
  - Safety limits for maximum frequencies
  - Integration with existing audio generation
- Background sound mixer with EQ in `src/resonera/audio/mixer.py`:
  - Three-band equalizer (low, mid, high)
  - White noise generation with pink filtering
  - Ambient drone generation with harmonics
  - Support for both mono and stereo mixing
  - Volume control and normalization

### Technical
- Added FFT-based frequency band filtering
- Implemented proper signal normalization
- Added comprehensive test suites for both components
- Enhanced audio quality with rich harmonic content

## [0.1.4] - 2025-01-28
### Added
- Email notification system in `src/resonera/core/email.py`:
  - MIME-based email functionality with HTML and plain text support
  - Configurable email templates in `src/resonera/core/templates/email/`
  - Welcome email template with safety guidelines and getting started info
- Environment configuration for email system:
  - Added email configuration to `.env`
  - Updated configuration handling in `src/resonera/core/config.py`
  - Documented setup process in main documentation

### Technical
- Implemented EmailSender class with comprehensive error handling
- Added template loading system for email content
- Created test script for email functionality verification
- Updated documentation with email configuration guidelines

## [0.1.3] - 2025-01-28
### Added
- Harmonic relationship calculator in `src/resonera/audio/harmonics.py`:
  - Scientifically validated carrier frequencies for brainwave states:
    - Alpha wave (10 Hz → 200 Hz) for focus and meditation
    - Theta wave (6 Hz → 288 Hz) for deep meditation
    - Delta wave (2 Hz → 256 Hz) for deep sleep
  - Flexible harmonic finding for non-core frequencies
  - Comprehensive test suite in `src/resonera/audio/test_harmonics.py`

### Technical
- Added optimal carrier frequency selection based on harmonic ratios
- Implemented ratio decomposition for harmonic analysis
- Added extensive test coverage for core and edge cases

## [0.1.2] - 2025-01-28
### Added
- Frequency transition system in `src/resonera/audio/transitions.py`:
  - Linear transitions for basic frequency changes
  - Exponential transitions for natural progression
  - Sigmoid transitions for smooth acceleration/deceleration
  - Optimal duration calculation based on frequency difference
- Enhanced audio generation in `src/resonera/audio/generator.py`:
  - Integrated frequency transitions for smooth state changes
  - Optimized carrier frequencies for each brainwave range
  - Support for transition type selection (linear/exponential/sigmoid)

### Technical
- Added comprehensive test suites for transitions and enhanced generator
- Improved audio quality with smooth frequency changes
- Added optimal carrier frequency selection for better perception

## [0.1.1] - 2025-01-28
### Added
- Support for all brainwave frequency ranges in `src/resonera/audio/generator.py`:
  - Delta waves (0.5-4 Hz) for deep sleep
  - Theta waves (4-8 Hz) for meditation
  - Gamma waves (30-100 Hz) for high cognition
- Optimal carrier frequency selection for different ranges
- Comprehensive unit testing suite:
  - Audio generation tests in `src/resonera/audio/test_generator.py`
  - Safety validation tests in `src/resonera/safety/test_validator.py`

### Technical
- Improved audio generation with frequency-optimized carrier waves
- Added proper Flask app context handling in tests
- Fixed test suite implementation using Python's built-in unittest

## [0.1.0] - 2025-01-28

### Added
- Core Flask application structure with modular design
  - `src/resonera/__init__.py`: Main application factory
  - `src/run.py`: Application entry point
  - `requirements.txt`: Project dependencies
  - `.env`: Environment configuration
  - `.gitignore`: Version control exclusions

- User authentication system with JWT tokens
  - `src/resonera/core/routes.py`: Authentication endpoints
  - `src/resonera/core/config.py`: JWT configuration

- Database models and initialization
  - `src/resonera/database/__init__.py`: Models for User, Session, SafetyLog
  - `src/resonera/core/config.py`: Database configuration

- Audio generation engine
  - `src/resonera/audio/generator.py`: Core audio generation logic
  - `src/resonera/audio/routes.py`: Audio generation endpoints
  - Features:
    - Binaural beats generation
    - Isochronic tones generation
    - Frequency range validation (0.5-100 Hz)
    - Volume control and safety limits

- Safety system implementation
  - `src/resonera/safety/validator.py`: Safety validation logic
  - `src/resonera/database/__init__.py`: Safety logging model

- API endpoints implementation
  - `src/resonera/core/routes.py`:
    - User registration (/register)
    - Authentication (/login)
    - Profile management (/profile)
  - `src/resonera/audio/routes.py`:
    - Audio generation (/audio/generate)
    - Session management (/audio/sessions)

### Security
- Password hashing implementation in `src/resonera/core/routes.py`
- JWT authentication in `src/resonera/core/config.py` and `src/resonera/__init__.py`
- Frequency validation in `src/resonera/safety/validator.py`
- Volume limiting in `src/resonera/audio/generator.py`
- User safety preferences in `src/resonera/database/__init__.py`

### Technical
- Project structure:
  - `src/resonera/`: Main package directory
  - `src/resonera/core/`: Core functionality
  - `src/resonera/audio/`: Audio processing
  - `src/resonera/safety/`: Safety features
  - `src/resonera/database/`: Data models

- Framework integrations:
  - Flask web framework (`src/resonera/__init__.py`)
  - SQLAlchemy ORM (`src/resonera/database/__init__.py`)
  - JWT management (`src/resonera/core/config.py`)
  - Audio processing with NumPy/SciPy (`src/resonera/audio/generator.py`)

[0.1.0]: https://github.com/username/resonera/releases/tag/v0.1.0
