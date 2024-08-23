from importlib.resources import files

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Tests, Results, TestFile
from .serializers import TestSerializer, TestFileSerializer
from rest_framework import status
from django.db import transaction

class GetAllTestsAPI(APIView):
    def get(self, request):
        test_custom = Tests.objects.all()
        ser = TestSerializer(test_custom, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class GetTestByIdAPI(APIView):
    def get(self, request, pk):
        try:
            filtered_test = Tests.objects.get(id=pk)
        except Tests.DoesNotExist:
            return Response({"detail": "Test not found."}, status=status.HTTP_404_NOT_FOUND)

        filtered_test_file = TestFile.objects.filter(test=filtered_test)

        ser1 = TestSerializer(filtered_test)
        ser2 = TestFileSerializer(filtered_test_file, many=True)

        return Response({
            "test": ser1.data,
            "test_files": ser2.data
        }, status=status.HTTP_200_OK)


class CheckUserSolvedAPI(APIView):
    def get(self, request, pk):
        telegram_id = request.query_params.get('telegram_id')

        if not telegram_id:
            return Response({"error": "Telegram ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        filtered_result_test = Results.objects.filter(telegram_id=telegram_id, test_id=pk)

        if filtered_result_test.exists():
            # Assuming you want to return the result from the first match
            user_result = filtered_result_test.first().result
            question_quantity = filtered_result_test.first().test.question_quantity
            return Response({"solved": True, "result": user_result, "question_quantity": question_quantity},
                            status=status.HTTP_200_OK)

        return Response({"solved": False}, status=status.HTTP_200_OK)


class CheckTestByIdAPI(APIView):
    def post(self, request, pk):
        test_solutions = request.data.get('solution')
        telegram_id = request.data.get('telegram_id')
        name = request.data.get('name')

        # Ensure all necessary data is provided
        if not test_solutions or not telegram_id or not name:
            return Response({"error": "All fields (solution, telegram_id, name) are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Try to get the specific test
        try:
            specific_test = Tests.objects.get(id=pk)
        except Tests.DoesNotExist:
            return Response({"error": "Test not found."}, status=status.HTTP_404_NOT_FOUND)

        specific_test_ans = list(specific_test.answers)

        user_solution = list(test_solutions)

        correct_answer = 0
        actual_ans_len = len(specific_test_ans)
        user_solution_len = len(user_solution)
        for i in range(actual_ans_len):
            if user_solution_len <= i:
                break
            elif user_solution[i] == specific_test_ans[i]:
                correct_answer += 1

        new_result = Results(
            name=name,
            test=specific_test,
            telegram_id=telegram_id,
            test_solutions=test_solutions,
            result=correct_answer
        )
        new_result.save()

        return Response({"result": correct_answer, "question_quantity": actual_ans_len},
                        status=status.HTTP_201_CREATED)


class GetTestFileByIDAPI(APIView):
    def get(self, request, pk):
        tests_custom = TestFile.objects.all()
        filtered_test = tests_custom.filter(id=pk)
        ser = TestFileSerializer(filtered_test, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class AddTestFileAPI(APIView):
    def post(self, request):
        test_id = request.data.get('test_id')
        file_id = request.data.get('file_id')

        if not test_id or not file_id:
            return Response({"error": "All fields (file_id, test_id) are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            specific_test = Tests.objects.get(id=test_id)
        except Tests.DoesNotExist:
            return Response({"error": "Test not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                new_testfile = TestFile(
                    test=specific_test,
                    file_id=file_id
                )
                new_testfile.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"status": "created", "test_file_id": new_testfile.id},
                        status=status.HTTP_201_CREATED)
