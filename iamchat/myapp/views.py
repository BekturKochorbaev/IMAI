import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MessageSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from django.http import JsonResponse
from .models import BotResponse
from .serializers import BotResponseSerializer

API_URL = "https://71f3-92-62-69-226.ngrok-free.app/ask"


class SendMessageAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data["message"]

            # Отправляем сообщение на API вашего напарника
            payload = {"prompt": message}
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                # Получаем ответ от API вашего напарника
                response = response.json().get("answer", "")

                # Сохраняем сообщение и ответ в базу данных
                BotResponse.objects.create(message=message, response=response)

                # Возвращаем ответ от API вашего напарника
                return Response(
                    {"status": "Message sent!", "response": response},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Failed to send message to API"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetBotResponsesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        responses = BotResponse.objects.all()
        serializer = BotResponseSerializer(responses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#
# class TelegramAnswerAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         # Извлекаем последний ответ бота из базы данных
#         last_response = BotResponse.objects.order_by('-created_at').first()
#
#         if last_response:
#             return Response({
#                 "chat_id": last_response.chat_id,
#                 "user_message": last_response.user_message,
#                 "bot_response": last_response.bot_response
#             }, status=status.HTTP_200_OK)
#
#         return Response({"error": "Нет ответов от бота."}, status=status.HTTP_200_OK)
#
#
#
# class TelegramWebhookAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body.decode("utf-8"))
#
#         if "message" in data:
#             chat_id = data["message"]["chat"]["id"]
#             user_message = data["message"]["text"]
#
#             # Создаем ответ бота
#             bot_response_text = f"Вы написали: {user_message}"
#
#             # Сохраняем ответ в базе данных
#             BotResponse.objects.create(
#                 chat_id=chat_id,
#                 user_message=user_message,
#                 bot_response=bot_response_text
#             )
#
#             # Отправляем ответ в Telegram
#             self.send_message(chat_id, bot_response_text)
#
#             return Response({"status": "ok"}, status=status.HTTP_200_OK)
#
#         return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
#
#     def send_message(self, chat_id, text):
#         """Отправить сообщение в чат"""
#         url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
#         payload = {
#             "chat_id": chat_id,
#             "text": text
#         }
#         response = requests.post(url, data=payload)
#
#         if response.status_code == 200:
#             print(f"Сообщение отправлено в чат {chat_id}")
#         else:
#             print(f"Ошибка при отправке сообщения: {response.status_code}")