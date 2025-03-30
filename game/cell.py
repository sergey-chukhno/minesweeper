import customtkinter as ctk
from game.config import (
    CELL_COVERED, CELL_FLAGGED, CELL_QUESTION, CELL_REVEALED,
    UI_COLORS, TEXT_COLORS, NUMBER_COLORS, EMOJIS
)

class AnimatedCell(ctk.CTkButton):
    """Grid cell with animation capability."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_revealed = False
        self.is_flagged = False
        self.is_question = False
        self.is_mine = False
        self.is_exploded = False
        self.value = 0
        self.animation_step = 0
        self.animation_active = False
        self.animation_id = None
        self.hover_active = False
        
        # Store original colors for animations
        self.original_fg = kwargs.get('fg_color', "#0A0A1A")
        self.original_hover = kwargs.get('hover_color', "#1A1A3A")
        self.original_border = kwargs.get('border_color', "#1A1A4A")
        
        # Bind hover events for neon glow effect
        self.bind("<Enter>", self._on_hover_enter)
        self.bind("<Leave>", self._on_hover_leave)
    
    def _on_hover_enter(self, event):
        """Handle hover enter event for neon glow effect."""
        if not self.is_revealed and not self.animation_active:
            self.hover_active = True
            self.configure(
                border_color="#00F0FF",  
                border_width=2
            )
    
    def _on_hover_leave(self, event):
        """Handle hover leave event for neon glow effect."""
        if self.hover_active and not self.is_revealed:
            self.hover_active = False
            self.configure(
                border_color=self.original_border,
                border_width=1
            )
    
    def start_idle_animation(self, parent):
        """Start subtle pulsing animation when idle."""
        if not self.is_revealed and not self.animation_active:
            self.animation_active = True
            self.animation_step = 0
            self._animate_idle(parent)
    
    def _animate_idle(self, parent):
        """Animate idle cell with subtle pulsing effect."""
        if not self.animation_active or self.is_revealed:
            return
        
        try:
            # Check if the widget still exists
            if not self.winfo_exists():
                self.animation_active = False
                self.animation_id = None
                return
            
            # Pulsing animation with neon color
            self.animation_step = (self.animation_step + 1) % 30
            
            # Calculate pulsing intensity (0-10)
            intensity = abs(15 - self.animation_step) / 15
            
            # Create neon glow effect based on intensity
            r = int(10 + 10 * intensity)  
            g = int(10 + 40 * intensity)  
            b = int(40 + 80 * intensity)  
            
            # Update colors
            pulse_color = f"#{r:02x}{g:02x}{b:02x}"
            self.configure(fg_color=pulse_color)
            
            # Schedule next animation frame
            self.animation_id = parent.after(50, lambda: self._animate_idle(parent))
        except Exception:
            self.animation_active = False
            self.animation_id = None
    
    def stop_animation(self):
        """Stop any running animation."""
        self.animation_active = False
        if self.animation_id:
            try:
                if self.master and self.master.winfo_exists():
                    self.master.after_cancel(self.animation_id)
            except Exception:
                pass  
            self.animation_id = None
        
        try:
            if self.winfo_exists():
                if not self.is_revealed:
                    self.configure(fg_color=self.original_fg)
                elif self.is_exploded:
                    self.configure(fg_color="#FF2020")  
        except Exception:
            pass 
    
    def start_win_animation(self, parent):
        """Start victory animation effect."""
        self.animation_active = True
        self.animation_step = 0
        self._animate_win(parent)
    
    def _animate_win(self, parent):
        """Animate cell for win effect with bright neon colors."""
        if not self.animation_active:
            return
        
        try:
            if not self.winfo_exists():
                self.animation_active = False
                self.animation_id = None
                return
            
            # Victory animation
            self.animation_step = (self.animation_step + 1) % 120
            
            # Map step to hue (0-360)
            phase = self.animation_step / 120 * 360
            
            # Convert HSV-like values to RGB with high saturation and value for neon effect
            if phase < 60:  # Red to Yellow
                r = 255
                g = int(phase * 4.25)
                b = 100
            elif phase < 120:  # Yellow to Green
                r = int(255 - (phase - 60) * 4.25)
                g = 255
                b = 100
            elif phase < 180:  # Green to Cyan
                r = 100
                g = 255
                b = int((phase - 120) * 4.25)
            elif phase < 240:  # Cyan to Blue
                r = 100
                g = int(255 - (phase - 180) * 4.25)
                b = 255
            elif phase < 300:  # Blue to Magenta
                r = int((phase - 240) * 4.25)
                g = 100
                b = 255
            else:  # Magenta to Red
                r = 255
                g = 100
                b = int(255 - (phase - 300) * 4.25)
            
            # Ensure valid RGB values
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            # Apply the color
            color = f"#{r:02x}{g:02x}{b:02x}"
            border_color = f"#FFFFFF"
            
            # Configure cell with neon color
            self.configure(
                fg_color=color,
                border_color=border_color,
                border_width=2
            )
            
            # Schedule next animation frame
            self.animation_id = parent.after(30, lambda: self._animate_win(parent))
        except Exception:
            self.animation_active = False
            self.animation_id = None
    
    def start_lose_animation(self, parent):
        """Start explosion animation effect."""
        self.animation_active = True
        self.animation_step = 0
        self._animate_lose(parent)
    
    def _animate_lose(self, parent):
        """Animate cell for explosion effect with red neon glow."""
        if not self.animation_active:
            return
        
        try:
            if not self.winfo_exists():
                self.animation_active = False
                self.animation_id = None
                return
            
            # Explosion animation with red/orange pulsing
            self.animation_step = (self.animation_step + 1) % 30
            
            # Calculate flash intensity (0.0-1.0)
            intensity = abs(15 - self.animation_step) / 15
            
            # Calculate neon red/orange colors
            r = int(180 + 75 * intensity)  
            g = int(20 + 80 * intensity)   
            b = int(10 + 20 * intensity)   
            
            # Apply the color
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            # For strong flash effect
            if self.animation_step in [0, 1, 15, 16]:
                border_color = "#FFFFFF"  
                border_width = 2
            else:
                border_color = "#FF0000"  
                border_width = 1
            
            # Configure cell with explosion color
            self.configure(
                fg_color=color,
                border_color=border_color,
                border_width=border_width
            )
            
            # Schedule next animation frame
            self.animation_id = parent.after(40, lambda: self._animate_lose(parent))
        except Exception:
            self.animation_active = False
            self.animation_id = None

    def set_mine(self, is_mine=True):
        """Set whether this cell contains a mine."""
        self.is_mine = is_mine
        
    def set_adjacent_mines(self, count):
        """Set the number of adjacent mines."""
        self.adjacent_mines = count
        
    def toggle_mark(self):
        """Toggle between states: covered -> flagged -> question -> covered."""
        # Don't toggle if already revealed
        if self.is_revealed:
            return False
        
        changed = False
        
        # Apply state changes in sequence
        if self.state == CELL_COVERED:
            self.state = CELL_FLAGGED
            self.configure(text=EMOJIS["flag"], text_color=TEXT_COLORS["flag"])
            changed = True
        elif self.state == CELL_FLAGGED:
            self.state = CELL_QUESTION
            self.configure(text="?", text_color=TEXT_COLORS["question"])
            changed = True
        elif self.state == CELL_QUESTION:
            self.state = CELL_COVERED
            self.configure(text="")
            changed = True
            
        return changed
            
    def reveal(self):
        """Reveal the cell content."""
        if self.is_revealed or self.state == CELL_FLAGGED:
            return False
            
        self.is_revealed = True
        self.state = CELL_REVEALED
        
        # Configure appearance based on content
        if self.is_mine:
            self.configure(text=EMOJIS["mine"], fg_color=UI_COLORS["mine_bg"], text_color=TEXT_COLORS["mine"])
            return True
        else:
            self.configure(fg_color=UI_COLORS["cell_revealed"])
            if self.adjacent_mines > 0:
                self.configure(
                    text=str(self.adjacent_mines),
                    text_color=NUMBER_COLORS[self.adjacent_mines]
                )
            return False
            
    def highlight_mine(self, exploded=False):
        """Highlight mine for game over state."""
        if self.is_mine:
            if exploded:
                self.configure(text=EMOJIS["explosion"], fg_color="#FF0000", text_color="#FFFFFF")
            else:
                self.configure(text=EMOJIS["mine"], fg_color=UI_COLORS["mine_bg"], text_color=TEXT_COLORS["mine"])
                
    def highlight_wrong_flag(self):
        """Highlight incorrectly flagged cell."""
        if not self.is_mine and self.state == CELL_FLAGGED:
            self.configure(text=EMOJIS["wrong_flag"], fg_color=UI_COLORS["mine_bg"], text_color=TEXT_COLORS["mine"])
    
    def is_flagged(self):
        """Check if cell is flagged."""
        return self.state == CELL_FLAGGED
        
    def is_question(self):
        """Check if cell has a question mark."""
        return self.state == CELL_QUESTION
        
    def is_covered(self):
        """Check if cell is still covered."""
        return not self.is_revealed
        
    def get_state(self):
        """Get the current state of the cell."""
        return self.state 