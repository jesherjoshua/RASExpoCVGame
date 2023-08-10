


# Dino IRL - Gesture Controlled Chrome Dinosaur Game

Control the Chrome Dinosaur game using real-life gestures captured through your webcam! This Python program uses the Mediapipe library to detect hand gestures and body poses, enabling you to jump, crouch, and control the game just by moving your body.

## Setup

### Python Virtual Environment

It is recommended to use a Python virtual environment to manage dependencies for this project. This ensures that the required packages do not interfere with your global Python environment.

#### Windows

```bash
# Open a Command Prompt
cd path/to/dino-irl
python -m venv venv
venv\Scripts\activate
```

#### Linux

```bash
# Open a Terminal
cd path/to/dino-irl
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

Once the virtual environment is activated, install the required packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Running the Program

1. Make sure your webcam is connected and functional.
2. Open a Command Prompt or Terminal.
3. Navigate to the project directory.

#### Windows

```bash
venv\Scripts\activate
```

#### Linux

```bash
source venv/bin/activate
```

4. Run the program:

```bash
python online.py
```

5. The program will start capturing your gestures through the webcam and control the Chrome Dinosaur game accordingly.

## How to Play

1. Start the program and follow the instructions displayed on the screen to join your hands and start the game.
2. As the game begins, make the appropriate gestures to control the dinosaur:

   - Join both hands to start the game.
   - Jump to make the dino jump.
   - Crouch to make the dino dodge.
   - Stand upright to stop crouching/jumping.
   - To retry just jump again.

3. The program will send keyboard inputs to control the Chrome Dinosaur game in a web browser.

## Notes

- If you experience issues with window activation, you may need to adjust the window title in the code to match your browser's title.

- Press the `Esc` key to exit the program.

- This program uses the [Mediapipe](https://google.github.io/mediapipe/) library for pose estimation and hand tracking.

- Developed by [Jesher Joshua M](https://github.com/jesherjoshua/)
