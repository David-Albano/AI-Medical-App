import json
from django.db.models import Count, Avg, DateField
from django.db.models.functions import Cast
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from transformers import pipeline
from medical_ai.openai_client import get_openai_client
from .models import JournalEntry
from .serializers import JournalEntrySerializer
from .settings import sentiment_analysis_model, text_classification_model

client = get_openai_client()


class JournalEntryView(APIView):
    """Create and analyze a new journal entry"""

    def post(self, request):
        text = request.data.get("text", "")
        if not text:
            return Response({"error": "Text is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize Hugging Face pipelines (do this once)
        sentiment_analyzer = pipeline("sentiment-analysis")
        emotion_analyzer = pipeline("text-classification", model=text_classification_model)
        

        # Run sentiment + emotion analysis
        sentiment_result = sentiment_analyzer(text)[0]
        sentiment_score = round(sentiment_result["score"], 3)
        sentiment = sentiment_result["label"].lower()

        emotion_result = emotion_analyzer(text)[0]
        emotion_score = round(emotion_result["score"], 3)
        emotion = emotion_result["label"].lower()


        # print('\n\n 111111 sentiment_analyzer: ', sentiment_analyzer(text), '\n\n=============')
        # print('\n\n 111111 emotion_analyzer: ', emotion_analyzer(text))

        # print('\n\n 22222 sentiment_result: ', sentiment_result, '\n\n=============')
        # print('\n\n 22222 emotion_result: ', emotion_result)

        # Generate justification
        model_result_justification = self.generate_justification(text, sentiment, sentiment_score, emotion_score, emotion)

        # Generate empathetic feedback
        feedback = self.generate_feedback(sentiment, emotion, sentiment_score, emotion_score, text)

        # Save to DB
        entry = JournalEntry.objects.create(
            text=text,
            sentiment=sentiment,
            emotion=emotion,
            sentiment_score=sentiment_score,
            emotion_score=emotion_score,
            model_result_justification=model_result_justification,
            ai_feedback=feedback,
        )

        serializer = JournalEntrySerializer(entry)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    def generate_feedback(self, sentiment, emotion, sentiment_score, emotion_score, text=None):
        """
        Generate empathetic feedback using OpenAI based on the user's journal entry,
        detected sentiment, and emotion.
        """

        prompt = f"""
            You are an emotionally intelligent medical/wellness assistant helping users reflect on their journal entries.

            Journal text: "{text}"
            Detected sentiment: {sentiment}
            Sentiment Score: {sentiment_score}
            Detected emotion: {emotion}
            Emotion Score: {emotion_score}

            Based on this information, write a brief (2–3 sentences) personal response to the user that:
            - acknowledges or reflects their expressed mood or experience,
            - encourages self-awareness and healthy reflection,
            - maintains a warm, understanding, and supportive tone without assuming the user feels bad or needs fixing.

            Your response should feel natural and human—like a thoughtful friend acknowledging what the person shared.
            Avoid being overly positive or therapeutic unless it matches the tone of the entry.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # you can also use gpt-4o or gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": "You are an empathetic medical/wellness assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=100,
            )

            feedback = response.choices[0].message.content.strip()
            return feedback

        except Exception as e:
            print("OpenAI feedback generation failed:", str(e))
            return "Keep reflecting on your feelings—awareness is a powerful first step."
        

    def generate_justification(self, text, sentiment, emotion, sentiment_score, emotion_score):
        
        prompt = f"""
            You are an AI assistant explaining why a model might have detected this sentiment and emotion.

            Journal text: "{text}"
            Detected sentiment: {sentiment}
            Sentiment Score: {sentiment_score}
            Detected emotion: {emotion}
            Emotion Score: {emotion_score}

            Explain briefly (1–2 sentences each) why a model might have detected from Journal text:
            1. This sentiment
            2. This emotion

            The explanation should focus on linguistic or emotional cues in the text (e.g., words, tone, phrasing).
            Keep it natural, not technical.
            
            Strictly return response with this structure:
            
                Sentiment Justification: ...
                Emotion Justification: ...
                
            With two escape sequence between Sentiment Justification and Emotion Justification
            (Of course instead of ellipsis must be the justification)
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an assistant explaining AI sentiment and emotion detection clearly and simply."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=150,
            )

            content = response.choices[0].message.content.strip()
                
            return content

        except Exception as e:
            print("Justification generation failed:", str(e))
            return "Model reasoning unavailable."
        

    def get(self, request):
        entries = JournalEntry.objects.all().order_by("-date")
        serializer = JournalEntrySerializer(entries, many=True)
        return Response(serializer.data)


# 1. Sentiment Over Time
@api_view(['GET'])
def sentiment_over_time(request):
    try:
        data = (
            JournalEntry.objects
            .filter(date__range=("2025-11-01", "2025-12-31"))
            .exclude(sentiment__isnull=True)
            .annotate(date_only=Cast('date', output_field=DateField()))
            .values('date_only')
            .annotate(avg_sentiment_score=Avg('sentiment_score'))
            .order_by('date_only')
        )

        return Response(list(data))
    except Exception as e:
        raise Exception(str(e))


# 2. Emotion Proportion Pie/Donut
@api_view(['GET'])
def emotion_proportion(request):
    try:
        data = (
            JournalEntry.objects
            .exclude(emotion__isnull=True)
            .values('emotion')
            .annotate(count=Count('id'))
        )

        return Response(list(data))
    
    except Exception as e:
        raise Exception(str(e))


# 3. Daily Journal Activity (for Heatmap)
@api_view(['GET'])
def daily_journal_activity(request):
    try:
        data = (
            JournalEntry.objects
            .annotate(date_only=Cast('date', output_field=DateField()))
            .values('date_only')
            .annotate(count=Count('id'))
            .order_by('date_only')
        )
        return Response(list(data))
    
    except Exception as e:
        raise Exception(str(e))