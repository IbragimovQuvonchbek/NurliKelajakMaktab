from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Tests, Results
from .serializers import TestSerializer
from rest_framework import status


class GetAllTestsAPI(APIView):
    def get(self, request):
        test_custom = Tests.objects.all()
        ser = TestSerializer(test_custom, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class GetTestByIdAPI(APIView):
    def get(self, request, pk):
        tests_custom = Tests.objects.all()
        filtered_test = tests_custom.filter(id=pk)
        ser = TestSerializer(filtered_test, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


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
            return Response({"solved": True, "result": user_result, "question_quantity": question_quantity}, status=status.HTTP_200_OK)

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

        # Create a dictionary of correct answers
        specific_test_ans = specific_test.answers.split('\n')
        answer_dict = {}
        for ans in specific_test_ans:
            split_two = ans.split('.')
            if len(split_two) == 2:
                answer_dict[split_two[0].strip()] = split_two[1].strip().lower()

        # Process user input and check for multiple or duplicate answers
        user_solution = test_solutions.split('\n')
        unique_solutions = {}
        incorrect_questions = set()

        for user_ans in user_solution:
            split_two = user_ans.split('.')
            if len(split_two) == 2:
                question_num = split_two[0].strip()
                user_ans_text = split_two[1].strip().lower()

                # If the question has already been answered, mark it as incorrect
                if question_num in unique_solutions:
                    incorrect_questions.add(question_num)
                else:
                    unique_solutions[question_num] = user_ans_text

        # Calculate the number of correct answers
        correct_answer = 0
        for question_num, user_ans_text in unique_solutions.items():
            if question_num not in incorrect_questions and answer_dict.get(question_num) == user_ans_text:
                correct_answer += 1
            else:
                incorrect_questions.add(question_num)  # Mark the question as incorrect if answers don't match

        # Create and save the result
        new_result = Results(
            name=name,
            test=specific_test,
            telegram_id=telegram_id,
            test_solutions='\n'.join([f"{k}.{v}" for k, v in unique_solutions.items()]),
            result=correct_answer
        )
        new_result.save()

        return Response({"result": correct_answer, "question_quantity": len(answer_dict)}, status=status.HTTP_201_CREATED)
