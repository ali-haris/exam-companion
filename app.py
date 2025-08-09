import streamlit as st
import json
import datetime
from datetime import timedelta
import pandas as pd
from io import BytesIO
import re

# PDF and document processing
try:
    import PyMuPDF as fitz  # PyMuPDF
except ImportError:
    try:
        import pdfplumber
    except ImportError:
        st.error("Please install PyMuPDF or pdfplumber for PDF processing: pip install PyMuPDF or pip install pdfplumber")

# PDF generation
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch
except ImportError:
    st.error("Please install reportlab for PDF export: pip install reportlab")

# OpenAI API
from openai import OpenAI

# Google Calendar (ICS format)
try:
    from ics import Calendar, Event
    ICS_AVAILABLE = True
except ImportError:
    ICS_AVAILABLE = False

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="AI Exam Study Planner",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== OPENAI SETUP ====================
@st.cache_resource
def get_openai_client():
    """Initialize OpenAI client with API key"""
    return OpenAI(
        api_key="API HERE" #Insert you api here
    )

def call_gpt(prompt, model_name="gpt-4.1"):
    """Call OpenAI GPT API with the given prompt"""
    try:
        client = get_openai_client()
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert study planner and educational consultant. You create optimal study schedules based on available time, course content, and student constraints."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=model_name,
            max_tokens=4096,
            temperature=0.3
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return None

# ==================== PDF PROCESSING ====================
def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file"""
    try:
        # Try PyMuPDF first
        try:
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except:
            # Fallback to pdfplumber
            import pdfplumber
            uploaded_file.seek(0)  # Reset file pointer
            with pdfplumber.open(uploaded_file) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None

def parse_topics_from_content(content):
    """Parse topics from course content"""
    lines = content.strip().split('\n')
    topics = []
    
    for line in lines:
        line = line.strip()
        if line:
            # Remove common bullet point markers
            line = re.sub(r'^[-•\*\d+\.\)]\s*', '', line)
            if len(line) > 5:  # Only consider meaningful topics
                topics.append(line)
    
    return topics

# ==================== TIME CALCULATION ====================
def calculate_available_study_time(exam_date, hours_per_day, busy_hours_list):
    """Calculate total available study time"""
    today = datetime.date.today()
    days_until_exam = (exam_date - today).days
    
    if days_until_exam <= 0:
        return 0, 0
    
    # Calculate busy hours per day
    busy_hours_per_day = 0
    for busy_slot in busy_hours_list:
        if busy_slot.strip():
            # Parse time range like "1pm-2pm" or "13:00-14:00"
            try:
                time_parts = re.findall(r'\d+', busy_slot)
                if len(time_parts) >= 2:
                    busy_hours_per_day += 1  # Simplified: assume 1 hour per slot
            except:
                pass
    
    effective_hours_per_day = max(0, hours_per_day - busy_hours_per_day)
    total_study_hours = days_until_exam * effective_hours_per_day
    
    return days_until_exam, total_study_hours

# ==================== AI STUDY PLANNER ====================
def generate_study_schedule(topics, days_available, hours_per_day, busy_hours, exam_date):
    """Generate study schedule using OpenAI"""
    
    topics_str = "\n".join([f"- {topic}" for topic in topics])
    busy_hours_str = "\n".join([f"- {slot}" for slot in busy_hours if slot.strip()])
    
    prompt = f"""
Create a detailed study schedule for an upcoming exam. Here are the details:

COURSE TOPICS:
{topics_str}

TIME CONSTRAINTS:
- Days until exam: {days_available}
- Hours available per day: {hours_per_day}
- Exam date: {exam_date}

BUSY HOURS (to avoid):
{busy_hours_str}

REQUIREMENTS:
1. If total available time is insufficient, prioritize the most important/foundational topics
2. Distribute topics across available days
3. Avoid the specified busy hours
4. Include review sessions before the exam
5. Balance study intensity (don't overload any single day)

Please return a JSON response in exactly this format:
{{
    "schedule_feasible": true/false,
    "total_topics_scheduled": number,
    "priority_level": "high/medium/low",
    "daily_schedule": [
        {{
            "date": "YYYY-MM-DD",
            "day": "Monday",
            "study_sessions": [
                {{
                    "time": "9:00-11:00",
                    "topic": "Topic name",
                    "type": "study/review",
                    "duration_hours": 2
                }}
            ],
            "total_hours": 4
        }}
    ],
    "study_tips": ["tip1", "tip2", "tip3"]
}}

Make sure the JSON is valid and complete.
"""
    
    response = call_gpt(prompt, model_name="gpt-4.1")
    
    if response:
        try:
            # Clean the response to extract JSON
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end]
                schedule_data = json.loads(json_str)
                return schedule_data
        except json.JSONDecodeError as e:
            st.error(f"Error parsing AI response: {str(e)}")
            return None
    
    return None

# ==================== PDF EXPORT ====================
def wrap_text_for_cell(text, max_width=30):
    """Wrap text to fit in table cells"""
    if len(text) <= max_width:
        return text
    
    # Split long text into multiple lines
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line + word) <= max_width:
            current_line += word + " "
        else:
            if current_line:
                lines.append(current_line.strip())
            current_line = word + " "
    
    if current_line:
        lines.append(current_line.strip())
    
    return "\n".join(lines)

def generate_pdf_schedule(schedule_data, student_name="Student"):
    """Generate PDF of the study schedule"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor=colors.darkblue,
        alignment=1  # Center alignment
    )
    story.append(Paragraph(f"AI Generated Study Schedule for {student_name}", title_style))
    story.append(Spacer(1, 20))
    
    # Schedule Info
    info_data = [
        ["Schedule Feasible", "Yes" if schedule_data.get('schedule_feasible', False) else "No"],
        ["Topics Scheduled", str(schedule_data.get('total_topics_scheduled', 0))],
        ["Priority Level", schedule_data.get('priority_level', 'Medium').title()],
    ]
    
    info_table = Table(info_data, colWidths=[3*inch, 2*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 30))
    
    # Daily Schedule
    story.append(Paragraph("Daily Study Schedule", styles['Heading2']))
    story.append(Spacer(1, 20))
    
    for day_schedule in schedule_data.get('daily_schedule', []):
        # Day header
        day_title = f"{day_schedule['day']} - {day_schedule['date']}"
        story.append(Paragraph(day_title, styles['Heading3']))
        
        # Sessions table with proper text wrapping
        session_data = [['Time', 'Topic', 'Type', 'Duration']]
        for session in day_schedule.get('study_sessions', []):
            # Wrap long topic names
            topic_text = wrap_text_for_cell(session.get('topic', ''), max_width=35)
            session_data.append([
                session.get('time', ''),
                topic_text,
                session.get('type', '').title(),
                f"{session.get('duration_hours', 0)}h"
            ])
        
        # Adjusted column widths to prevent overlap
        session_table = Table(session_data, colWidths=[1.2*inch, 3.5*inch, 0.8*inch, 0.8*inch])
        session_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Top alignment for wrapped text
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('WORDWRAP', (0, 0), (-1, -1), 'CJK'),  # Enable word wrapping
        ]))
        
        story.append(session_table)
        story.append(Spacer(1, 20))
    
    # Study Tips
    if schedule_data.get('study_tips'):
        story.append(Paragraph("Study Tips", styles['Heading2']))
        for tip in schedule_data['study_tips']:
            story.append(Paragraph(f"• {tip}", styles['Normal']))
            story.append(Spacer(1, 10))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ==================== ICS CALENDAR EXPORT ====================
def create_ics_calendar(schedule_data):
    """Create ICS calendar file from study schedule"""
    try:
        c = Calendar()
        
        for day_schedule in schedule_data.get('daily_schedule', []):
            date_str = day_schedule['date']
            
            for session in day_schedule.get('study_sessions', []):
                # Parse time range
                time_range = session.get('time', '')
                if '-' in time_range:
                    start_time_str, end_time_str = time_range.split('-')
                    start_time_str = start_time_str.strip()
                    end_time_str = end_time_str.strip()
                    
                    # Convert to 24-hour format if needed
                    start_hour, start_min = parse_time_to_24h(start_time_str)
                    end_hour, end_min = parse_time_to_24h(end_time_str)
                    
                    # Parse date
                    year, month, day = map(int, date_str.split('-'))
                    
                    # Create datetime objects
                    start_datetime = datetime.datetime(year, month, day, start_hour, start_min)
                    end_datetime = datetime.datetime(year, month, day, end_hour, end_min)
                    
                    # Create event
                    e = Event()
                    e.name = f"Study: {session.get('topic', 'Unknown Topic')}"
                    e.begin = start_datetime
                    e.end = end_datetime
                    e.description = f"Type: {session.get('type', 'Study').title()}\nDuration: {session.get('duration_hours', 0)} hours\n\nGenerated by AI Exam Study Planner"
                    
                    c.events.add(e)
        
        return c
    
    except Exception as e:
        st.error(f"Error creating ICS calendar: {str(e)}")
        return None

def parse_time_to_24h(time_str):
    """Parse time string to 24-hour format and return hour, minute"""
    time_str = time_str.lower().strip()
    
    if 'pm' in time_str:
        hour = int(re.sub(r'[^\d]', '', time_str))
        if hour != 12:
            hour += 12
        return hour, 0
    elif 'am' in time_str:
        hour = int(re.sub(r'[^\d]', '', time_str))
        if hour == 12:
            hour = 0
        return hour, 0
    else:
        # Assume already in 24-hour format or just hour number
        try:
            if ':' in time_str:
                parts = time_str.split(':')
                hour = int(parts[0])
                minute = int(parts[1]) if len(parts) > 1 else 0
                return hour, minute
            else:
                hour = int(time_str)
                return hour, 0
        except:
            return 9, 0  # Default fallback

# ==================== MAIN STREAMLIT APP ====================
def main():
    st.title("📚 AI Exam Study Planner")
    st.markdown("Generate an intelligent study schedule based on your course content, available time, and constraints.")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("📝 Course Information")
        
        # Student name
        student_name = st.text_input("Your Name", "Student")
        
        # Course content input
        input_method = st.radio("How would you like to input course content?", 
                               ["Upload PDF", "Paste Text"])
        
        course_content = ""
        topics = []
        
        if input_method == "Upload PDF":
            uploaded_file = st.file_uploader("Upload course material (PDF)", type=['pdf'])
            if uploaded_file:
                with st.spinner("Extracting text from PDF..."):
                    course_content = extract_text_from_pdf(uploaded_file)
                    if course_content:
                        topics = parse_topics_from_content(course_content)
                        st.success(f"✅ Extracted {len(topics)} topics from PDF")
        else:
            course_content = st.text_area("Paste your course content here", 
                                        height=200,
                                        placeholder="Enter topics, chapters, or key concepts...")
            if course_content:
                topics = parse_topics_from_content(course_content)
                st.success(f"✅ Parsed {len(topics)} topics")
        
        # Display topics preview
        if topics:
            with st.expander("📋 Topics Preview"):
                for i, topic in enumerate(topics[:10], 1):
                    st.write(f"{i}. {topic}")
                if len(topics) > 10:
                    st.write(f"... and {len(topics) - 10} more topics")
        
        st.header("⏰ Time Constraints")
        
        # Exam date
        exam_date = st.date_input("Exam Date", 
                                 min_value=datetime.date.today() + timedelta(days=1))
        
        # Hours per day
        hours_per_day = st.number_input("Hours you can study per day", 
                                       min_value=1, max_value=16, value=4)
        
        st.header("🚫 Busy Hours")
        
        # Busy hours input
        num_busy_slots = st.number_input("Number of busy time slots per day", 
                                        min_value=0, max_value=10, value=2)
        
        busy_hours = []
        for i in range(num_busy_slots):
            busy_slot = st.text_input(f"Busy slot {i+1}", 
                                     placeholder="e.g., 1pm-2pm or 13:00-14:00",
                                     key=f"busy_{i}")
            busy_hours.append(busy_slot)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.header("📊 Schedule Summary")
        
        if topics and exam_date:
            days_available, total_hours = calculate_available_study_time(
                exam_date, hours_per_day, busy_hours
            )
            
            st.metric("Days until exam", days_available)
            st.metric("Total study hours", f"{total_hours}h")
            st.metric("Topics to cover", len(topics))
            
            if total_hours > 0:
                hours_per_topic = round(total_hours / len(topics), 1) if topics else 0
                st.metric("Average hours per topic", f"{hours_per_topic}h")
                
                # Feasibility indicator
                if hours_per_topic < 1:
                    st.warning("⚠️ Limited time - will prioritize key topics")
                elif hours_per_topic < 3:
                    st.info("ℹ️ Moderate time - focused study needed")
                else:
                    st.success("✅ Sufficient time for comprehensive study")
    
    with col1:
        st.header("🤖 Generate Study Schedule")
        
        if st.button("Generate AI Study Plan", type="primary", use_container_width=True):
            if not topics:
                st.error("Please provide course content first!")
            elif exam_date <= datetime.date.today():
                st.error("Exam date must be in the future!")
            else:
                with st.spinner("🧠 AI is creating your personalized study schedule..."):
                    days_available, total_hours = calculate_available_study_time(
                        exam_date, hours_per_day, busy_hours
                    )
                    
                    schedule_data = generate_study_schedule(
                        topics, days_available, hours_per_day, busy_hours, exam_date
                    )
                    
                    if schedule_data:
                        st.session_state['schedule_data'] = schedule_data
                        st.session_state['student_name'] = student_name
                        st.success("✅ Study schedule generated successfully!")
                    else:
                        st.error("Failed to generate study schedule. Please try again.")
        
        # Display generated schedule
        if 'schedule_data' in st.session_state:
            schedule_data = st.session_state['schedule_data']
            
            st.subheader("📅 Your Study Schedule")
            
            # Schedule overview
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Feasible", 
                         "Yes" if schedule_data.get('schedule_feasible', False) else "No")
            with col_b:
                st.metric("Topics Scheduled", schedule_data.get('total_topics_scheduled', 0))
            with col_c:
                st.metric("Priority Level", schedule_data.get('priority_level', 'Medium').title())
            
            # Daily schedule table
            if schedule_data.get('daily_schedule'):
                schedule_df_data = []
                for day in schedule_data['daily_schedule']:
                    for session in day.get('study_sessions', []):
                        schedule_df_data.append({
                            'Date': day['date'],
                            'Day': day['day'],
                            'Time': session.get('time', ''),
                            'Topic': session.get('topic', ''),
                            'Type': session.get('type', '').title(),
                            'Duration': f"{session.get('duration_hours', 0)}h"
                        })
                
                if schedule_df_data:
                    schedule_df = pd.DataFrame(schedule_df_data)
                    st.dataframe(schedule_df, use_container_width=True, hide_index=True)
            
            # Study tips
            if schedule_data.get('study_tips'):
                st.subheader("💡 Study Tips")
                for tip in schedule_data['study_tips']:
                    st.info(f"💡 {tip}")
            
            # Export options
            st.subheader("📤 Export Options")
            col_export1, col_export2 = st.columns(2)
            
            with col_export1:
                if st.button("📄 Download PDF", use_container_width=True):
                    try:
                        pdf_buffer = generate_pdf_schedule(
                            schedule_data, 
                            st.session_state.get('student_name', 'Student')
                        )
                        st.download_button(
                            label="💾 Download Study Schedule PDF",
                            data=pdf_buffer.getvalue(),
                            file_name=f"study_schedule_{datetime.date.today()}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")
            
            with col_export2:
                if st.button("📅 Export to Calendar (.ics)", use_container_width=True):
                    if ICS_AVAILABLE:
                        try:
                            calendar = create_ics_calendar(schedule_data)
                            if calendar:
                                # Convert calendar to string
                                calendar_str = str(calendar)
                                st.download_button(
                                    label="💾 Download Calendar File (.ics)",
                                    data=calendar_str,
                                    file_name=f"study_schedule_{datetime.date.today()}.ics",
                                    mime="text/calendar",
                                    use_container_width=True
                                )
                                st.success("✅ Calendar file ready for download!")
                        except Exception as e:
                            st.error(f"Error creating calendar file: {str(e)}")
                    else:
                        st.error("Calendar export not available. Install 'ics' package: pip install ics")
        
        # Google Calendar Instructions
        if 'schedule_data' in st.session_state:
            st.subheader("📋 How to Import to Google Calendar")
            
            with st.expander("📖 Click here for step-by-step instructions"):
                st.markdown("""
                ### Method 1: Using ICS File (Recommended)
                
                1. **Download the ICS file** by clicking the "Export to Calendar (.ics)" button above
                2. **Open Google Calendar** in your web browser
                3. **Click the "+" button** next to "Other calendars" on the left sidebar
                4. **Select "Create new calendar"** to make a dedicated study calendar (optional but recommended)
                5. **Go back to the main calendar view**
                6. **Click the gear icon** ⚙️ in the top right corner
                7. **Select "Settings"** from the dropdown menu
                8. **Click "Import & export"** in the left sidebar
                9. **Click "Select file from your computer"** and choose your downloaded .ics file
                10. **Choose the calendar** where you want to import (your new study calendar or existing one)
                11. **Click "Import"** - all your study sessions will be added automatically!
                
                ### Method 2: Manual Entry
                
                1. **Open Google Calendar**
                2. **Click on the date and time** for each study session
                3. **Enter the topic name** as the event title
                4. **Set the correct start and end times**
                5. **Add the study type and duration** in the description
                6. **Set reminders** (recommended: 15 minutes and 5 minutes before)
                7. **Choose a color** (e.g., green for study sessions)
                8. **Save the event**
                
                ### Pro Tips:
                - 🎨 **Create a separate calendar** for study sessions to keep them organized
                - 🔔 **Set up notifications** to remind you of upcoming study sessions
                - 📱 **Sync with your mobile device** so you get reminders on your phone
                - 🔄 **Review and adjust** the schedule as needed based on your progress
                
                ### Troubleshooting:
                - If the ICS file doesn't import correctly, try opening it in a text editor first to ensure it's properly formatted
                - Make sure you're using the latest version of your web browser
                - Some browsers may require you to save the file first, then import it
                """)

if __name__ == "__main__":
    main()
