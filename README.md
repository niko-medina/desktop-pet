
# Desktop Pet

**Desktop Pet** is a simple desktop companion built with Python using Tkinter and PIL. The pet moves around your screen, changes directions, and animates itself while doing so. You can drag the pet around, and it reacts to the borders of the screen by bouncing off them.

**Credits**:  
[Cat animation sprites](https://pixelfight.itch.io/birdcat) by [PixelFight on itch.io](https://pixelfight.itch.io) 
## Features

- **Walking Animation:** The pet animates while walking in different directions.
- **Screen Boundaries:** The pet changes direction when it reaches the edges of your screen.
- **Drag and Drop:** You can click and drag the pet around your desktop.
- **Idle Animation:** The pet will display idle animations when not moving.

## Requirements

- Python 3.6+
- Tkinter (usually included with Python)
- PIL (Pillow) for image handling

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/niko-medina/desktop-pet.git
   cd desktop-pet
   ```

2. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the script:**

   ```bash
   python pet.py
   ```

## Usage

Once the pet is running, it will start moving around your desktop. You can interact with the pet in the following ways:

- **Drag the Pet:** Click and hold the left mouse button on the pet to drag it to a new location.
- **Right-Click to Stop:** Right-click on the pet to stop its movement.
- **Double-Click to Quit:** Double-click on the pet to quit.

## Customization

### Custom Images

1. Place your animation frames in the `assets` folder. Each frame should be a PNG file with a consistent naming pattern (e.g., `up_1.png`, `up_2.png`, etc.).  
Name your files `"idle-set-1 ({i}).png"`, `"idle-set-1 ({i}).png"`, etc. for idle animation, `"drag ({i}).png"` for dragging and `"walk-{direction} ({i}).png"` for walking animation, where {i} is the frame number (starting with 1)  
or modify the `load_images(self)` function in the script to match your files naming pattern.  
Because white color is made transparent, I recommend to not use pure white in your images.

2. Update the `self.idle_images` dictionary in the script to add more sets of idle images.

3. Modify the frames attributes in the script to match the number of frames in your animations:
```
        self.idle_frames_1 = 4  
        self.idle_frames_2 = 4
        self.walk_frames = 8
        self.drag_frames = 4
```
### Changing Size

To change the size of the images modify:  
`self.size = (150, 150)` (width, height)  

### Changing Animation Speed

The animation speed is controlled by the `self.framerate` attribute in the `DesktopPet` class. To change the speed:

```python
self.framerate = 200  # Lower value for faster animation, higher for slower
```

### Adjusting Movement Speed

The movement speed is controlled by the `self.speed` attribute in the `DesktopPet` class. To change the speed:

```python
self.speed = 200  # Lower value for faster movement, higher for slower
```
### Adjusting Idle Animation Duration

The idle animation changes to the next set of images after a duration controlled by the `self.idle_duration` attribute:
```python
# Change idle animation after 60 frames (adjust as needed)
self.idle_duration = self.framerate * 60  
```
## Building an Executable

To distribute the desktop pet as a standalone executable:

1. **Install PyInstaller:**

   ```bash
   pip install pyinstaller
   ```

2. **Create the executable:**

   ```bash
   pyinstaller --add-data "assets/*:assets" --onefile pet.py
   ```

   The executable will be located in the `dist` folder.

