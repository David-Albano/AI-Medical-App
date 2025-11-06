import random
from datetime import timedelta, date
from faker import Faker
from .models import JournalEntry

fake = Faker()

def enter_entries():
    # Define options
    sentiments = ["positive", "negative", "neutral", "mixed"]
    emotions = ["happy", "sad", "angry", "calm", "anxious", "excited", "bored", "grateful", "tired", "content"]

    # Helper to generate random past date within last 60 days
    def random_date():
        days_ago = random.randint(0, 60)
        return date.today() - timedelta(days=days_ago)

    entries = []

    for _ in range(40):
        sentiment = random.choice(sentiments)
        emotion = random.choice(emotions)
        
        sentiment_score = round(random.uniform(0.2, 1.0), 2)
        emotion_score = round(random.uniform(0.2, 1.0), 2)

        entry = JournalEntry(
            date=random_date(),
            text=fake.sentence(nb_words=12),
            sentiment=sentiment,
            emotion=emotion,
            sentiment_score=sentiment_score,
            emotion_score=emotion_score,
            ai_feedback=fake.sentence(nb_words=8),
            model_result_justification=f"Detected {sentiment} and {emotion}.",
        )
        entries.append(entry)

    # Bulk create for efficiency
    JournalEntry.objects.bulk_create(entries)

    print(f"\n\n ✅ Successfully inserted {len(entries)} fake JournalEntry rows.")


def update_journal_entry_dates():
    def random_date(start_date, end_date):
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return start_date + timedelta(days=random_days)

    start = date(2025, 1, 1)
    end = date(2025, 12, 31)

    entries = JournalEntry.objects.all()
    updated = 0
    for entry in entries:
        entry.date = random_date(start, end)
        updated += 1
        entry.save()
    
    
    print('\n\n ========== updated: ', updated)
