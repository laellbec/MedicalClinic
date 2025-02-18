# Medical Clinic System GUI

This repository contains the implementation of a Graphical User Interface (GUI) for a medical clinic system, developed as part of the SENG 265 course at the University of Victoria. The project builds on previous assignments, where a model and file layer were implemented, and now adds a user-friendly interface using the PyQt6 framework.

## Key Features:
- **Model-View-Controller (MVC) Design**: The GUI is decoupled from the model, allowing for modular and maintainable code.
- **User Stories Implementation**: The GUI supports all required user stories, including patient management (create, retrieve, update, delete) and note management for patient records.
- **Dynamic Data Display**: Patient lists are displayed in a `QTableView` widget, while notes and patient records are displayed in a `QPlainTextEdit` widget.
- **Persistent Data**: The system uses JSON and Pickle for data persistence, ensuring that patient and note data are saved between sessions.

## Repository Structure:
- **`controller.py`**: Handles interactions between the GUI and the model.
- **`patient.py`**: Defines the `Patient` class.
- **`patient_record.py`**: Defines the `PatientRecord` class.
- **`note.py`**: Defines the `Note` class.
- **`dao/`**: Contains data access objects for handling JSON and Pickle file storage.
- **`gui/`**: Contains all GUI-related code.
- **`tests/`**: Contains unit and integration tests for the model and controller.

## Learning Outcomes:
- Gained experience in developing GUIs using PyQt6.
- Learned to implement the Model-View-Controller (MVC) design pattern.
- Developed skills in modularizing GUI code and ensuring usability for end users.
- Practiced integrating a GUI with an existing model and file layer
