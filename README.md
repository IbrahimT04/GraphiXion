# GraphiXion

GraphiXion is a 3D graphics rendering engine that supports various 3D features like lighting, texture mapping, and model handling. This project is built with Python and OpenGL and is designed to create immersive scenes with customizable shaders and textures.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [License](#license)

## Features

- **3D Rendering**: Supports rendering of 3D models with textures and lighting.
- **Customizable Shaders**: Modify shaders to adjust lighting, colors, and visual effects.
- **Scene Management**: Organize and manage complex 3D scenes with multiple objects.
- **Camera Control**: Navigate through the scene using camera controls.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/GraphiXion.git
   ```
2. Navigate to the project directory:
   ```bash
   cd GraphiXion
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the project, execute the main script:
```bash
python main.py
```

This will initialize the scene, load objects, and start rendering. Adjust parameters in the scripts to customize the rendering output.

## Project Structure

- **`main.py`**: Entry point for running the application.
- **`camera.py`**: Manages camera control and positioning within the scene.
- **`lighting.py`**: Controls lighting properties for dynamic scenes.
- **`mesh.py`, `model.py`**: Handles mesh generation and model loading.
- **`scene.py`**: Defines the structure of the scene, including objects and lighting.
- **`scene_renderer.py`**: Core rendering logic for displaying the scene.
- **`shader_program.py`**: Manages shader loading and compilation.
- **`vao.py`, `vbo.py`**: Handles OpenGL VAO and VBO management.
- **`shaders/`**: Contains custom shader files.
- **`textures/`**: Stores textures for objects.

## Requirements

- Python 3.x
- OpenGL libraries compatible with Python
- Additional dependencies listed in `requirements.txt`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
