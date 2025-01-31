from django.urls import path
from .views import SendMessageAPIView, GetBotResponsesAPIView

urlpatterns = [
    path("send-message/", SendMessageAPIView.as_view(), name="send-message"),
    path("answers/", GetBotResponsesAPIView.as_view(), name="get-answers"),
    ]

    # path("telegram-webhook/", TelegramWebhookAPIView.as_view(), name="telegram-webhook"),
    # path('telegram-webhook_answer/', TelegramAnswerAPIView.as_view(), name='telegram-webhook-answer'),  # Новый путь

