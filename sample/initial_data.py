from sample.models import Faculty
from django.contrib.auth.hashers import make_password
from sample.models import Student, Faculty
from sample.models import Company

Faculty.objects.create(
    role='Professor',
    staff_id='FAC001',
    user_id=1,
    password=make_password('password123'),
    name='Dr. Alice Johnson',
    email='alice.johnson@example.com',
    ph_number='1234567890',
    department='Computer Science'
)

Faculty.objects.create(
    role='Assistant Professor',
    staff_id='FAC002',
    user_id=2,
    password=make_password('password123'),
    name='Dr. Bob Smith',
    email='bob.smith@example.com',
    ph_number='0987654321',
    department='Mathematics'
)

Faculty.objects.create(
    role='Associate Professor',
    staff_id='FAC003',
    user_id=3,
    password=make_password('password123'),
    name='Dr. Carol Lee',
    email='carol.lee@example.com',
    ph_number='1122334455',
    department='Physics'
)



advisor = Faculty.objects.get(staff_id='FAC001')  # Assuming Alice Johnson is the faculty advisor

Student.objects.create(
    name='John Doe',
    SRN='SRN001',
    branch='Computer Science',
    dob='2000-01-15',
    email='john.doe@example.com',
    ph_number='1231231234',
    gender='Male',
    cgpa=8.5,
    faculty_advisor='Dr. Alice Johnson',
    user_id=advisor,
    password=make_password('password123')
)

Student.objects.create(
    name='Jane Doe',
    SRN='SRN002',
    branch='Mechanical Engineering',
    dob='2001-02-20',
    email='jane.doe@example.com',
    ph_number='2342342345',
    gender='Female',
    cgpa=9.2,
    faculty_advisor='Dr. Bob Smith',
    user_id_id=Faculty.objects.get(staff_id='FAC002'),  # Assuming Bob Smith as advisor
    password=make_password('password123')
)

Student.objects.create(
    name='Mike Ross',
    SRN='SRN003',
    branch='Electrical Engineering',
    dob='1999-03-25',
    email='mike.ross@example.com',
    ph_number='3453453456',
    gender='Male',
    cgpa=7.8,
    faculty_advisor='Dr. Carol Lee',
    user_id_id=Faculty.objects.get(staff_id='FAC003'),  # Assuming Carol Lee as advisor
    password=make_password('password123')
)



Company.objects.create(
    name='TechCorp',
    type='Technology',
    designation_role='Software Engineer',
    location='San Francisco, CA',
    package=120000.00,
    user_id=1001,
    password=make_password('password123')
)

Company.objects.create(
    name='BizInc',
    type='Consulting',
    designation_role='Business Analyst',
    location='New York, NY',
    package=90000.00,
    user_id=1002,
    password=make_password('password123')
)

Company.objects.create(
    name='MediSolutions',
    type='Healthcare',
    designation_role='Data Analyst',
    location='Austin, TX',
    package=85000.00,
    user_id=1003,
    password=make_password('password123')
)


































from django.contrib.auth.hashers import make_password
from sample.models import Faculty

# Creating 3 dummy Faculty data with hashed password
faculty1 = Faculty.objects.create(
    role="Professor",
    staff_id="F101",
    user_id=101,
    password=make_password("1234"),  # Password hashed using make_password
    name="Dr. John Doe",
    email="john.doe@pes.edu",
    ph_number="9201112233",
    department="Computer Science"
)

faculty2 = Faculty.objects.create(
    role="Associate Professor",
    staff_id="F102",
    user_id=102,
    password=make_password("1234"),  # Password hashed using make_password
    name="Dr. Jane Smith",
    email="jane.smith@pes.edu",
    ph_number="9201122334",
    department="Mathematics"
)

faculty3 = Faculty.objects.create(
    role="Assistant Professor",
    staff_id="F103",
    user_id=103,
    password=make_password("1234"),  # Password hashed using make_password
    name="Dr. Alan Turing",
    email="alan.turing@pes.edu",
    ph_number="9201133445",
    department="Physics"
)

print("Faculty data with hashed passwords created!")





from django.contrib.auth.hashers import make_password
from sample.models import Student, Faculty

# Get Faculty instances
faculty1 = Faculty.objects.get(faculty_id=1)
faculty2 = Faculty.objects.get(faculty_id=2)
faculty3 = Faculty.objects.get(faculty_id=3)

# Creating 10 dummy Student data with custom SRN format and hashed password
student1 = Student.objects.create(
    name="Alice Green",
    SRN="PES1UG22AM001",
    branch="Computer Science",
    dob="2000-03-01",
    email="alice.green@student.com",
    ph_number="9200000001",
    gender="Female",
    cgpa=9.2,
    faculty_advisor="Dr. John Doe",
    user_id_id=faculty1,
    password=make_password("1234")  # Password hashed using make_password
)

student2 = Student.objects.create(
    name="Bob Brown",
    SRN="PES1UG22AM002",
    branch="Mathematics",
    dob="2001-04-10",
    email="bob.brown@student.com",
    ph_number="9200000002",
    gender="Male",
    cgpa=8.5,
    faculty_advisor="Dr. Jane Smith",
    user_id_id=faculty2,
    password=make_password("1234")  # Password hashed using make_password
)

student3 = Student.objects.create(
    name="Charlie Black",
    SRN="PES1UG22AM003",
    branch="Physics",
    dob="2000-07-25",
    email="charlie.black@student.com",
    ph_number="9200000003",
    gender="Male",
    cgpa=7.8,
    faculty_advisor="Dr. Alan Turing",
    user_id_id=faculty3,
    password=make_password("1234")  # Password hashed using make_password
)

student4 = Student.objects.create(
    name="David White",
    SRN="PES1UG22AM004",
    branch="Computer Science",
    dob="2001-09-30",
    email="david.white@student.com",
    ph_number="9200000004",
    gender="Male",
    cgpa=8.0,
    faculty_advisor="Dr. John Doe",
    user_id_id=faculty1,
    password=make_password("1234")  # Password hashed using make_password
)

student5 = Student.objects.create(
    name="Eve Blue",
    SRN="PES1UG22AM005",
    branch="Mathematics",
    dob="2000-11-05",
    email="eve.blue@student.com",
    ph_number="9200000005",
    gender="Female",
    cgpa=9.5,
    faculty_advisor="Dr. Jane Smith",
    user_id_id=faculty2,
    password=make_password("1234")  # Password hashed using make_password
)

student6 = Student.objects.create(
    name="Frank Gray",
    SRN="PES1UG22AM006",
    branch="Physics",
    dob="2000-05-20",
    email="frank.gray@student.com",
    ph_number="9200000006",
    gender="Male",
    cgpa=7.2,
    faculty_advisor="Dr. Alan Turing",
    user_id_id=faculty3,
    password=make_password("1234")  # Password hashed using make_password
)

student7 = Student.objects.create(
    name="Grace Yellow",
    SRN="PES1UG22AM007",
    branch="Computer Science",
    dob="2001-01-15",
    email="grace.yellow@student.com",
    ph_number="9200000007",
    gender="Female",
    cgpa=8.9,
    faculty_advisor="Dr. John Doe",
    user_id_id=faculty1,
    password=make_password("1234")  # Password hashed using make_password
)

student8 = Student.objects.create(
    name="Hannah Purple",
    SRN="PES1UG22AM008",
    branch="Mathematics",
    dob="2001-06-18",
    email="hannah.purple@student.com",
    ph_number="9200000008",
    gender="Female",
    cgpa=7.6,
    faculty_advisor="Dr. Jane Smith",
    user_id_id=faculty2,
    password=make_password("1234")  # Password hashed using make_password
)

student9 = Student.objects.create(
    name="Isaac Red",
    SRN="PES1UG22AM009",
    branch="Physics",
    dob="2000-12-22",
    email="isaac.red@student.com",
    ph_number="9200000009",
    gender="Male",
    cgpa=9.0,
    faculty_advisor="Dr. Alan Turing",
    user_id_id=faculty3,
    password=make_password("1234")  # Password hashed using make_password
)

student10 = Student.objects.create(
    name="Jack Orange",
    SRN="PES1UG22AM010",
    branch="Computer Science",
    dob="2001-10-05",
    email="jack.orange@student.com",
    ph_number="9200000010",
    gender="Male",
    cgpa=8.7,
    faculty_advisor="Dr. John Doe",
    user_id_id=faculty1,
    password=make_password("1234")  # Password hashed using make_password
)

print("Student data with SRN format PES1UG22AM000 and hashed passwords created!")



#
# Version 2
#

from django.contrib.auth.hashers import make_password
from sample.models import Company

companies = [
    {"name": "Tech Innovators", "type": "Software", "ph_number": "9123456789", "location": "Silicon Valley", "email": "hiring@techinnovators.com", "password": make_password("1234")},
    {"name": "Green Solutions", "type": "Renewable Energy", "ph_number": "9123456790", "location": "New York", "email": "hiring@greensolutions.com", "password": make_password("1234")},
    {"name": "EduWorld", "type": "Education", "ph_number": "9123456791", "location": "Boston", "email": "hiring@eduworld.com", "password": make_password("1234")},
    {"name": "FinWise", "type": "Finance", "ph_number": "9123456792", "location": "London", "email": "hiring@finwise.com", "password": make_password("1234")},
    {"name": "HealthFirst", "type": "Healthcare", "ph_number": "9123456793", "location": "Los Angeles", "email": "hiring@healthfirst.com", "password": make_password("1234")},
    {"name": "AeroTech", "type": "Aerospace", "ph_number": "9123456794", "location": "Houston", "email": "hiring@aerotech.com", "password": make_password("1234")},
    {"name": "AgriPro", "type": "Agriculture", "ph_number": "9123456795", "location": "Chicago", "email": "hiring@agripro.com", "password": make_password("1234")},
    {"name": "MediaHub", "type": "Media", "ph_number": "9123456796", "location": "Los Angeles", "email": "hiring@mediahub.com", "password": make_password("1234")},
    {"name": "AutoMakers", "type": "Automobile", "ph_number": "9123456797", "location": "Detroit", "email": "hiring@automakers.com", "password": make_password("1234")},
    {"name": "RetailConnect", "type": "Retail", "ph_number": "9123456798", "location": "San Francisco", "email": "hiring@retailconnect.com", "password": make_password("1234")},
]

for company_data in companies:
    Company.objects.create(**company_data)



from django.contrib.auth.hashers import make_password
from sample.models import Faculty

faculty1 = Faculty.objects.create(
    role="Professor",
    password=make_password("1234"),  # Password hashed using make_password
    name="Dr. Arvind Kumar",
    email="arvind.kumar@pes.edu",
    ph_number="9201112233",
    department="CSE (AI & ML)"
)

faculty2 = Faculty.objects.create(
    role="Associate Professor",
    password=make_password("1234"),  # Password hashed using make_password
    name="Dr. Neha Sharma",
    email="neha.sharma@pes.edu",
    ph_number="9201122334",
    department="CSE"
)

faculty3 = Faculty.objects.create(
    role="Assistant Professor",
    password=make_password("1234"),  # Password hashed using make_password
    name="Dr. Ramesh Bhat",
    email="ramesh.bhat@pes.edu",
    ph_number="9201133445",
    department="ECE"
)

faculty4 = Faculty.objects.create(
    role="Professor",
    password=make_password("1234"),  # Password hashed using make_password
    name="Dr. Priya Menon",
    email="priya.menon@pes.edu",
    ph_number="9201144556",
    department="CSE"
)

faculty5 = Faculty.objects.create(
    role="Assistant Professor",
    password=make_password("1234"),  # Password hashed using make_password
    name="Dr. Suresh Rao",
    email="suresh.rao@pes.edu",
    ph_number="9201155667",
    department="CSE (AI & ML)"
)

print("Faculty data with hashed passwords created!")    




from django.contrib.auth.hashers import make_password
from sample.models import Student, Faculty

# Get Faculty instances
faculty1 = Faculty.objects.get(faculty_id=1).faculty_id
faculty2 = Faculty.objects.get(faculty_id=2).faculty_id
faculty3 = Faculty.objects.get(faculty_id=3).faculty_id

# Creating 10 dummy Student data with custom SRN format and hashed password
student1 = Student.objects.create(
    name="Aarav Mehta",
    SRN="PES1UG22CS001",
    branch="Computer Science",
    dob="2000-03-01",
    email="aarav.mehta@gmail.com",
    ph_number="9200000001",
    gender="Male",
    cgpa=8.8,
    faculty_advisor="Dr. Arvind Kumar",
    user_id_id=faculty1,
    password=make_password("1234")
)

student2 = Student.objects.create(
    name="Ananya Iyer",
    SRN="PES1UG22CS002",
    branch="Computer Science",
    dob="2001-04-10",
    email="ananya.iyer@outlook.com",
    ph_number="9200000002",
    gender="Female",
    cgpa=9.1,
    faculty_advisor="Dr. Neha Sharma",
    user_id_id=faculty2,
    password=make_password("1234")
)

student3 = Student.objects.create(
    name="Rohan Desai",
    SRN="PES1UG22EC003",
    branch="Electronics and Communication",
    dob="2000-07-25",
    email="rohan.desai@gmail.com",
    ph_number="9200000003",
    gender="Male",
    cgpa=7.5,
    faculty_advisor="Dr. Ramesh Bhat",
    user_id_id=faculty3,
    password=make_password("1234")
)

student4 = Student.objects.create(
    name="Meera Reddy",
    SRN="PES1UG22CS004",
    branch="Computer Science",
    dob="2001-09-30",
    email="meera.reddy@gmail.com",
    ph_number="9200000004",
    gender="Female",
    cgpa=8.3,
    faculty_advisor="Dr. Arvind Kumar",
    user_id_id=faculty1,
    password=make_password("1234")
)

student5 = Student.objects.create(
    name="Vikram Patil",
    SRN="PES1UG22EC005",
    branch="Electronics and Communication",
    dob="2000-11-05",
    email="vikram.patil@outlook.com",
    ph_number="9200000005",
    gender="Male",
    cgpa=9.0,
    faculty_advisor="Dr. Ramesh Bhat",
    user_id_id=faculty3,
    password=make_password("1234")
)

student6 = Student.objects.create(
    name="Lakshmi Menon",
    SRN="PES1UG22CS006",
    branch="Computer Science",
    dob="2000-05-20",
    email="lakshmi.menon@gmail.com",
    ph_number="9200000006",
    gender="Female",
    cgpa=6.8,
    faculty_advisor="Dr. Neha Sharma",
    user_id_id=faculty2,
    password=make_password("1234")
)

student7 = Student.objects.create(
    name="Siddharth Gupta",
    SRN="PES1UG22EC007",
    branch="Electronics and Communication",
    dob="2001-01-15",
    email="siddharth.gupta@gmail.com",
    ph_number="9200000007",
    gender="Male",
    cgpa=8.1,
    faculty_advisor="Dr. Ramesh Bhat",
    user_id_id=faculty3,
    password=make_password("1234")
)

student8 = Student.objects.create(
    name="Priya Joshi",
    SRN="PES1UG22CS008",
    branch="Computer Science",
    dob="2001-06-18",
    email="priya.joshi@outlook.com",
    ph_number="9200000008",
    gender="Female",
    cgpa=7.6,
    faculty_advisor="Dr. Arvind Kumar",
    user_id_id=faculty1,
    password=make_password("1234")
)

student9 = Student.objects.create(
    name="Arjun Nair",
    SRN="PES1UG22EC009",
    branch="Electronics and Communication",
    dob="2000-12-22",
    email="arjun.nair@gmail.com",
    ph_number="9200000009",
    gender="Male",
    cgpa=7.2,
    faculty_advisor="Dr. Ramesh Bhat",
    user_id_id=faculty3,
    password=make_password("1234")
)

student10 = Student.objects.create(
    name="Kavya Singh",
    SRN="PES1UG22CS010",
    branch="Computer Science",
    dob="2001-10-05",
    email="kavya.singh@outlook.com",
    ph_number="9200000010",
    gender="Female",
    cgpa=9.5,
    faculty_advisor="Dr. Neha Sharma",
    user_id_id=faculty2,
    password=make_password("1234")
)

print("Student data with department-specific SRN format and hashed passwords created!")
