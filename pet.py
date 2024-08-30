import random
import sys
import tkinter as tk
from PIL import Image, ImageTk
import os
import itertools


class DesktopPet:
    def __init__(self, window):

        # Handle paths for bundled executables
        if hasattr(sys, '_MEIPASS'):
            self.assets_path = os.path.join(sys._MEIPASS, 'assets')
        else:
            self.assets_path = os.path.join(os.path.dirname(__file__), 'assets')

        self.window = window
        self.window.overrideredirect(True)  # Remove window border
        self.window.wm_attributes("-topmost", True)  # Always on top
        self.window.wm_attributes("-transparentcolor", "white")  # Make white color transparent

        self.idle_images = []
        self.dragging_images = []

        # Initialize direction-specific walking images
        self.walking_images = {
            'up': [],
            'down': [],
            'left': [],
            'right': []
        }

        # Adjust size
        self.size = (150, 150)

        # Adjust speed
        self.framerate = 200  # Animation speed
        self.speed = 200  # Movement speed

        # Number of frames
        self.idle_frames_1 = 4
        self.idle_frames_2 = 4
        self.idle_frames_3 = 4
        self.idle_frames_4 = 4
        self.walk_frames = 8
        self.drag_frames = 4

        # State management
        self.is_walking = True  # Controls whether the pet is walking or not
        self.is_dragging = False  # State to track whether the pet is being dragged
        self.last_x = self.window.winfo_x()
        self.last_y = self.window.winfo_y()
        self.current_direction = 'down'  # Default direction
        self.direction_duration = 0  # Time to move in one direction
        self.time_moved_in_direction = 0  # Counter for movement time in current direction

        # Idle animation management
        self.idle_timer = 0  # Time since last activity
        self.idle_duration = self.framerate * 60  # Change idle animation after 60 frames (adjust as needed)
        self.current_idle_set = 0  # Track which idle animation set is active

        self.load_images()

        self.label = tk.Label(window, bd=0, bg="white")
        self.label.pack()

        self.image_cycle = itertools.cycle(self.idle_images[self.current_idle_set])
        self.animate_pet()
        self.move_pet()

        # Bind dragging event
        self.label.bind("<B1-Motion>", self.dragging)
        self.label.bind("<ButtonRelease-1>", self.stop_dragging)
        self.label.bind("<Button-3>", self.toggle_walking)  # Right-click to toggle walking
        # To quit on double-click
        self.label.bind("<Double-Button-1>", lambda e: self.window.quit())

    def load_images(self):
        try:
            # Load idle images
            self.idle_images = [
                [ImageTk.PhotoImage(
                    Image.open(os.path.join(self.assets_path, f"idle-set-1 ({img}).png"))
                    .resize(self.size, Image.Resampling.BOX)
                    )
                    for img in range(1, self.idle_frames_1 + 1)],
                [ImageTk.PhotoImage(
                    Image.open(os.path.join(self.assets_path, f"idle-set-2 ({img}).png"))
                    .resize(self.size, Image.Resampling.BOX)
                    )
                    for img in range(1, self.idle_frames_2 + 1)],
                [ImageTk.PhotoImage(
                    Image.open(os.path.join(self.assets_path, f"idle-set-3 ({img}).png"))
                    .resize(self.size, Image.Resampling.BOX)
                )
                    for img in range(1, self.idle_frames_3 + 1)],
                [ImageTk.PhotoImage(
                    Image.open(os.path.join(self.assets_path, f"idle-set-4 ({img}).png"))
                    .resize(self.size, Image.Resampling.BOX)
                )
                    for img in range(1, self.idle_frames_4 + 1)]
            ]

            # Load dragging images
            self.dragging_images = [
                ImageTk.PhotoImage(Image.open(os.path.join(self.assets_path, f"drag ({img}).png"))
                                   .resize(self.size, Image.Resampling.BOX)
                                   )
                for img in range(1, self.drag_frames + 1)
            ]

            # Load direction-specific walking images
            directions = ['up', 'down', 'left', 'right']
            for direction in directions:
                self.walking_images[direction] = [
                    ImageTk.PhotoImage(
                        Image.open(os.path.join(
                            self.assets_path, f"walk-{direction} ({i}).png"))
                        .resize(self.size, Image.Resampling.BOX)
                        )
                    for i in range(1, self.walk_frames + 1)  # Should have the same number of frames for each direction
                ]
            if not self.idle_images or not self.walking_images or not self.dragging_images:
                print("No images found! Make sure you have images in the 'assets' folder.")
        except Exception as e:
            print(f"Error loading images: {e}")

    def animate_pet(self):
        if not self.is_walking and not self.is_dragging:
            # Increment the idle timer
            self.idle_timer += self.framerate  # Increment by the animation frame delay
            if self.idle_timer >= self.idle_duration:
                # Reset the idle timer and switch to a different idle set
                self.idle_timer = 0
                self.current_idle_set = (self.current_idle_set + 1) % len(self.idle_images)  # Cycle through idle sets
                self.label.config(image=next(self.image_cycle))
                self.image_cycle = itertools.cycle(self.idle_images[self.current_idle_set])
        if self.is_walking and not self.is_dragging:
            self.label.config(image=next(self.image_cycle))
        self.label.config(image=next(self.image_cycle))
        self.window.after(self.framerate, self.animate_pet)  # Adjust the speed here

    def dragging(self, event):
        # Switch to dragging animation
        if not self.is_dragging:
            self.is_dragging = True
            self.image_cycle = itertools.cycle(self.dragging_images)  # Switch to dragging images
            self.idle_timer = 0

        x = self.window.winfo_pointerx() - self.window.winfo_width() // 2
        y = self.window.winfo_pointery() - self.window.winfo_height() // 2
        self.window.geometry(f"+{x}+{y}")

    def move_pet(self):
        if self.is_walking and not self.is_dragging:
            self.idle_timer = 0  # Reset idle timer when the pet is moving

            # self.image_cycle = itertools.cycle(self.walking_images[self.current_direction])
            if self.time_moved_in_direction >= self.direction_duration:
                # Change direction after the current duration
                self.current_direction = random.choice(['up', 'down', 'left', 'right'])
                self.direction_duration = random.randint(5, 30)  # Randomize how long to move in the current direction
                self.time_moved_in_direction = 0  # Reset the movement timer

                # Refresh the image cycle to the new direction
                self.image_cycle = itertools.cycle(self.walking_images[self.current_direction])

            # Get the screen dimensions
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()

            # Move the pet in the current direction
            x_move, y_move = 0, 0
            if self.current_direction == 'up':
                y_move = -10
            elif self.current_direction == 'down':
                y_move = 10
            elif self.current_direction == 'left':
                x_move = -10
            elif self.current_direction == 'right':
                x_move = 10

            current_x = self.window.winfo_x()
            current_y = self.window.winfo_y()

            new_x = current_x + x_move
            new_y = current_y + y_move

            # Check for screen boundaries and reverse direction if a border is hit
            if new_x <= 0:
                self.current_direction = 'right'
                self.image_cycle = itertools.cycle(self.walking_images[self.current_direction])
            elif new_x + self.window.winfo_width() >= screen_width:
                self.current_direction = 'left'
                self.image_cycle = itertools.cycle(self.walking_images[self.current_direction])
            elif new_y <= 0:
                self.current_direction = 'down'
                self.image_cycle = itertools.cycle(self.walking_images[self.current_direction])
            elif new_y + self.window.winfo_height() >= screen_height:
                self.current_direction = 'up'
                self.image_cycle = itertools.cycle(self.walking_images[self.current_direction])

            # Update the window position
            self.window.geometry(f"+{new_x}+{new_y}")

            # Update movement time
            self.time_moved_in_direction += 1

        # Schedule the next move
        self.window.after(self.speed, self.move_pet)  # Adjust the speed of movement

    def stop_dragging(self, event):
        # Switch back to idle animation
        self.is_dragging = False
        if not self.is_walking:
            # Switch to idle images when the pet stops walking
            self.image_cycle = itertools.cycle(self.idle_images[self.current_idle_set])

    def toggle_walking(self, event):
        # Toggle walking state when right-clicked
        self.is_walking = not self.is_walking
        if not self.is_walking:
            # Switch to idle images when the pet stops walking
            self.image_cycle = itertools.cycle(self.idle_images[self.current_idle_set])


if __name__ == "__main__":
    root = tk.Tk()
    pet = DesktopPet(root)
    root.mainloop()
