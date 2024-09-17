from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student, StudentResult
from .serializers import StudentResultSerializer


class GetStudentById(APIView):
    def get(self, request):
        id_student = request.query_params.get('ids')

        if id_student:
            try:
                student = Student.objects.get(id_unique=id_student)

                results = StudentResult.objects.filter(student=student)

                if results.exists():
                    serializer = StudentResultSerializer(results, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "No results found for this student"}, status=status.HTTP_404_NOT_FOUND)

            except Student.DoesNotExist:
                return Response({"error": "Student with the given ID does not exist"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "You did not provide the 'ids' parameter"}, status=status.HTTP_400_BAD_REQUEST)
