# Audio Generation Technical Specification

## 1. Core Components

### 1.1 Implementation Stages

#### Proof of Concept
- Basic sine wave generation
- Simple frequency validation
- Standard audio format (16-bit, 44.1kHz)
- Core safety checks

#### Production Evolution
- Advanced waveform generation
- Sophisticated frequency analysis
- High-quality audio (24-bit, up to 96kHz)
- Comprehensive safety systems

### 1.2 Frequency Generation Engine

#### POC Implementation
```python
class BasicFrequencyGenerator:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.safety_validator = BasicFrequencyValidator()
    
    def generate_sine_wave(self, frequency, duration, amplitude=0.8):
        """
        Generate a pure sine wave.
        
        Parameters:
        - frequency: Hz (0.5-100 Hz for brainwave entrainment)
        - duration: seconds
        - amplitude: 0.0-1.0
        
        Returns:
        - numpy array of samples
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        return amplitude * np.sin(2 * np.pi * frequency * t)
```

#### POC Binaural Beat Generation
```python
class BasicBinauralGenerator:
    def generate_binaural(self, carrier_freq, target_freq, duration):
        """
        Basic binaural beat generation.
        
        Simplified for POC:
        - Fixed carrier frequency (200Hz)
        - Basic safety validation
        - Simple stereo output
        """
        if not self.validate_frequency(target_freq):
            raise ValueError("Unsafe frequency")
            
        left = self.generate_sine(200, duration)
        right = self.generate_sine(200 + target_freq, duration)
        
        return left, right

    def validate_frequency(self, freq):
        """Basic frequency validation"""
        return 0.5 <= freq <= 40  # Safe range for POC
```

#### Migration to Production
```python
class AdvancedBinauralGenerator:
    """Future implementation with:
    - Dynamic carrier frequency
    - Advanced safety checks
    - Phase alignment
    - Harmonic enhancement
    """
    pass
```

### 1.3 POC Isochronic Generation
```python
class BasicIsochronicGenerator:
    def generate_isochronic(self, frequency, duration):
        """
        Basic isochronic tone generation.
        
        Simplified for POC:
        - Fixed carrier (300Hz)
        - Fixed duty cycle (50%)
        - Basic modulation
        """
        carrier = self.generate_sine(300, duration)
        modulator = self.generate_square(frequency, duration)
        return carrier * modulator
```

#### Migration to Production
- Add variable duty cycle
- Implement smooth envelope control
- Add harmonic enrichment
- Enhance modulation patterns
```

## 2. Frequency Management

### 2.1 POC Transition Control
```python
class BasicTransitionController:
    def __init__(self):
        self.max_rate = 1.0  # Hz per second for POC
    
    def calculate_steps(self, start_freq, end_freq, duration):
        """
        Simple linear transition calculation.
        
        POC Limitations:
        - Linear transitions only
        - Fixed rate limit
        - Basic safety checks
        """
        if abs(end_freq - start_freq) / duration > self.max_rate:
            raise ValueError("Transition too fast")
            
        steps = np.linspace(start_freq, end_freq, 10)
        return steps
```

### Migration to Production
- Implement variable transition rates
- Add non-linear transitions
- Enhanced safety validation
- Optimized step calculation
```

### 2.2 Harmonic System
```python
class HarmonicOvertoneGenerator:
    """Generate harmonic overtones for neural entrainment."""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.calculator = HarmonicCalculator()
        self.safety_limits = {
            'max_frequency': 1000.0,  # Maximum safe frequency for overtones
            'max_harmonics': 5,       # Maximum number of harmonics to generate
            'min_amplitude': 0.1,     # Minimum amplitude for overtones
            'amplitude_decay': 0.7    # Decay factor for each successive harmonic
        }
        
    def generate_overtones(self, fundamental: float, duration: float,
                          base_amplitude: float = 0.5) -> np.ndarray:
        """
        Generate harmonic overtones for a fundamental frequency.
        
        Args:
            fundamental: Fundamental frequency in Hz
            duration: Duration in seconds
            base_amplitude: Base amplitude for fundamental (0-1)
            
        Returns:
            numpy.ndarray: Combined audio with harmonics
        """
        # Validate fundamental frequency
        if fundamental <= 0:
            raise ValueError("Fundamental frequency must be positive")
        if fundamental > self.safety_limits['max_frequency']:
            raise ValueError(f"Frequency {fundamental} Hz exceeds safety limit")
            
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        combined = np.zeros_like(t)
        amplitude = base_amplitude
        
        # Generate fundamental and harmonics
        for n in range(1, self.safety_limits['max_harmonics'] + 1):
            harmonic_freq = fundamental * n
            if harmonic_freq > self.safety_limits['max_frequency']:
                break
                
            combined += amplitude * np.sin(2 * np.pi * harmonic_freq * t)
            amplitude *= self.safety_limits['amplitude_decay']
            
        # Normalize to prevent clipping
        max_amplitude = np.max(np.abs(combined))
        if max_amplitude > 1:
            combined /= max_amplitude
            
        return combined
```

### Features
- Multiple harmonic generation with configurable limits
- Dynamic amplitude control with natural decay
- Comprehensive safety validation
- Automatic normalization

## 3. Audio Processing Pipeline

### 3.1 Processing Chain
```python
class AudioProcessor:
    def __init__(self):
        self.processors = [
            VolumeNormalizer(),
            FrequencyAnalyzer(),
            SafetyValidator(),
            Equalizer()
        ]
    
    def process(self, audio_data):
        """
        Run audio through processing chain.
        """
        for processor in self.processors:
            audio_data = processor.process(audio_data)
        return audio_data
```

### 3.2 Background Sound Integration
```python
class BackgroundSoundMixer:
    """Mix background sounds with neural entrainment audio."""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.equalizer = Equalizer(sample_rate=sample_rate)
        
    def generate_white_noise(self, duration: float,
                           volume: float = 0.1) -> np.ndarray:
        """Generate pink-filtered white noise."""
        samples = int(self.sample_rate * duration)
        noise = np.random.normal(0, 1, samples)
        
        # Shape noise with pink filter (more natural sounding)
        fft = np.fft.rfft(noise)
        freqs = np.fft.rfftfreq(len(noise))
        pink_filter = 1 / np.sqrt(freqs[1:])
        fft[1:] *= pink_filter
        noise = np.fft.irfft(fft)
        
        return noise / np.max(np.abs(noise)) * volume
        
    def generate_ambient_drone(self, duration: float,
                             base_freq: float = 100.0,
                             volume: float = 0.1) -> np.ndarray:
        """Generate rich ambient drone with harmonics."""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        
        harmonics = [1.0, 1.5, 2.0, 2.5, 3.0]
        amplitudes = [1.0, 0.5, 0.3, 0.2, 0.1]
        
        drone = np.zeros_like(t)
        for harmonic, amplitude in zip(harmonics, amplitudes):
            freq = base_freq * harmonic
            drone += amplitude * np.sin(2 * np.pi * freq * t)
            
        # Add subtle modulation
        mod_freq = 0.1
        modulation = 1 + 0.1 * np.sin(2 * np.pi * mod_freq * t)
        drone *= modulation
        
        return drone / np.max(np.abs(drone)) * volume
        
    def mix_background(self, main_audio: Union[np.ndarray, tuple],
                      background_type: str = 'white_noise',
                      volume: float = 0.1,
                      eq_gains: Optional[dict] = None) -> Union[np.ndarray, tuple]:
        """
        Mix background sounds with main entrainment audio.
        
        Args:
            main_audio: Primary audio (mono array or stereo tuple)
            background_type: Type of background ('white_noise', 'ambient')
            volume: Background volume level (0-1)
            eq_gains: Optional EQ gains (e.g., {'low': -3, 'mid': 0, 'high': 2})
        """
        is_stereo = isinstance(main_audio, tuple)
        duration = len(main_audio[0] if is_stereo else main_audio) / self.sample_rate
        
        # Generate and process background
        background = (self.generate_white_noise(duration, volume)
                     if background_type == 'white_noise'
                     else self.generate_ambient_drone(duration, volume=volume))
                     
        if eq_gains:
            background = self.equalizer.process(background, eq_gains)
            
        # Mix and normalize
        if is_stereo:
            mixed = tuple(ch + background for ch in main_audio)
            return tuple(ch / max(1, np.max(np.abs(ch))) for ch in mixed)
        else:
            mixed = main_audio + background
            return mixed / max(1, np.max(np.abs(mixed)))
```

### Features
- Multiple background types (white noise, ambient drones)
- Three-band equalizer integration
- Stereo and mono support
- Automatic normalization
- Volume control

## 4. Safety Systems

### 4.1 Frequency Validation
```python
class FrequencyValidator:
    def __init__(self):
        self.safe_ranges = {
            'delta': (0.5, 4),
            'theta': (4, 8),
            'alpha': (8, 14),
            'beta': (14, 30),
            'gamma': (30, 100)
        }
        
    def validate_frequency(self, frequency):
        """
        Validate frequency safety.
        """
        for range_min, range_max in self.safe_ranges.values():
            if range_min <= frequency <= range_max:
                return True
        return False
```

### 4.2 Volume Safety
```python
class VolumeSafetySystem:
    def __init__(self, max_db=85):
        self.max_db = max_db
        
    def check_volume_levels(self, audio_data):
        """
        Ensure audio stays within safe volume range.
        """
        peak_db = 20 * np.log10(np.max(np.abs(audio_data)))
        if peak_db > self.max_db:
            raise VolumeSafetyError(f"Audio exceeds safety threshold")
```

## 5. Output Formats

### 5.1 File Format Specifications
- Sample Rate: 44100 Hz
- Bit Depth: 24-bit
- Channels: Stereo
- Primary Format: WAV (lossless)
- Distribution Format: MP3 (320kbps)

### 5.2 Metadata Requirements
```python
class AudioMetadata:
    required_fields = {
        'base_frequency': float,
        'target_frequency': float,
        'duration': int,
        'generation_date': datetime,
        'safety_validated': bool,
        'target_state': str,
        'transition_points': list
    }
```

## 6. Implementation Guidelines

### 6.1 Performance Considerations
- Use NumPy for all frequency calculations
- Implement parallel processing for long sessions
- Cache frequently used frequency combinations
- Monitor CPU usage during generation

### 6.2 Error Handling
```python
class AudioGenerationError(Exception):
    pass

class FrequencyError(AudioGenerationError):
    pass

class TransitionError(AudioGenerationError):
    pass

class VolumeSafetyError(AudioGenerationError):
    pass
```

### 6.3 Quality Assurance
- Frequency accuracy within 0.1 Hz
- Phase alignment error < 0.1%
- Harmonic distortion < 0.01%
- Signal-to-noise ratio > 90 dB

## 7. Usage Examples

### 7.1 Basic Usage
```python
# Initialize components
generator = AudioGenerator()
mixer = BackgroundSoundMixer(sample_rate=44100)

# Generate 5-minute alpha state session with harmonics
left, right = generator.generate_binaural_beat(
    target_frequency=10,  # Alpha state
    duration=300,
    volume=0.7
)

# Add background sounds with EQ
background_eq = {
    'low': -3,    # Reduce low frequencies
    'mid': 0,     # Keep mids neutral
    'high': 2     # Slightly boost highs
}

final_audio = mixer.mix_background(
    main_audio=(left, right),
    background_type='white_noise',  # or 'ambient'
    volume=0.1,
    eq_gains=background_eq
)
```

### 7.2 Advanced Usage
```python
# Generate complex session with transitions and harmonics
generator = AudioGenerator()

# Generate a session transitioning from theta to alpha
audio_file = generator.generate(
    frequency=4,      # Start at theta
    duration=600,     # 10 minutes
    volume=0.7,
    transition_type='sigmoid'  # Smooth transition
)

# The generator automatically:
# - Adds harmonic overtones for richer sound
# - Handles frequency transitions smoothly
# - Combines binaural beats and isochronic tones
# - Applies proper fades and normalization

# Add ambient background with EQ
mixer = BackgroundSoundMixer(sample_rate=44100)
final_audio = mixer.mix_background(
    main_audio=audio_file,
    background_type='ambient',
    volume=0.15,
    eq_gains={
        'low': 0,     # Keep bass
        'mid': -6,    # Reduce mids
        'high': -12   # Significantly reduce highs
    }
)
```
