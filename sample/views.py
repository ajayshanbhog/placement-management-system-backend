from django.http import JsonResponse
from .models import Sample
from .serializers import SampleSerializers
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

@api_view(['GET','POST'])
def sample_list(request):

    if request.method == 'GET':
        sample = Sample.objects.all()
        serializer = SampleSerializers(sample, many = True)
        return JsonResponse({'sample':serializer.data})   

    if request.method == 'POST':
        serializer = SampleSerializers(data = request.data)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])        
def sample_detail(request,id):

    if request.method == 'GET':
        SampleSerializers()
    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        pass       


@api_view(['POST'])
def login_faculty(request):
    email = request.data.get('email')
    password = request.data.get('password')
    faculty = get_object_or_404(Faculty, email=email)
    if check_password(password, faculty.password):
        return Response({'message': 'Login successful', 'user_id': faculty.faculty_id}, status=status.HTTP_200_OK)
    return Response({'message': 'Login Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_company(request):
    name = request.data.get('name')
    password = request.data.get('password')
    company = get_object_or_404(Company, name=name)
    if check_password(password, company.password):
        return Response({'message': 'Login successful', 'user_id': company.company_id}, status=status.HTTP_200_OK)
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
            'student_cgpa': student.cgpa if student.cgpa is not None else None  # Converts Decimal to float or returns None
        }, status=status.HTTP_200_OK)

    # If the password is incorrect
    return Response({'message': 'Login Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)







@api_view(['POST'])
def register_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Student registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_company(request):
    serializer = CompanySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Company registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_faculty(request):
    serializer = FacultySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Faculty registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






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
    students = Student.objects.filter(user_id=faculty_user_id)
    serializer = StudentSerializerForFaculty(students, many=True)
    return Response(serializer.data)

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




# Define a custom SQL query to fetch the required applicant data
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
            a.type
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
            'type': row[11]
        })

    return Response(applicants)









# Edit Api for profiles



# Faculty Update API - Only password, email, and phone number can be changed
@api_view(['PUT'])
def update_faculty_profile(request, faculty_id):
    """
    Update Faculty profile by faculty_id, allowing partial updates.
    """
    try:
        # Check if the faculty member exists
        try:
            Faculty.objects.get(faculty_id=faculty_id)
        except Faculty.DoesNotExist:
            return Response({'message': 'Faculty not found'}, status=status.HTTP_404_NOT_FOUND)

        # Define fields to update
        fields_to_update = {}

        if request.data.get('role') is not None:
            fields_to_update['role'] = request.data.get('role')

        if request.data.get('staff_id') is not None:
            fields_to_update['staff_id'] = request.data.get('staff_id')

        if request.data.get('name') is not None:
            fields_to_update['name'] = request.data.get('name')

        if request.data.get('email') is not None:
            fields_to_update['email'] = request.data.get('email')

        if request.data.get('ph_number') is not None:
            fields_to_update['ph_number'] = request.data.get('ph_number')

        if request.data.get('department') is not None:
            fields_to_update['department'] = request.data.get('department')

        if request.data.get('password') is not None:
            fields_to_update['password'] = make_password(request.data.get('password'))

        # Construct dynamic SQL query for partial updates
        set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
        query = f"UPDATE sample_faculty SET {set_clause} WHERE faculty_id = %s"

        # Execute query with values in correct order
        with connection.cursor() as cursor:
            cursor.execute(query, list(fields_to_update.values()) + [faculty_id])

        return Response({"message": "Faculty profile updated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Student Update API - Only password, email, and phone number can be changed
@api_view(['PUT'])
def update_student_profile(request, student_id):
    """
    Update Student profile by student_id, allowing partial updates.
    """
    try:
        # Check if the student exists
        try:
            Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            return Response({'message': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        # Define fields to update
        fields_to_update = {}

        if request.data.get('name') is not None:
            fields_to_update['name'] = request.data.get('name')

        if request.data.get('email') is not None:
            fields_to_update['email'] = request.data.get('email')

        if request.data.get('ph_number') is not None:
            fields_to_update['ph_number'] = request.data.get('ph_number')

        if request.data.get('password') is not None:
            fields_to_update['password'] = make_password(request.data.get('password'))

        # Construct dynamic SQL query for partial updates
        set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
        query = f"UPDATE sample_student SET {set_clause} WHERE student_id = %s"

        # Execute query with values in correct order
        with connection.cursor() as cursor:
            cursor.execute(query, list(fields_to_update.values()) + [student_id])

        return Response({"message": "Student profile updated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Company Update API

@api_view(['PUT'])
def update_company_profile(request, company_id):
    """
    Update Company profile by company_id, allowing partial updates.
    """
    try:
        # Check if the company exists
        try:
            Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            return Response({'message': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get allowed fields from request body
        fields_to_update = {}
        
        if request.data.get('name') is not None:
            fields_to_update['name'] = request.data.get('name')
        
        if request.data.get('type') is not None:
            fields_to_update['type'] = request.data.get('type')
        
        if request.data.get('designation_role') is not None:
            fields_to_update['designation_role'] = request.data.get('designation_role')
        
        if request.data.get('location') is not None:
            fields_to_update['location'] = request.data.get('location')
        
        if request.data.get('password') is not None:
            fields_to_update['password'] = make_password(request.data.get('password'))

        # Construct dynamic SQL query for partial updates
        set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
        query = f"UPDATE sample_company SET {set_clause} WHERE company_id = %s"
        
        # Execute query with values in correct order
        with connection.cursor() as cursor:
            cursor.execute(query, list(fields_to_update.values()) + [company_id])

        return Response({"message": "Company profile updated successfully"}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)














from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def get_faculty_profile(request, user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT faculty_id, role, staff_id, name, email, ph_number, department FROM sample_faculty WHERE faculty_id = %s", [user_id])
        row = cursor.fetchone()

    if row:
        data = {
            "role": row[1],
            "staff_id": row[2],
            "name": row[3],
            "email": row[4],
            "ph_number": row[5],
            "department": row[6],
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Faculty not found"}, status=404)
    

@require_http_methods(["GET"])
def get_student_profile(request, user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT student_id, name, SRN, branch, dob, email, ph_number, gender, cgpa, faculty_advisor FROM sample_student WHERE student_id = %s", [user_id])
        row = cursor.fetchone()

    if row:
        data = {
            "name": row[1],
            "SRN": row[2],
            "branch": row[3],
            "dob": row[4],
            "email": row[5],
            "ph_number": row[6],
            "gender": row[7],
            "cgpa": row[8],
            "faculty_advisor": row[9],
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Student not found"}, status=404)   
    

@require_http_methods(["GET"])
def get_company_profile(request, user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT company_id, name, type, designation_role, location, package FROM sample_company WHERE company_id = %s", [user_id])
        row = cursor.fetchone()

    if row:
        data = {
            "name": row[1],
            "type": row[2],
            "designation_role": row[3],
            "location": row[4],
            "package": row[5],
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
            print(data)
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
        # SQL query to delete a FullTime job by ID
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sample_fulltime WHERE job_id = %s", [pk])
        return JsonResponse({"message": "FullTime job deleted successfully"})


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
        # SQL query to delete an Internship by ID
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sample_internship WHERE internship_id = %s", [pk])
        return JsonResponse({"message": "Internship deleted successfully"})