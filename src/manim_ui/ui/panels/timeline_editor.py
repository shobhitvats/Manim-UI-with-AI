"""
Timeline Editor Panel
=====================

Timeline-based animation editor for Manim scenes.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QSplitter, QListWidget, QListWidgetItem,
    QSlider, QSpinBox, QDoubleSpinBox, QComboBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont

class TimelineTrack(QWidget):
    """A single track in the timeline representing an object or layer."""
    
    def __init__(self, track_name, duration=10.0):
        super().__init__()
        
        self.track_name = track_name
        self.duration = duration
        self.keyframes = []  # List of (time, animation_type, properties)
        
        self.setMinimumHeight(40)
        self.setMaximumHeight(40)
        
        # Track properties
        self.track_color = QColor(100, 150, 200)
        self.selected = False
    
    def add_keyframe(self, time, animation_type, properties=None):
        """Add a keyframe to this track."""
        if properties is None:
            properties = {}
        
        self.keyframes.append((time, animation_type, properties))
        self.keyframes.sort(key=lambda x: x[0])  # Sort by time
        self.update()
    
    def remove_keyframe(self, index):
        """Remove a keyframe by index."""
        if 0 <= index < len(self.keyframes):
            del self.keyframes[index]
            self.update()
    
    def paintEvent(self, event):
        """Paint the timeline track."""
        painter = QPainter(self)
        
        # Background
        bg_color = QColor(60, 60, 60) if not self.selected else QColor(80, 80, 120)
        painter.fillRect(self.rect(), bg_color)
        
        # Track name area
        name_width = 150
        painter.fillRect(0, 0, name_width, self.height(), QColor(50, 50, 50))
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont("Arial", 10))
        painter.drawText(5, 5, name_width - 10, self.height() - 10, 
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, 
                        self.track_name)
        
        # Timeline area
        timeline_x = name_width
        timeline_width = self.width() - name_width
        
        if timeline_width > 0:
            # Draw time grid
            pixels_per_second = timeline_width / self.duration
            
            painter.setPen(QPen(QColor(80, 80, 80)))
            for i in range(int(self.duration) + 1):
                x = timeline_x + i * pixels_per_second
                painter.drawLine(x, 0, x, self.height())
            
            # Draw keyframes
            for time, animation_type, properties in self.keyframes:
                x = timeline_x + time * pixels_per_second
                
                # Keyframe marker
                painter.setPen(QPen(QColor(255, 255, 255), 2))
                painter.setBrush(QBrush(self.track_color))
                painter.drawEllipse(x - 5, self.height() // 2 - 5, 10, 10)
                
                # Animation type label
                painter.setPen(QPen(QColor(255, 255, 255)))
                painter.setFont(QFont("Arial", 8))
                painter.drawText(x + 8, self.height() // 2 + 3, animation_type)
    
    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.selected = not self.selected
            self.update()
            
            # TODO: Emit selection signal
    
    def get_time_from_x(self, x):
        """Convert x coordinate to time."""
        name_width = 150
        timeline_x = name_width
        timeline_width = self.width() - name_width
        
        if x < timeline_x:
            return 0
        
        relative_x = x - timeline_x
        return (relative_x / timeline_width) * self.duration if timeline_width > 0 else 0

class TimelineWidget(QWidget):
    """Main timeline widget containing multiple tracks."""
    
    time_changed = pyqtSignal(float)  # Emitted when playhead position changes
    keyframe_added = pyqtSignal(str, float, str)  # track_name, time, animation_type
    
    def __init__(self):
        super().__init__()
        
        self.duration = 10.0  # Total timeline duration in seconds
        self.current_time = 0.0  # Current playhead position
        self.tracks = []  # List of TimelineTrack objects
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area for tracks
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Container for tracks
        self.tracks_container = QWidget()
        self.tracks_layout = QVBoxLayout(self.tracks_container)
        self.tracks_layout.setContentsMargins(0, 0, 0, 0)
        self.tracks_layout.setSpacing(1)
        
        self.scroll_area.setWidget(self.tracks_container)
        layout.addWidget(self.scroll_area)
        
        # Add default track
        self.add_track("Scene")
    
    def add_track(self, track_name):
        """Add a new track to the timeline."""
        track = TimelineTrack(track_name, self.duration)
        self.tracks.append(track)
        self.tracks_layout.addWidget(track)
        return track
    
    def remove_track(self, track_name):
        """Remove a track from the timeline."""
        for i, track in enumerate(self.tracks):
            if track.track_name == track_name:
                self.tracks_layout.removeWidget(track)
                track.deleteLater()
                del self.tracks[i]
                break
    
    def add_keyframe(self, track_name, time, animation_type, properties=None):
        """Add a keyframe to a specific track."""
        for track in self.tracks:
            if track.track_name == track_name:
                track.add_keyframe(time, animation_type, properties)
                self.keyframe_added.emit(track_name, time, animation_type)
                break
    
    def set_current_time(self, time):
        """Set the current playhead position."""
        self.current_time = max(0, min(time, self.duration))
        self.time_changed.emit(self.current_time)
        self.update()
    
    def paintEvent(self, event):
        """Paint the playhead."""
        super().paintEvent(event)
        
        if self.tracks:
            painter = QPainter(self)
            
            # Calculate playhead position
            name_width = 150
            timeline_width = self.width() - name_width
            pixels_per_second = timeline_width / self.duration if self.duration > 0 else 0
            playhead_x = name_width + self.current_time * pixels_per_second
            
            # Draw playhead line
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawLine(playhead_x, 0, playhead_x, self.height())

class TimelineEditorPanel(QWidget):
    """Complete timeline editor panel with controls and timeline."""
    
    def __init__(self):
        super().__init__()
        
        self.is_playing = False
        self.playback_timer = QTimer()
        self.playback_timer.timeout.connect(self._update_playback)
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout(self)
        
        # Header with controls
        header_layout = QHBoxLayout()
        
        # Title
        title_label = QLabel("Timeline Editor")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Playback controls
        self.play_btn = QPushButton("Play")
        self.stop_btn = QPushButton("Stop")
        self.prev_frame_btn = QPushButton("<<")
        self.next_frame_btn = QPushButton(">>")
        
        header_layout.addWidget(self.prev_frame_btn)
        header_layout.addWidget(self.play_btn)
        header_layout.addWidget(self.stop_btn)
        header_layout.addWidget(self.next_frame_btn)
        
        # Time display
        self.time_label = QLabel("00:00.00")
        self.time_label.setStyleSheet("font-family: monospace; font-size: 12px;")
        header_layout.addWidget(self.time_label)
        
        # Duration setting
        header_layout.addWidget(QLabel("Duration:"))
        self.duration_spinbox = QDoubleSpinBox()
        self.duration_spinbox.setRange(1.0, 300.0)
        self.duration_spinbox.setValue(10.0)
        self.duration_spinbox.setSuffix(" sec")
        header_layout.addWidget(self.duration_spinbox)
        
        layout.addLayout(header_layout)
        
        # Separator
        separator = QFrame()
        separator.setFrameStyle(QFrame.Shape.HLine | QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Timeline and animation controls splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Timeline widget
        self.timeline = TimelineWidget()
        splitter.addWidget(self.timeline)
        
        # Animation controls panel
        animation_panel = self._create_animation_panel()
        splitter.addWidget(animation_panel)
        
        # Set splitter proportions
        splitter.setStretchFactor(0, 3)  # Timeline gets more space
        splitter.setStretchFactor(1, 1)  # Animation panel gets less space
        
        layout.addWidget(splitter)
    
    def _create_animation_panel(self):
        """Create the animation controls panel."""
        panel = QWidget()
        panel.setMinimumWidth(200)
        panel.setMaximumWidth(300)
        
        layout = QVBoxLayout(panel)
        
        # Animation type selection
        layout.addWidget(QLabel("Add Animation:"))
        
        self.animation_combo = QComboBox()
        animations = [
            "FadeIn", "FadeOut", "Write", "Unwrite",
            "DrawBorderThenFill", "ShowIncreasingSubsets",
            "MoveTo", "Shift", "Rotate", "Scale",
            "Transform", "ReplacementTransform",
            "Wiggle", "Flash", "Indicate"
        ]
        self.animation_combo.addItems(animations)
        layout.addWidget(self.animation_combo)
        
        # Duration setting for animations
        layout.addWidget(QLabel("Duration:"))
        self.anim_duration_spinbox = QDoubleSpinBox()
        self.anim_duration_spinbox.setRange(0.1, 10.0)
        self.anim_duration_spinbox.setValue(1.0)
        self.anim_duration_spinbox.setSuffix(" sec")
        layout.addWidget(self.anim_duration_spinbox)
        
        # Add animation button
        self.add_animation_btn = QPushButton("Add to Timeline")
        layout.addWidget(self.add_animation_btn)
        
        layout.addStretch()
        
        # Track management
        layout.addWidget(QLabel("Tracks:"))
        
        self.add_track_btn = QPushButton("Add Track")
        layout.addWidget(self.add_track_btn)
        
        self.remove_track_btn = QPushButton("Remove Track")
        layout.addWidget(self.remove_track_btn)
        
        layout.addStretch()
        
        return panel
    
    def _connect_signals(self):
        """Connect signals between components."""
        # Playback controls
        self.play_btn.clicked.connect(self._toggle_playback)
        self.stop_btn.clicked.connect(self._stop_playback)
        self.prev_frame_btn.clicked.connect(self._previous_frame)
        self.next_frame_btn.clicked.connect(self._next_frame)
        
        # Timeline
        self.timeline.time_changed.connect(self._on_time_changed)
        self.duration_spinbox.valueChanged.connect(self._on_duration_changed)
        
        # Animation controls
        self.add_animation_btn.clicked.connect(self._add_animation)
        self.add_track_btn.clicked.connect(self._add_track)
        self.remove_track_btn.clicked.connect(self._remove_track)
    
    def _toggle_playback(self):
        """Toggle playback state."""
        if self.is_playing:
            self._pause_playback()
        else:
            self._start_playback()
    
    def _start_playback(self):
        """Start playback."""
        self.is_playing = True
        self.play_btn.setText("Pause")
        self.playback_timer.start(33)  # ~30 FPS update rate
    
    def _pause_playback(self):
        """Pause playback."""
        self.is_playing = False
        self.play_btn.setText("Play")
        self.playback_timer.stop()
    
    def _stop_playback(self):
        """Stop playback and reset to beginning."""
        self._pause_playback()
        self.timeline.set_current_time(0.0)
    
    def _update_playback(self):
        """Update playback position."""
        if self.is_playing:
            new_time = self.timeline.current_time + 0.033  # Add ~33ms
            if new_time >= self.timeline.duration:
                self._stop_playback()
            else:
                self.timeline.set_current_time(new_time)
    
    def _previous_frame(self):
        """Move to previous frame."""
        new_time = max(0, self.timeline.current_time - 0.033)
        self.timeline.set_current_time(new_time)
    
    def _next_frame(self):
        """Move to next frame."""
        new_time = min(self.timeline.duration, self.timeline.current_time + 0.033)
        self.timeline.set_current_time(new_time)
    
    def _on_time_changed(self, time):
        """Handle time changes from the timeline."""
        # Update time display
        minutes = int(time // 60)
        seconds = time % 60
        self.time_label.setText(f"{minutes:02d}:{seconds:05.2f}")
    
    def _on_duration_changed(self, duration):
        """Handle duration changes."""
        self.timeline.duration = duration
        for track in self.timeline.tracks:
            track.duration = duration
            track.update()
    
    def _add_animation(self):
        """Add an animation to the current track."""
        if self.timeline.tracks:
            # Use the first track for now (TODO: support track selection)
            track_name = self.timeline.tracks[0].track_name
            animation_type = self.animation_combo.currentText()
            time = self.timeline.current_time
            
            self.timeline.add_keyframe(track_name, time, animation_type)
    
    def _add_track(self):
        """Add a new track to the timeline."""
        track_count = len(self.timeline.tracks)
        track_name = f"Track {track_count + 1}"
        self.timeline.add_track(track_name)
    
    def _remove_track(self):
        """Remove the last track from the timeline."""
        if len(self.timeline.tracks) > 1:  # Keep at least one track
            last_track = self.timeline.tracks[-1]
            self.timeline.remove_track(last_track.track_name)