import streamlit as st
import json
from google import genai

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🤖 AI Career Analyzer")

st.write("Find the right career path based on your skills and interests.")

skills = st.text_input(
    "Enter your skills",
    placeholder="Example: Python, SQL, Excel"
)

interests = st.text_input(
    "Enter your interests",
    placeholder="Example: Backend, Web Development, Data"
)

experience = st.selectbox(
    "Select your experience level",
    ["Beginner", "Intermediate", "Advanced"]
)

if st.button("Analyze My Career"):

    if skills:

        skills = skills.lower()
        interests = interests.lower()

        with st.spinner("🤖 AI is analyzing your career profile..."):

            response = client.models.generate_content(
                model="gemini-3.7-flash",
                contents=f"""
    You are an expert AI career advisor.

    Analyze this user's profile:

    Skills: {skills}
    Interests: {interests}
    Experience Level: {experience}

    Identify the most suitable realistic career role based on the
    user's skills, interests, and experience.

    Do not invent skills that the user did not provide.

    Return ONLY valid JSON with these fields:

    recommended_role
    reason
    required_skills
    missing_skills
    match_score
    roadmap

    match_score must be a number from 0 to 100.

    required_skills must contain the important skills normally needed
    for the recommended role.

    missing_skills must contain skills the user needs to develop.

    roadmap must contain practical step-by-step learning actions.
    """,
            config={
                "response_mime_type": "application/json"
    }
)

        analysis = json.loads(response.text) 

        st.success("Career analysis completed!")

        st.subheader("🎯 Recommended Career")
        st.write(analysis["recommended_role"])

        st.subheader("💡 Why?")
        st.write(analysis["reason"])

        st.subheader("📚 Required Skills")

        for skill in analysis["required_skills"]:
            st.markdown(f"✅ **{skill}**")

        st.subheader("❗ Missing Skills")

        for skill in analysis["missing_skills"]:
            st.markdown(f"📌 **{skill}**")

            
        st.subheader("📊 Career Match Score")

        match_score = analysis["match_score"]

        st.metric(
            "Career Match",
            f"{match_score}%"
        )

        st.progress(int(match_score))

        st.subheader("🗺️ Your AI Learning Roadmap")

        for number, step in enumerate(analysis["roadmap"], start=1):
            st.markdown(f"### Step {number}")
            st.write(step)

        # Career Report

        report = f"""
AI CAREER ANALYZER REPORT

Recommended Career:
{analysis["recommended_role"]}

Why:
{analysis["reason"]}

Career Match Score:
{analysis["match_score"]}%

Required Skills:
{", ".join(analysis["required_skills"])}

Missing Skills:
{", ".join(analysis["missing_skills"])}

Experience Level:
{experience}

Interests:
{interests}

AI LEARNING ROADMAP:
"""

        for number, step in enumerate(analysis["roadmap"], start=1):
            report += f"{number}. {step}\n"
       

        st.download_button(
            "📄 Download Career Report",
            report,
            file_name="career_report.txt",
            mime="text/plain"
        )

    else:

        st.warning("Please enter your skills first.")