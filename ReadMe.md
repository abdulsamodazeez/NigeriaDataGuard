# NDPA Compliance Assessment Tool

## Overview
The NDPA Compliance Assessment Tool is a web-based application built with Streamlit that helps organizations evaluate their compliance with the Nigeria Data Protection Act (NDPA). This interactive tool provides a systematic approach to assessing data protection practices, generating insights, and identifying areas for improvement.

## Features

### 1. User Authentication
- Secure login system for organizations
- Organization-specific assessments and results
- Session management for user data persistence

### 2. Interactive Assessment
- Step-by-step questionnaire covering key NDPA compliance areas
- Progress tracking
- Risk-level indicators for each question
- Optional comments for detailed responses

**Categories covered:**
- Data Processing Volume
- Management Awareness
- Security Standards
- Incident Management
- Digital Processing

### 3. Results Analysis
- Real-time compliance scoring
- Visual analytics including:
  - Overall compliance score
  - Category-wise summary
  - Response distribution pie chart
  - Risk level distribution by category
- Detailed response review
- Exportable Excel reports

### 4. Document Management
- Support for multiple file uploads
- Accepted formats: PDF, DOCX, TXT
- Document verification system

## Technical Requirements

### Dependencies
- Streamlit
- pandas
- plotly.express
- json

### File Structure
- `app.py`: Main application file
- `questions.json`: Question bank configuration
- `README.md`: Documentation

### Installation
1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```

2. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure the questions:
    Create a `questions.json` file with the following structure:

    ```json
    {
        "questions": [
            {
                "id": "q1",
                "category": "Data Processing",
                "question": "Question text",
                "guidance": "Guidance text",
                "risk_level": "high/medium/low",
                "options": ["Yes", "No"]
            }
            // ... more questions
        ]
    }

    ```

4. Run the application:

    ```bash
    streamlit run app.py
    ```

## Usage Guide

### 1. Login
- Access the application using default credentials:
  - **Email**: user@example.com
  - **Password**: password
- Enter your organization name.

### 2. Navigation
The application provides five main sections:
- **Home**: Overview and getting started guide
- **About**: Information about NDPA compliance
- **Answer Questions**: Complete the assessment
- **View Results**: Analysis and reports (available after completion)
- **Upload Documents**: Submit supporting documentation

### 3. Completing the Assessment
- Navigate to "Answer Questions"
- Answer each question honestly
- Provide additional comments where necessary
- Use Previous/Next buttons to navigate
- Submit when all questions are answered

### 4. Viewing Results
- Access comprehensive analysis after submission
- Export results in Excel format
- Review category-wise compliance
- Identify areas needing improvement

## Security Considerations
- Current authentication is basic and should be enhanced for production
- Implement proper database storage for responses
- Add encryption for sensitive data
- Include proper file handling for document uploads

## Customization
The application can be customized by:
- Modifying the `questions.json` file
- Adjusting the scoring algorithm
- Adding new visualization types
- Implementing additional security measures
- Customizing the UI theme

## Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request
