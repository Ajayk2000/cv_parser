import pytesseract
import cv2
import pdf2image
import numpy as np
import os
import json
import fitz
import re
from pdf2image import convert_from_path



skills_list = [
    'Python', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management', 'Deep Learning', 'SQL', 'Tableau',
    'Java', 'C++', 'JavaScript', 'HTML', 'CSS', 'React', 'Angular', 'Node.js', 'MongoDB', 'Express.js', 'Git',
    'Research', 'Statistics', 'Quantitative Analysis', 'Qualitative Analysis', 'SPSS', 'R', 'Data Visualization', 'Matplotlib',
    'Seaborn', 'Plotly', 'Pandas', 'Numpy', 'Scikit-learn', 'TensorFlow', 'Keras', 'PyTorch', 'NLTK', 'Text Mining',
    'Natural Language Processing', 'Computer Vision', 'Image Processing', 'OCR', 'Speech Recognition', 'Recommendation Systems',
    'Collaborative Filtering', 'Content-Based Filtering', 'Reinforcement Learning', 'Neural Networks', 'Convolutional Neural Networks',
    'Recurrent Neural Networks', 'Generative Adversarial Networks', 'XGBoost', 'Random Forest', 'Decision Trees', 'Support Vector Machines',
    'Linear Regression', 'Logistic Regression', 'K-Means Clustering', 'Hierarchical Clustering', 'DBSCAN', 'Association Rule Learning',
    'Apache Hadoop', 'Apache Spark', 'MapReduce', 'Hive', 'HBase', 'Apache Kafka', 'Data Warehousing', 'ETL', 'Big Data Analytics',
    'Cloud Computing', 'Amazon Web Services (AWS)', 'Microsoft Azure', 'Google Cloud Platform (GCP)', 'Docker', 'Kubernetes', 'Linux',
    'Shell Scripting', 'Cybersecurity', 'Network Security', 'Penetration Testing', 'Firewalls', 'Encryption', 'Malware Analysis',
    'Digital Forensics', 'CI/CD', 'DevOps', 'Agile Methodology', 'Scrum', 'Kanban', 'Continuous Integration', 'Continuous Deployment',
    'Software Development', 'Web Development', 'Mobile Development', 'Backend Development', 'Frontend Development', 'Full-Stack Development',
    'UI/UX Design', 'Responsive Design', 'Wireframing', 'Prototyping', 'User Testing', 'Adobe Creative Suite', 'Photoshop', 'Illustrator',
    'InDesign', 'Figma', 'Sketch', 'Zeplin', 'InVision', 'Product Management', 'Market Research', 'Customer Development', 'Lean Startup',
    'Business Development', 'Sales', 'Marketing', 'Content Marketing', 'Social Media Marketing', 'Email Marketing', 'SEO', 'SEM', 'PPC',
    'Google Analytics', 'Facebook Ads', 'LinkedIn Ads', 'Lead Generation', 'Customer Relationship Management (CRM)', 'Salesforce',
    'HubSpot', 'Zendesk', 'Intercom', 'Customer Support', 'Technical Support', 'Troubleshooting', 'Ticketing Systems', 'ServiceNow',
    'ITIL', 'Quality Assurance', 'Manual Testing', 'Automated Testing', 'Selenium', 'JUnit', 'Load Testing', 'Performance Testing',
    'Regression Testing', 'Black Box Testing', 'White Box Testing', 'API Testing', 'Mobile Testing', 'Usability Testing', 'Accessibility Testing',
    'Cross-Browser Testing', 'Agile Testing', 'User Acceptance Testing', 'Software Documentation', 'Technical Writing', 'Copywriting',
    'Editing', 'Proofreading', 'Content Management Systems (CMS)', 'WordPress', 'Joomla', 'Drupal', 'Magento', 'Shopify', 'E-commerce',
    'Payment Gateways', 'Inventory Management', 'Supply Chain Management', 'Logistics', 'Procurement', 'ERP Systems', 'SAP', 'Oracle',
    'Microsoft Dynamics', 'QlikView', 'Looker', 'Data Engineering', 'Data Governance', 'Data Quality', 'Master Data Management',
    'Predictive Analytics', 'Prescriptive Analytics', 'Descriptive Analytics', 'Business Intelligence', 'Dashboarding', 'Reporting',
    'Data Mining', 'Web Scraping', 'API Integration', 'RESTful APIs', 'GraphQL', 'SOAP', 'Microservices', 'Serverless Architecture',
    'Lambda Functions', 'Event-Driven Architecture', 'Message Queues', 'Socket.io', 'WebSockets', 'Ruby', 'Ruby on Rails', 'PHP',
    'Symfony', 'Laravel', 'CakePHP', 'Zend Framework', 'ASP.NET', 'C#', 'VB.NET', 'ASP.NET MVC', 'Entity Framework', 'Spring', 'Hibernate',
    'Struts', 'Kotlin', 'Swift', 'Objective-C', 'iOS Development', 'Android Development', 'Flutter', 'React Native', 'Ionic',
    'Mobile UI/UX Design', 'Material Design', 'SwiftUI', 'RxJava', 'RxSwift', 'Django', 'Flask', 'FastAPI', 'Falcon', 'Tornado',
    'Server Administration', 'System Administration', 'Network Administration', 'Database Administration', 'MySQL', 'PostgreSQL',
    'SQLite', 'Microsoft SQL Server', 'Oracle Database', 'NoSQL', 'Cassandra', 'Redis', 'Elasticsearch', 'Firebase', 'Google Tag Manager',
    'Adobe Analytics', 'Robotic Process Automation (RPA)', 'Virtual Reality (VR)', 'Augmented Reality (AR)', '3D Modeling', 'Animation',
    'Video Editing', 'Sound Design', 'Music Production', 'A/B Testing', 'Customer Experience (CX)', 'User Experience (UX)', 'Persona Development',
    'User Journey Mapping', 'Information Architecture (IA)', 'Internationalization (I18n)', 'Localization (L10n)', 'Chatbots',
    'Document Recognition', 'Fraud Detection', 'Blockchain', 'Cryptocurrency', 'Decentralized Finance (DeFi)', 'Smart Contracts',
    'Talent Acquisition', 'Employee Relations', 'Compensation & Benefits', 'HRIS', 'Payroll Management', 'Succession Planning',
    'Organizational Development', 'Workforce Planning', 'Learning & Development', 'Employee Retention Strategies', 'VPN Configuration',
    'Virtualization', 'Network Load Balancing', 'Strategic Planning & Execution', 'Market Entry Strategies', 'Business Case Development',
    'Corporate Governance', 'Mergers & Acquisitions', 'Operational Excellence', 'Lean Management', 'Cost-Benefit Analysis',
    'Hotel Management Systems', 'Food & Beverage Management', 'Event Planning', 'Catering Services', 'Tour Operations',
    'Brand Positioning', 'Growth Hacking', 'Digital PR', 'Healthcare Compliance', 'Telemedicine', 'Health Informatics', 'Nursing Care Management',
    'Contract Law', 'GDPR Compliance', 'Due Diligence', 'Civil Engineering Project Management', 'Green Energy Solutions',
    'Urban Planning', 'Carbon Footprint Analysis', 'IT Vendor Management', 'Endpoint Security', 'Backup & Recovery Solutions'"Headline Writing",
    "Investigative Journalism","Editorial Writing","Broadcast Scriptwriting","Profile Writing","Narrative Nonfiction",
    "Infographic Design","Live Reporting","Podcast Production","Visual Storyboarding","Cross-platform Content Adaptation","Data-driven Storytelling",
    "Audience Engagement Strategies","Long-form Journalism","Ethical Decision-making in Reporting","Breaking News Coverage","Opinion Piece Development",
    "Collaborative Reporting","Interview Transcription and Analysis","Pitching Stories to Editors","Story development","Commentary writing",
    "Content writing" ,"Interviewing","Content review","Fact-checking"]

def extract_text(file):
    poppler_path = r"C:\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    text = ""

    if file.lower().endswith('.pdf'):
        pages = convert_from_path(file, poppler_path=poppler_path)
        for page in pages:
            frame = np.array(page, dtype="uint8")
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            text += pytesseract.image_to_string(gray)  
            text = text.replace('•','')
            text = text.replace('¢','')
            text = text.replace('®','')
            text = text.replace('®','')
            text = text.replace('™','')
            text = text.replace('-)','')
            text = text.replace('& ','')
            text = text.replace('*','')
            text = text.replace('+','')
            text = text.replace('©','')
            text = text.replace('‘','')
            text = text.replace('«','')
            text = re.sub(r'^e ', '', text, flags=re.MULTILINE)

    elif file.lower().endswith('.docx'):
        doc = fitz.open(file)
        for page in doc:
            text += page.get_text()

    elif file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        image = cv2.imread(file)
        frame = np.array(image, dtype="uint8")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text += pytesseract.image_to_string(gray)
        text = text.replace('•','')
        text = text.replace('¢','')
        text = text.replace('®','')
        text = text.replace('®','')
        text = text.replace('™','')
        text = text.replace('-)','')
        text = text.replace('& ','')
        text = text.replace('*','')
        text = text.replace('+','')
        text = text.replace('©','')
        text = text.replace('‘','')
        text = text.replace('«','')
        text = re.sub(r'^e ', '', text, flags=re.MULTILINE)

    else:
        raise ValueError("Unsupported file format. Only PDF , DOCX and Img are supported.")

    return text

def extract_details(text, skills_list):
    # Initialize result dictionary
    details = {
        "Name": None,
        "Email": None,
        "Contact": None,
        "Linkedin": None,
        "Objective": None,
        "Education": None,
        "Skills": [],
        "Experience": None,
        "Languages": None
    }
    
    # Extract name
    lines = text.strip().split('\n')
    for line in lines[:5]:
        line = line.strip()
        if re.match(r'^[A-Za-z\s]+$', line) and len(line.split()) <= 3:
            if not any(word.lower() in line.lower() for word in ["developer", "engineer", "analyst", "manager", "consultant", "accountant"]):
                details["Name"] = line
                break
    
    # Extract email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_match = re.search(email_pattern, text)
    details["Email"] = email_match.group() if email_match else "Not found"

    # Extract phone number
    ph_pattern = r'(\+?\d{1,3}[\s.-]?)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}\b'
    ph_match = re.search(ph_pattern, text)
    details["Contact"] = ph_match.group() if ph_match else "Not found"

    # Extract LinkedIn
    linkedin_pattern = r'linkedin.com/in/\S+'
    linkedin_match = re.search(linkedin_pattern, text)
    details["Linkedin"] = linkedin_match.group() if linkedin_match else "Not found"

    # Extract Objective
    summary_keywords = ["objective","summary", "profile", "about me", "career overview"]
    summary_pattern = '|'.join([f'{keyword}' for keyword in summary_keywords])
    summary_regex = rf'(?i)({summary_pattern})\s*([\s\S]+?)(?=\n(?:experience|education|skills|projects|certifications|awards|languages|interests|work experience)|$)'
    summary_match = re.search(summary_regex, text)
    if summary_match:
        details["Objective"] = summary_match.group(2).strip()

    # Extract education
    education_keywords = ["education", "academic background", "educational qualifications", "academic history"]
    education_pattern = '|'.join([f'{keyword}' for keyword in education_keywords])
    education_regex = rf'(?i)({education_pattern})\s*([\s\S]+?)(?=\n(?:experience|skills|projects|certifications|awards|languages|interests|work experience)|$)'
    education_match = re.search(education_regex, text)
    if education_match:
        details["Education"] = education_match.group(2).strip()

    # Extract skills
    for skill in skills_list:
        pattern = rf'\b{re.escape(skill)}\b'
        if re.search(pattern, text, re.IGNORECASE):
            details["Skills"].append(skill)

    # Extract experience
    exp_keywords = ["experience", "work history", "professional experience", "employment history", "work experience"]
    exp_pattern = '|'.join([f'{keyword}' for keyword in exp_keywords])
    exp_regex = rf'(?i)({exp_pattern})\s*([\s\S]+?)(?=\n(?:education|skills|projects|certifications|awards|languages|interests)|$)'
    exp_match = re.search(exp_regex, text)
    if exp_match:
        details["Experience"] = exp_match.group(2).strip()

    # Extract languages
    languages_pattern = r'LANGUAGES\s*[:\-]?\s*(.*?)(?:\n\n|\n(?:SOCIAL|CERTIFICATIONS|PERSONAL PROJECTS|REFERENCES|$))'
    languages_match = re.search(languages_pattern, text, re.IGNORECASE | re.DOTALL)
    if languages_match:
        languages_text = languages_match.group(1)
        languages_list = [lang.strip() for lang in languages_text.split('\n') if lang.strip()]
        details["Languages"] = ", ".join(languages_list) if languages_list else "Not found"

    return details
