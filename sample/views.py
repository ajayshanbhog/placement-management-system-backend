from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password


from rest_framework import views
from .models import Faculty, Company, Student, Applicants 

from .serializers import FacultySerializer, CompanySerializer, StudentSerializer, ApplicantSerializer
from django.shortcuts import get_object_or_404




from rest_framework import generics
from .models import Internship, FullTime, Rounds
from .serializers import InternshipSerializer, FullTimeSerializer, StudentSerializerForFaculty



from rest_framework.response import Response
from .serializers import StudentSerializer
from django.views.decorators.csrf import csrf_exempt
     
@api_view(['POST'])
def login_faculty(request):
    email = request.data.get('email')
    password = request.data.get('password')
    faculty = get_object_or_404(Faculty, email=email)
    if check_password(password, faculty.password):
        return Response({'message': 'Login successful', 'user_id': faculty.faculty_id, 'name': faculty.name}, status=status.HTTP_200_OK)
    return Response({'message': 'Login Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_company(request):
    name = request.data.get('name')
    password = request.data.get('password')
    company = get_object_or_404(Company, name=name)
    if check_password(password, company.password):
        return Response({'message': 'Login successful', 'user_id': company.company_id,'name': company.name}, status=status.HTTP_200_OK)
    return Response({'message': 'Login Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_student(request):
    srn = request.data.get('SRN')
    password = request.data.get('password')

    # Check if both SRN and password are provided
    if not srn or not password:
        return Response({'message': 'SRN and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Find the student by SRN
    student = Student.objects.filter(SRN=srn).first()
    if student is None:
        return Response({'message': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if password matches
    if check_password(password, student.password):
        return Response({
            'message': 'Login successful',
            'student_id': student.student_id,
            'student_cgpa': student.cgpa if student.cgpa is not None else None,  # Converts Decimal to float or returns None
            'name': student.name
        }, status=status.HTTP_200_OK)

    # If the password is incorrect
    return Response({'message': 'Login Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)







@csrf_exempt
@api_view(['POST'])
def register_student(request):
    data = request.data
    hashed_password = make_password(data['password'])
    query = """
        INSERT INTO sample_student (name, email, ph_number, password)
        VALUES (%s, %s, %s, %s)
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, [data['name'], data['email'], data['ph_number'], hashed_password])
        return JsonResponse({"message": "Student registered successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def register_faculty(request):
    data = request.data
    hashed_password = make_password(data['password'])
    query = """
        INSERT INTO sample_faculty (name, email, ph_number, password)
        VALUES (%s, %s, %s, %s)
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, [data['name'], data['email'], data['ph_number'], hashed_password])
        return JsonResponse({"message": "Faculty registered successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def register_company(request):
    data = request.data
    hashed_password = make_password(data['password'])
    query = """
        INSERT INTO sample_company (name, email, ph_number, password)
        VALUES (%s, %s, %s, %s)
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, [data['name'], data['email'], data['ph_number'], hashed_password])
        return JsonResponse({"message": "Company registered successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)







# Internship Views
class InternshipListCreateView(generics.ListCreateAPIView):
    serializer_class = InternshipSerializer

    def get_queryset(self):
        company_id = self.request.query_params.get('company')
        return Internship.objects.filter(company_id=company_id)

    def perform_create(self, serializer):
        company_id = self.request.data.get('company')
        serializer.save(company_id=company_id)

class InternshipRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer


# FullTime Job Views
class FullTimeListCreateView(generics.ListCreateAPIView):
    serializer_class = FullTimeSerializer

    def get_queryset(self):
        company_id = self.request.query_params.get('company')
        return FullTime.objects.filter(company_id=company_id)

    def perform_create(self, serializer):
        company_id = self.request.data.get('company')
        serializer.save(company_id=company_id)

class FullTimeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FullTime.objects.all()
    serializer_class = FullTimeSerializer



@api_view(['GET'])
def get_students_by_faculty(request, faculty_user_id):
    query = '''
        SELECT 
            s.student_id,
            s.name,
            s.SRN,
            s.branch,
            s.dob,
            s.email,
            s.ph_number,
            s.gender,
            s.cgpa, 
            s.faculty_advisor,
            f.name AS faculty_name,
            f.email AS faculty_email
        FROM 
            sample_student s
        JOIN 
            sample_faculty f ON s.user_id_id = f.faculty_id
        WHERE 
            s.user_id_id = %s;
    '''
    
    with connection.cursor() as cursor:
        cursor.execute(query, [faculty_user_id])
        results = cursor.fetchall()

    # Prepare the results
    students = []
    for row in results:
        students.append({
            'student_id': row[0],
            'name': row[1],
            'SRN': row[2],
            'branch': row[3],
            'dob': row[4],
            'email': row[5],
            'ph_number': row[6],
            'gender': row[7],
            'cgpa': row[8],
            'faculty_advisor': row[9],
            'faculty_name': row[10],
            'faculty_email': row[11]
        })
    
    return Response(students)

@api_view(['GET'])
def students_by_faculty_email(request, faculty_email):
    try:
        faculty = Faculty.objects.get(email=faculty_email)
        students = Student.objects.filter(user_id=faculty)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Faculty.DoesNotExist:
        return Response({'error': 'Faculty not found'}, status=status.HTTP_404_NOT_FOUND)
    







@api_view(['GET'])
def internship_list(request, cgpa):
    try:
        cgpa = float(cgpa)  # Parse the CGPA as a float
    except ValueError:
        return Response({'error': 'Invalid CGPA format'}, status=status.HTTP_400_BAD_REQUEST)

    internships = Internship.objects.filter(cutoff__lte=cgpa)
    serializer = InternshipSerializer(internships, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def fulltime_list(request, cgpa):
    try:
        cgpa = float(cgpa)  # Parse the CGPA as a float
    except ValueError:
        return Response({'error': 'Invalid CGPA format'}, status=status.HTTP_400_BAD_REQUEST)

    fulltime_jobs = FullTime.objects.filter(cutoff__lte=cgpa)
    serializer = FullTimeSerializer(fulltime_jobs, many=True)
    return Response(serializer.data)


from django.db import connection

def dictfetchall(cursor):
    """ Helper function to convert SQL results into a dictionary """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

@api_view(['GET'])
def internship_list_by_srn(request, srn):
    student = Student.objects.filter(SRN=srn).first()
    if not student:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Using raw SQL query to fetch internships with company_name
    query = """
        SELECT internship.internship_id, internship.name, internship.location, internship.stipend,
               internship.ppo, internship.type, internship.duration, internship.cutoff,
               company.name as company_name
        FROM sample_internship as internship
        JOIN sample_company as company ON internship.company_id = company.company_id
        WHERE internship.cutoff <= %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [student.cgpa])
        internships = dictfetchall(cursor)

    return Response(internships)


@api_view(['GET'])
def fulltime_list_by_srn(request, srn):
    student = Student.objects.filter(SRN=srn).first()
    if not student:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Using raw SQL query to fetch full-time jobs with company_name
    query = """
        SELECT fulltime.job_id, fulltime.job_title, fulltime.location, fulltime.package,
               fulltime.cutoff, company.name as company_name
        FROM sample_fulltime as fulltime
        JOIN sample_company as company ON fulltime.company_id = company.company_id
        WHERE fulltime.cutoff <= %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [student.cgpa])
        fulltime_jobs = dictfetchall(cursor)

    return Response(fulltime_jobs)


from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def apply(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        app_type = data.get("type")
        app_id = data.get("id")

        # Fetch student instance
        try:
            student = Student.objects.get(SRN=username)
        except Student.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Student not found"}, status=404)

        # Check application type and apply accordingly
        if app_type == "Internship":
            try:
                internship = Internship.objects.get(internship_id=app_id)
                company = internship.company
                # Check if the student has already applied
                if Applicants.objects.filter(student=student, internship=internship).exists():
                    return JsonResponse({"status": "error", "message": "Already applied"})
                # Otherwise, create a new application
                Applicants.objects.create(student=student, company=company, type="Internship", internship=internship)
            except Internship.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Internship not found"}, status=404)
        elif app_type == "FullTime":
            try:
                job = FullTime.objects.get(job_id=app_id)
                company = job.company
                # Check if the student has already applied
                if Applicants.objects.filter(student=student, job=job).exists():
                    return JsonResponse({"status": "error", "message": "Already applied"})
                # Otherwise, create a new application
                Applicants.objects.create(student=student, company=company, type="FullTime", job=job)
            except FullTime.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Full-time job not found"}, status=404)

        return JsonResponse({"status": "success", "message": "Application successful"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)









@api_view(['GET'])
def check_application_status(request):
    # Get parameters from the request
    student_id = request.GET.get('student_id')  # Use 'student_id' instead of 'srn'
    internship_id = request.GET.get('internship_id')
    job_id = request.GET.get('job_id')

    # Check if either internship_id or job_id is provided
    if not internship_id and not job_id:
        return Response({"error": "Must provide either 'internship_id' or 'job_id'"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the student exists using student_id
    student_query = "SELECT student_id FROM sample_student WHERE student_id = %s"  # Query for student_id
    with connection.cursor() as cursor:
        cursor.execute(student_query, [student_id])
        student = cursor.fetchone()  # Fetch the first row only

    if not student:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the student has applied to the internship or job
    if internship_id:
        application_query = """
            SELECT 1
            FROM sample_applicants
            WHERE student_id = %s AND internship_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(application_query, [student_id, internship_id])
            application_exists = cursor.fetchone() is not None  # Check if a matching record exists

    elif job_id:
        application_query = """
            SELECT 1
            FROM sample_applicants
            WHERE student_id = %s AND job_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(application_query, [student_id, job_id])
            application_exists = cursor.fetchone() is not None  # Check if a matching record exists

    # Return the application status
    if application_exists:
        return Response({"status": "Applied"}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "Not Applied"}, status=status.HTTP_200_OK)




@api_view(['GET'])
def get_applicants_for_company(request, company_id):
    query = '''
        SELECT 
            a.applicant_id,
            s.student_id,
            s.name AS student_name,
            s.SRN,
            s.email,
            s.gender,
            s.ph_number,
            s.cgpa,
            s.faculty_advisor,
            i.name AS internship_name,
            f.job_title AS job_title,
            a.type,
            a.status
        FROM 
            sample_applicants a
        LEFT JOIN sample_student s ON a.student_id = s.student_id
        LEFT JOIN sample_internship i ON a.internship_id = i.internship_id
        LEFT JOIN sample_fulltime f ON a.job_id = f.job_id
        WHERE a.company_id = %s
    '''

    # Execute the SQL query
    with connection.cursor() as cursor:
        cursor.execute(query, [company_id])
        results = cursor.fetchall()

    # Format the results as a list of dictionaries for the response
    applicants = []
    for row in results:
        applicants.append({
            'applicant_id': row[0],
            'student': {
                'student_id': row[1],
                'name': row[2],
                'SRN': row[3],
                'email': row[4],
                'gender': row[5],
                'ph_number': row[6],
                'cgpa': row[7],
                'faculty_advisor': row[8],
            },
            'internship': {
                'name': row[9] if row[9] else None
            },
            'job': {
                'name': row[10] if row[10] else None
            },
            'type': row[11],
            'status': row[12]
        })

    return Response(applicants)

@csrf_exempt
@api_view(['PUT'])
def toggle_applicant_status(request, applicant_id):
    # SQL query to toggle status between 'selected' and 'notselected'
    query = '''
        UPDATE sample_applicants
        SET status = CASE 
                        WHEN status = 'selected' THEN 'notselected'
                        ELSE 'selected'
                     END
        WHERE applicant_id = %s
    '''
    
    with connection.cursor() as cursor:
        cursor.execute(query, [applicant_id])
    
    # Return success response
    return Response({"message": "Applicant status updated successfully."}, status=status.HTTP_200_OK)









# Edit Api for profiles



# Faculty Update API - Only password, email, and phone number can be changed
@csrf_exempt
@api_view(['PUT'])
def update_faculty_profile(request, faculty_id):
    """
    Update Faculty profile by faculty_id, allowing partial updates on specific fields.
    """
    try:
        # Check if the faculty member exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sample_faculty WHERE faculty_id = %s", [faculty_id])
            faculty = cursor.fetchone()
        
        if not faculty:
            return Response({'message': 'Faculty not found'}, status=status.HTTP_404_NOT_FOUND)

        # Define fields to update
        fields_to_update = {}
        
        if request.data.get('email') is not None:
            fields_to_update['email'] = request.data.get('email')
        
        if request.data.get('ph_number') is not None:
            fields_to_update['ph_number'] = request.data.get('ph_number')
        
        if request.data.get('password') is not None:
            fields_to_update['password'] = make_password(request.data.get('password'))

        # Construct dynamic SQL query for partial updates
        if fields_to_update:
            set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
            query = f"UPDATE sample_faculty SET {set_clause} WHERE faculty_id = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, list(fields_to_update.values()) + [faculty_id])

        return Response({"message": "Faculty profile updated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Student Update API - Only email, phone number, and password can be changed
@csrf_exempt
@api_view(['PUT'])
def update_student_profile(request, student_id):
    """
    Update Student profile by student_id, allowing partial updates on specific fields.
    """
    try:
        # Check if the student exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sample_student WHERE student_id = %s", [student_id])
            student = cursor.fetchone()
        
        if not student:
            return Response({'message': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        # Define fields to update
        fields_to_update = {}
        
        if request.data.get('email') is not None:
            fields_to_update['email'] = request.data.get('email')
        
        if request.data.get('ph_number') is not None:
            fields_to_update['ph_number'] = request.data.get('ph_number')
        
        if request.data.get('password') is not None:
            fields_to_update['password'] = make_password(request.data.get('password'))

        # Construct dynamic SQL query for partial updates
        if fields_to_update:
            set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
            query = f"UPDATE sample_student SET {set_clause} WHERE student_id = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, list(fields_to_update.values()) + [student_id])

        return Response({"message": "Student profile updated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Company Update API - Only name, type, location, email, and password can be changed
@csrf_exempt
@api_view(['PUT'])
def update_company_profile(request, company_id):
    """
    Update Company profile by company_id, allowing partial updates on specific fields.
    """
    try:
        # Check if the company exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sample_company WHERE company_id = %s", [company_id])
            company = cursor.fetchone()
        
        if not company:
            return Response({'message': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

        # Define fields to update
        fields_to_update = {}

        if request.data.get('name') is not None:
            fields_to_update['name'] = request.data.get('name')
        
        if request.data.get('type') is not None:
            fields_to_update['type'] = request.data.get('type')
        
        if request.data.get('location') is not None:
            fields_to_update['location'] = request.data.get('location')
        
        if request.data.get('email') is not None:
            fields_to_update['email'] = request.data.get('email')
        
        if request.data.get('password') is not None:
            fields_to_update['password'] = make_password(request.data.get('password'))

        # Construct dynamic SQL query for partial updates
        if fields_to_update:
            set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
            query = f"UPDATE sample_company SET {set_clause} WHERE company_id = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, list(fields_to_update.values()) + [company_id])

        return Response({"message": "Company profile updated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)














from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def get_faculty_profile(request, user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT email, ph_number FROM sample_faculty WHERE faculty_id = %s", [user_id])
        row = cursor.fetchone()

    if row:
        data = {
            "email": row[0],
            "ph_number": row[1],
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Faculty not found"}, status=404)
    

@require_http_methods(["GET"])
def get_student_profile(request, user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT email, ph_number FROM sample_student WHERE student_id = %s", [user_id])
        row = cursor.fetchone()

    if row:
        data = {
            "email": row[0],
            "ph_number": row[1],
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Student not found"}, status=404)   
    

@require_http_methods(["GET"])
def get_company_profile(request, user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, type, location, email FROM sample_company WHERE company_id = %s", [user_id])
        row = cursor.fetchone()

    if row:
        data = {
            "name": row[0],
            "type": row[1],
            "location": row[2],
            "email": row[3],
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Company not found"}, status=404)      
    




from datetime import date as current_date

@csrf_exempt
def create_round(request):
    if request.method == "POST":
        try:
            # Load JSON data from the request body
            data = json.loads(request.body)
            # Retrieve data with default values
            company_id = data.get('company_id')
            round_no = data.get('round_no', -1)
            round_name = data.get('round_name', 'Not Mentioned')
            date = data.get('date', current_date.today())  # Default to today's date if not provided
            time_scheduled = data.get('time_scheduled', '09:00')  # Default time
            status = data.get('status', 'Scheduled')  # Default status
            type = data.get('type', 'Not Mentioned')  # Default type
            internship_id = data.get('internship_id', None)
            job_id = data.get('job_id', None)

            # Ensure at least one of internship_id or job_id is provided
            if not internship_id and not job_id:
                return JsonResponse({'error': 'Either internship_id or job_id must be provided'}, status=400)

            # Execute SQL query to insert a new round
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO sample_rounds (round_no, round_name, date, time_scheduled, status, company_id, type, internship_id, job_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [round_no, round_name, date, time_scheduled, status, company_id, type, internship_id, job_id])

            return JsonResponse({'success': 'Round created successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)








@csrf_exempt
def internship_rounds(request, student_id):
    # SQL query to join Applicants, Rounds, Internship, and Company tables
    query = """
        SELECT r.round_id, r.round_no, r.round_name, r.date, r.time_scheduled, r.status, c.name AS company_name, i.name AS internship_name
        FROM sample_rounds AS r
        INNER JOIN sample_applicants AS a ON r.internship_id = a.internship_id
        INNER JOIN sample_internship AS i ON a.internship_id = i.internship_id
        INNER JOIN sample_company AS c ON i.company_id = c.company_id
        WHERE a.student_id = %s AND a.type = 'Internship';
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query, [student_id])
        rows = cursor.fetchall()
    
    # Prepare response data
    rounds_data = [
        {
            "round_id": row[0],
            "round_no": row[1],
            "round_name": row[2],
            "date": row[3],
            "time_scheduled": row[4],
            "status": row[5],
            "company_name": row[6],
            "internship_name": row[7],
        }
        for row in rows
    ]
    
    return JsonResponse(rounds_data, safe=False)


@csrf_exempt
def job_rounds(request, student_id):
    # SQL query to join Applicants, Rounds, FullTime, and Company tables
    query = """
        SELECT r.round_id, r.round_no, r.round_name, r.date, r.time_scheduled, r.status, c.name AS company_name, f.job_title AS job_name
        FROM sample_rounds AS r
        INNER JOIN sample_applicants AS a ON r.job_id = a.job_id
        INNER JOIN sample_fulltime AS f ON a.job_id = f.job_id
        INNER JOIN sample_company AS c ON f.company_id = c.company_id
        WHERE a.student_id = %s AND a.type = 'FullTime';
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query, [student_id])
        rows = cursor.fetchall()
    
    # Prepare response data
    rounds_data = [
        {
            "round_id": row[0],
            "round_no": row[1],
            "round_name": row[2],
            "date": row[3],
            "time_scheduled": row[4],
            "status": row[5],
            "company_name": row[6],
            "job_name": row[7],
        }
        for row in rows
    ]
    
    return JsonResponse(rounds_data, safe=False)









from django.db import connection, IntegrityError, transaction



@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def fulltime_detail(request, pk):
    if request.method == "GET":
        # SQL query to retrieve a FullTime job by ID
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sample_fulltime WHERE job_id = %s", [pk])
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                data = dict(zip(columns, row))
                return JsonResponse(data, safe=False)
            return JsonResponse({"error": "FullTime job not found"}, status=404)

    elif request.method == "PUT":
        # SQL query to update a FullTime job by ID
        data = json.loads(request.body)
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE sample_fulltime 
                SET job_title = %s, location = %s, package = %s, cutoff = %s, company_id = %s 
                WHERE job_id = %s
            """, [
                data.get("job_title"),
                data.get("location"),
                data.get("package"),
                data.get("cutoff"),
                data.get("company_id"),
                pk
            ])
        return JsonResponse({"message": "FullTime job updated successfully"})

    elif request.method == "DELETE":
        try:
            with transaction.atomic():  # Ensures all-or-nothing execution
                with connection.cursor() as cursor:
                # First, delete dependent records in Rounds and Applicants if not set to cascade
                    cursor.execute("DELETE FROM sample_rounds WHERE job_id = %s", [pk])
                    cursor.execute("DELETE FROM sample_applicants WHERE job_id = %s", [pk])
                
                # Then delete the FullTime job
                    cursor.execute("DELETE FROM sample_fulltime WHERE job_id = %s", [pk])
                
            return JsonResponse({"message": "FullTime job deleted successfully"})
        except IntegrityError:
            return JsonResponse({"error": "Cannot delete FullTime job; it has related records."}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def internship_detail(request, pk):
    if request.method == "GET":
        # SQL query to retrieve an Internship by ID
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sample_internship WHERE internship_id = %s", [pk])
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                data = dict(zip(columns, row))
                return JsonResponse(data, safe=False)
            return JsonResponse({"error": "Internship not found"}, status=404)

    elif request.method == "PUT":
        # SQL query to update an Internship by ID
        data = json.loads(request.body)
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE sample_internship 
                SET name = %s, location = %s, stipend = %s, ppo = %s, type = %s, duration = %s, cutoff = %s, company_id = %s 
                WHERE internship_id = %s
            """, [
                data.get("name"),
                data.get("location"),
                data.get("stipend"),
                data.get("ppo"),
                data.get("type"),
                data.get("duration"),
                data.get("cutoff"),
                data.get("company_id"),
                pk
            ])
        return JsonResponse({"message": "Internship updated successfully"})

    elif request.method == "DELETE":
        try:
            with transaction.atomic():  # Ensures all-or-nothing execution
                with connection.cursor() as cursor:
                # First, delete dependent records in Rounds and Applicants if not set to cascade
                    cursor.execute("DELETE FROM sample_rounds WHERE internship_id = %s", [pk])
                    cursor.execute("DELETE FROM sample_applicants WHERE internship_id = %s", [pk])
                
                # Then delete the Internship
                    cursor.execute("DELETE FROM sample_internship WHERE internship_id = %s", [pk])
                
            return JsonResponse({"message": "Internship deleted successfully"})
        except IntegrityError:
            return JsonResponse({"error": "Cannot delete internship; it has related records."}, status=400)
        








@csrf_exempt
def get_rounds_company_internship_fulltime(request, company_id, id):
    try:
        # Determine if ID is an internship or full-time job
        rounds = []
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT round_id, round_no, round_name, date, time_scheduled, status, type
                FROM sample_rounds
                WHERE company_id = %s AND (internship_id = %s OR job_id = %s)
            """, [company_id, id, id])
            rows = cursor.fetchall()

            # Format result
            rounds = [
                {
                    "round_id": row[0],
                    "round_no": row[1],
                    "round_name": row[2],
                    "date": row[3],
                    "time_scheduled": row[4],
                    "status": row[5],
                    "type": row[6],
                }
                for row in rows
            ]

        return JsonResponse({"rounds": rounds}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    






@csrf_exempt
def delete_round(request, round_id):
    if request.method == "DELETE":
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sample_rounds WHERE round_id = %s", [round_id])
            return JsonResponse({"message": "Round deleted successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    




@api_view(['GET'])
def get_students_results_by_faculty(request, faculty_id):
    query = '''
        SELECT 
            s.name AS student_name,
            c.name AS company_name,
            a.type AS application_type,
            COALESCE(f.job_title, i.name) AS post,
            COALESCE(f.package, i.stipend) AS compensation,
            s.SRN AS srn
        FROM 
            sample_applicants a
        JOIN sample_student s ON a.student_id = s.student_id
        JOIN sample_company c ON a.company_id = c.company_id
        LEFT JOIN sample_fulltime f ON a.job_id = f.job_id
        LEFT JOIN sample_internship i ON a.internship_id = i.internship_id
        WHERE 
            a.status = 'selected'
            AND s.user_id_id = %s
    '''

    # Execute the SQL query
    with connection.cursor() as cursor:
        cursor.execute(query, [faculty_id])
        results = cursor.fetchall()

    # Format the results as a list of dictionaries for the response
    students = []
    for row in results:
        students.append({
            'student_name': row[0],
            'company_name': row[1],
            'application_type': row[2],
            'post': row[3],
            'compensation': row[4],
            'srn': row[5]
        })

    return Response(students)    


@csrf_exempt
def check_selected_status(request, student_id):
    with connection.cursor() as cursor:
        query = '''
            SELECT c.name AS company_name, a.type, 
                   COALESCE(i.stipend, f.package) AS offer_amount 
            FROM sample_applicants a
            LEFT JOIN sample_internship i ON a.internship_id = i.internship_id
            LEFT JOIN sample_fulltime f ON a.job_id = f.job_id
            JOIN sample_company c ON a.company_id = c.company_id
            WHERE a.student_id = %s AND a.status = 'selected'
        '''
        cursor.execute(query, [student_id])
        result = cursor.fetchone()

        if result:
            return JsonResponse({
                'selected': True,
                'company_name': result[0],
                'type': result[1],
                'offer_amount': result[2]
            })
        else:
            return JsonResponse({'selected': False})
        

@csrf_exempt
def toggle_round_status(request, round_id):
    try:
        with connection.cursor() as cursor:
            # Query to get the current status of the round
            cursor.execute('''
                SELECT status FROM sample_rounds WHERE round_id = %s
            ''', [round_id])
            result = cursor.fetchone()

            if result:
                current_status = result[0]
                # Toggle the status based on the current one
                if current_status == 'Scheduled':
                    new_status = 'Completed'
                elif current_status == 'Completed':
                    new_status = 'Cancelled'
                else:
                    new_status = 'Scheduled'

                # Update the status in the database
                cursor.execute('''
                    UPDATE sample_rounds
                    SET status = %s
                    WHERE round_id = %s
                ''', [new_status, round_id])

                return JsonResponse({'status': 'success', 'new_status': new_status})

            else:
                return JsonResponse({'status': 'error', 'message': 'Round not found'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})        