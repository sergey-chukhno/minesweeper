"""
Sound Manager for Minesweeper.
"""
import os
import pygame
from game.config import SOUNDS_DIR

class SoundManager:
    """
    Manages game sounds and music.
    """
    def __init__(self):
        """Initialize the sound manager."""
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Load sound effects
        self.sounds = {
            'click': self._load_sound('click.wav'),
            'flag': self._load_sound('flag.wav'),
            'explosion': self._load_sound('explosion.wav'),
            'win': self._load_sound('win.wav'),
            'lose': self._load_sound('lose.wav'),
            'hover': self._load_sound('hover.wav')
        }
        
        # Load background music
        self.music = os.path.join(SOUNDS_DIR, 'background.mp3')
        
        # Volume settings
        self.sound_volume = 0.5
        self.music_volume = 0.3
        
        # Set initial volumes
        self.set_sound_volume(self.sound_volume)
        self.set_music_volume(self.music_volume)
    
    def _load_sound(self, filename):
        """Load a sound effect from file."""
        try:
            sound_path = os.path.join(SOUNDS_DIR, filename)
            if os.path.exists(sound_path):
                return pygame.mixer.Sound(sound_path)
            else:
                print(f"Warning: Sound file not found: {filename}")
                return None
        except Exception as e:
            print(f"Error loading sound {filename}: {e}")
            return None
    
    def play_sound(self, sound_name):
        """Play a sound effect."""
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()
    
    def play_music(self):
        """Start playing background music."""
        try:
            if os.path.exists(self.music):
                pygame.mixer.music.load(self.music)
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        except Exception as e:
            print(f"Error playing background music: {e}")
    
    def stop_music(self):
        """Stop background music."""
        pygame.mixer.music.stop()
    
    def set_sound_volume(self, volume):
        """Set volume for sound effects."""
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(self.sound_volume)
    
    def set_music_volume(self, volume):
        """Set volume for background music."""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def cleanup(self):
        """Clean up sound resources."""
        pygame.mixer.quit() 