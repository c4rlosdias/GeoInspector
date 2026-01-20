# GeoInspector

GeoInspector is a Blender/IFC-based application designed to inspect, analyze, and visualize BIM (Building Information Modeling) data. It provides tools for geometric operations, rule-based validation, and interactive previews, supporting workflows for architects, engineers, and BIM managers.

## Main Features

- **IFC File Processing:** Uses ifcopenshell to read and manipulate IFC files, enabling extraction of spatial and element data.
- **Geometric Analysis:** Includes utilities for bounding box calculations, spatial tree generation, and geometric filtering.
- **Rule Management:** Supports custom rule definitions via JSON files for validating BIM elements against project requirements.
- **Interactive Previews:** Integrates with Blender to display element previews and highlight geometry in the 3D viewport.
- **Data Serialization:** Safely exports analysis results to JSON, handling non-serializable objects.
- **Custom Decorators:** Provides decorators for enhanced visualization and annotation of BIM elements.

## Modules Overview

- `data.py`: Core logic for IFC data extraction, geometric operations, and tree generation.
- `operators.py`: Blender operators for running inspections, exporting results, and interacting with the UI.
- `panels.py`: UI panels for controlling the inspection workflow and displaying results.
- `previews.py`: Functions for generating and displaying previews of BIM elements.
- `properties.py`: Custom Blender properties for storing inspection settings and results.
- `decorators.py`: Visualization decorators for highlighting and annotating geometry.
- `rules.py` & `rules.json`: Rule engine and rule definitions for validating BIM elements.
- `resource/`: Additional resources, helper files, and configuration data.

## Usage

1. **Open Blender and load the GeoInspector add-on.**
2. **Import an IFC file** using the BlenderBIM add-on or directly via the UI.
3. **Configure rules** in `rules.json` to match your project requirements.
4. **Run inspections** from the GeoInspector panel to analyze the model.
5. **View results** in the UI or export them to JSON for further processing.

## Requirements

- Blender 3.x or newer
- BlenderBIM add-on
- ifcopenshell Python library

## License

This project is licensed under the terms of the LICENSE file included in the repository.

## Contact

For questions, feedback, or contributions, please contact the project maintainer or open an issue in the repository.
# GeoInspector
Geometry inspector for BIM files
version 0.2.0


