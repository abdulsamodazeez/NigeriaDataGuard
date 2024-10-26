import json
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Load questions from JSON file
def load_questions():
    with open('questions.json', 'r') as f:
        data = json.load(f)
        return data['questions']  # Returns the questions array from the JSON

class QuestionnaireApp:
    def __init__(self):
        # Initialize session state variables
        if 'authenticated' not in st.session_state:
            st.session_state['authenticated'] = False
        if 'question_index' not in st.session_state:
            st.session_state['question_index'] = 0
        if 'responses' not in st.session_state:
            st.session_state['responses'] = {}
        if 'user_info' not in st.session_state:
            st.session_state['user_info'] = {}
        if 'assessment_completed' not in st.session_state:
            st.session_state['assessment_completed'] = False

        self.questions = load_questions()
        self.create_layout()

    def login(self):
        st.title("NDPA Compliance Assessment Login")
        
        # Create a form for login
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            organization = st.text_input("Organization Name")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                if self.verify_credentials(email, password):
                    st.session_state["authenticated"] = True
                    st.session_state["user_info"] = {
                        "email": email,
                        "organization": organization
                    }
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")

    def verify_credentials(self, email, password):
        # Simple credential verification (replace with actual authentication system)
        return email == "user@example.com" and password == "password"

    def create_layout(self):
        if not st.session_state["authenticated"]:
            self.login()
        else:
            # Create sidebar navigation
            st.sidebar.title("Navigation")
            selection = st.sidebar.radio(
                "Go to",
                ["Home", "About", "Answer Questions", "View Results", "Upload Documents"]
            )
            
            # # Display user info in sidebar
            if st.session_state.get("user_info"):
                st.sidebar.divider()
                st.sidebar.markdown("**Logged in as:**")
                st.sidebar.write(f"Email: {st.session_state['user_info']['email']}")
                st.sidebar.write(f"Organization: {st.session_state['user_info']['organization']}")
            
            # Handle page routing
            if selection == "Home":
                self.show_home()
            elif selection == "About":
                self.show_about()
            elif selection == "Answer Questions":
                self.answer_questions()
            elif selection == "View Results":
                self.display_results()
            elif selection == "Upload Documents":
                self.upload_file()

    def show_home(self):
        st.title("Welcome to the NDPA Compliance Assessment Tool")
        st.write("""
        This tool helps organizations assess their compliance with the Nigeria Data Protection Act (NDPA).
        The assessment covers key areas including:
        - Data Processing Volume
        - Management Awareness
        - Security Standards
        - Incident Management
        - Digital Processing
        """)
        
        # Display getting started instructions
        st.subheader("Getting Started")
        st.write("""
        1. Navigate to 'Answer Questions' to begin the assessment
        2. Complete all questions honestly and accurately
        3. Review your results in the 'View Results' section
        4. Upload relevant documentation in the 'Upload Documents' section
        """)

    def show_about(self):
        st.title("About NDPA Compliance")
        st.write("""
        The Nigeria Data Protection Act (NDPA) establishes guidelines for processing personal data
        and protecting the privacy rights of data subjects in Nigeria.
        
        This assessment tool helps organizations:
        - Evaluate their current compliance status
        - Identify areas needing improvement
        - Track progress toward full compliance
        - Generate compliance reports
        """)

    def answer_questions(self):
        st.title("NDPA Compliance Assessment")
        
        # Add progress tracking
        total_questions = len(self.questions)
        question_index = st.session_state["question_index"]
        st.progress((question_index + 1) / total_questions)
        st.write(f"Question {question_index + 1} of {total_questions}")
        
        question = self.questions[question_index]
        
        # Display question category and risk level
        st.subheader(f"Category: {question['category']}")
        risk_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        st.write(f"Risk Level: {risk_color.get(question['risk_level'], '⚪')} {question['risk_level'].title()}")
        
        # Display question and guidance
        st.write(f"**{question['question']}**")
        st.info(question['guidance'])
        
        # Display options
        options = question.get("options", ["Yes", "No"])
        selected_option = st.session_state['responses'].get(question['id'], options[0])
        selected_option = st.radio("Select your answer:", options, index=options.index(selected_option))
        
        # Add optional comments
        comments = st.text_area(
            "Additional Comments (optional)",
            value=st.session_state.get(f"comments_{question['id']}", "")
        )
        st.session_state[f"comments_{question['id']}"] = comments
        
        # Save response
        st.session_state['responses'][question['id']] = selected_option

        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if question_index > 0:
                if st.button("Previous"):
                    st.session_state["question_index"] -= 1
        with col2:
            if question_index < len(self.questions) - 1:
                if st.button("Next"):
                    st.session_state["question_index"] += 1
        with col3:
            if question_index == len(self.questions) - 1:
                if st.button("Submit"):
                    if len(st.session_state['responses']) == len(self.questions):
                        self.save_responses()
                        st.success("Assessment completed! View your results in the 'View Results' section.")
                        st.session_state['assessment_completed'] = True
                    else:
                        st.error("Please answer all questions before submitting.")

    def save_responses(self):
        # In a real application, you would save to a database here
        st.session_state['assessment_completed'] = True
        st.success("Responses saved successfully.")

    def display_results(self):
        if not st.session_state.get('assessment_completed'):
            st.warning("Please complete the assessment before viewing results.")
            st.write("Navigate to 'Answer Questions' to complete the assessment.")
            return

        st.title("NDPA Compliance Assessment Results")
        
        # Create DataFrame with detailed information
        results = []
        for question in self.questions:
            results.append({
                'Category': question['category'],
                'Question': question['question'],
                'Response': st.session_state['responses'].get(question['id'], 'Not Answered'),
                'Risk Level': question['risk_level'],
                'Comments': st.session_state.get(f"comments_{question['id']}", "")
            })
        
        df = pd.DataFrame(results)
        
        # Calculate compliance score
        compliance_score = len(df[df['Response'] == 'Yes']) / len(df) * 100
        
        # Display overall score
        st.subheader("Overall Compliance Score")
        st.metric("Compliance Score", f"{compliance_score:.1f}%")
        
        # Display summary statistics
        st.subheader("Response Summary by Category")
        category_summary = df.pivot_table(
            index='Category',
            columns='Response',
            aggfunc='size',
            fill_value=0
        )
        st.write(category_summary)
        
        # Create visualizations
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.pie(df, names="Response", title="Overall Response Distribution")
            st.plotly_chart(fig1)
        
        with col2:
            fig2 = px.bar(df, x="Category", color="Risk Level", 
                         title="Responses by Category and Risk Level")
            st.plotly_chart(fig2)
        
        # Display detailed responses
        st.subheader("Detailed Responses")
        st.dataframe(df)
        
        # Export options
        if st.button("Export Results"):
            # Create Excel file
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Compliance Results', index=False)
                
                # Add summary sheet
                summary_df = pd.DataFrame({
                    'Metric': ['Compliance Score', 'Total Questions', 'Questions Answered'],
                    'Value': [
                        f"{compliance_score:.1f}%",
                        len(df),
                        len([r for r in df['Response'] if r != 'Not Answered'])
                    ]
                })
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Offer download
            st.download_button(
                label="Download Excel Report",
                data=output.getvalue(),
                file_name=f"ndpa_compliance_report_{st.session_state['user_info']['organization']}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


    def upload_file(self):
        st.title("Upload Supporting Documents")
        st.write("""
        Upload relevant documentation to support your compliance assessment.
        Accepted file types: PDF, DOCX, TXT
        """)
        
        uploaded_file = st.file_uploader(
            "Choose files to upload",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True
        )
        
        if uploaded_file:
            for file in uploaded_file:
                st.success(f"File uploaded successfully: {file.name}")
                # In a real application, you would process and store the file here

# Run the App
if __name__ == "__main__":
    st.set_page_config(
        page_title="NDPA Compliance Assessment",
        page_icon="📋",
        layout="wide"
    )
    QuestionnaireApp()