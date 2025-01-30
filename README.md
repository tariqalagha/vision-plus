# Vision+ Medical Imaging

A modern medical imaging application built with .NET 7 and WPF, designed for efficient DICOM image viewing and analysis.

## Features

- Modern and intuitive user interface
- DICOM image viewing and manipulation
- Advanced image analysis tools
- Patient data management
- Integration with SPHERE PACS system

## Prerequisites

- Windows OS
- .NET 7.0 SDK or later
- Visual Studio 2022 (recommended)

## Getting Started

1. Clone the repository
```bash
git clone [your-repository-url]
cd Vision+
```

2. Build the project
```bash
dotnet build
```

3. Run the application
```bash
dotnet run
```

## Project Structure

- `Vision_1/` - Main WPF application
  - `MainWindow.xaml` - Main application window
  - `Views/` - Application views
- `Dependencies/` - External dependencies and libraries
- `docs/` - Documentation
- `tests/` - Unit tests

## Dependencies

- fo-dicom (5.1.0)
- Microsoft.ML (2.0.0)
- Microsoft.ML.Vision (2.0.0)
- SixLabors.ImageSharp (3.0.1)
- MaterialDesignThemes (4.9.0)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## SPHERE Integration

This project integrates with SPHERE (PACS solution for Health Research), developed by the EDS-Imaging team within the APHP. For more information about SPHERE, see below:

### What is Sphere?

SPHERE is a PACS software that provides:
- DICOM data collection
- DICOM data export
- DICOMWEB support
- Annotation API

For full SPHERE documentation, please visit the `docs/` directory.
