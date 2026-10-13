import json
from datetime import datetime, date, timedelta
from models import db, Lesson, LessonProgress, Vocabulary, Quiz, LearningActivity, Conversation, ChatMessage

def seed_user_initial_content(user, prefs):
    """Seeds starter educational records for a newly registered user tailored to their target language."""
    target_lang = prefs.target_language or "Spanish"
    level = prefs.proficiency_level or "Beginner"

    # Only seed if user has 0 lessons
    existing_lessons = Lesson.query.filter_by(user_id=user.id).count()
    if existing_lessons > 0:
        return

    # 1. Seed Starter Lessons
    lesson_1_content = {
        "title": f"Greetings and Everyday Etiquette in {target_lang}",
        "objectives": [
            f"Master essential formal and informal greetings in {target_lang}",
            "Introduce yourself with proper pronunciation",
            "Politely ask and answer 'How are you?'"
        ],
        "vocabulary": [
            {"word": "Hola", "translation": "Hello", "phonetic": "OH-lah", "example": "¡Hola! ¿Cómo estás hoy?"},
            {"word": "Buenos días", "translation": "Good morning", "phonetic": "BWEH-nohs DEE-ahs", "example": "Buenos días a todos en la clase."},
            {"word": "Por favor", "translation": "Please", "phonetic": "pohr fah-BOHR", "example": "¿Un café, por favor?"},
            {"word": "Muchas gracias", "translation": "Thank you very much", "phonetic": "MOO-chahs GRAH-syahs", "example": "Muchas gracias por tu ayuda."},
            {"word": "Mucho gusto", "translation": "Nice to meet you", "phonetic": "MOO-choh GOOS-toh", "example": "Me llamo Carlos, mucho gusto."}
        ],
        "grammar_explanation": f"### Politeness and Registers in {target_lang}\n\nIn many languages like {target_lang}, there is a clear distinction between **formal** and **informal** address.\n- Use informal greetings with close friends, classmates, and family.\n- Use formal address with elders, officials, or in formal business contexts.\n\nVowels in {target_lang} are pure and short, never diphthongized like in English.",
        "example_sentences": [
            {"target": "¡Hola! Me llamo María y soy estudiante.", "native": "Hello! My name is Maria and I am a student.", "note": "Standard personal intro."},
            {"target": "¿Cómo está usted? — Muy bien, gracias.", "native": "How are you (formal)? — Very well, thank you.", "note": "Respectful formal exchange."}
        ],
        "practical_exercises": [
            {"type": "fill_in", "instruction": "Complete the greeting", "question": "Buenos ___ (morning)", "answer": "días", "hint": "Starts with 'd'"},
            {"type": "translate", "instruction": "Translate into English", "question": "Mucho gusto en conocerte.", "answer": "Nice to meet you.", "hint": "Introductions phrase"}
        ],
        "assessment": [
            {
                "question": "Which phrase is the most appropriate when introduced to someone for the first time?",
                "options": ["Mucho gusto", "Buenas noches", "De nada", "Adiós"],
                "correct_index": 0,
                "explanation": "'Mucho gusto' translates to 'Pleasure to meet you'."
            }
        ],
        "summary": "Great job! You have mastered foundational greetings and polite conversational phrases."
    }

    l1 = Lesson(
        user_id=user.id,
        title=f"Lesson 1: Greetings & Introductions in {target_lang}",
        target_language=target_lang,
        proficiency_level=level,
        learning_objective="Conversational Basics",
        topic="Greetings & Courtesy",
        duration_minutes=15,
        content_json=json.dumps(lesson_1_content),
        is_custom=False
    )
    db.session.add(l1)

    lesson_2_content = {
        "title": f"Numbers, Time, and Daily Routine in {target_lang}",
        "objectives": [
            f"Count from 1 to 20 with ease",
            "Express the time of day and schedule",
            "Talk about what time you wake up and study"
        ],
        "vocabulary": [
            {"word": "Uno, dos, tres", "translation": "One, two, three", "phonetic": "OO-noh, dohs, trehs", "example": "Tengo tres libros de idiomas."},
            {"word": "¿Qué hora es?", "translation": "What time is it?", "phonetic": "keh OH-rah ehs", "example": "Disculpe, ¿qué hora es?"},
            {"word": "La mañana", "translation": "The morning", "phonetic": "lah mah-NYAH-nah", "example": "Estudio por la mañana."},
            {"word": "La noche", "translation": "The night / evening", "phonetic": "lah NOH-cheh", "example": "Leo un libro por la noche."}
        ],
        "grammar_explanation": "Telling time usually relies on feminine articles ('la' for 1:00, 'las' for all other hours) because the implicit noun is 'la hora' (the hour).",
        "example_sentences": [
            {"target": "Son las ocho de la mañana.", "native": "It is eight o'clock in the morning.", "note": "Plural hours use 'Son las...'."},
            {"target": "Es la una de la tarde.", "native": "It is one o'clock in the afternoon.", "note": "Singular hour uses 'Es la...'."}
        ],
        "practical_exercises": [
            {"type": "fill_in", "instruction": "Complete the time phrase", "question": "___ las tres de la tarde.", "answer": "Son", "hint": "Plural form of verb 'ser'"}
        ],
        "assessment": [
            {
                "question": "How do you say 'It is one o'clock'?",
                "options": ["Es la una", "Son las una", "Es los uno", "Son los una"],
                "correct_index": 0,
                "explanation": "1:00 is singular, so we say 'Es la una'."
            }
        ],
        "summary": "You can now read numbers and communicate the time in conversation!"
    }

    l2 = Lesson(
        user_id=user.id,
        title=f"Lesson 2: Numbers & Telling Time in {target_lang}",
        target_language=target_lang,
        proficiency_level=level,
        learning_objective="Daily Scheduling",
        topic="Numbers & Routine",
        duration_minutes=20,
        content_json=json.dumps(lesson_2_content),
        is_custom=False
    )
    db.session.add(l2)
    db.session.commit()

    # 2. Seed Starter Vocabulary
    starter_words = [
        {"word": "El amigo / La amiga", "translation": "Friend", "definition": "A person whom one knows and with whom one has a bond of mutual affection.", "pronunciation": "ehl ah-MEE-goh", "example": "Mi amigo aprende idiomas conmigo.", "part_of_speech": "Noun", "difficulty": "easy"},
        {"word": "Aprender", "translation": "To learn", "definition": "To acquire knowledge of or skill in something through study.", "pronunciation": "ah-prehn-DEHR", "example": "Quiero aprender a hablar con fluidez.", "part_of_speech": "Verb", "difficulty": "easy"},
        {"word": "El libro", "translation": "Book", "definition": "A written or printed work consisting of pages glued or sewn together.", "pronunciation": "ehl LEE-broh", "example": "Este libro de gramática es muy claro.", "part_of_speech": "Noun", "difficulty": "easy"},
        {"word": "La pregunta", "translation": "Question", "definition": "A sentence worded or expressed so as to elicit information.", "pronunciation": "lah preh-GOON-tah", "example": "Tengo una pregunta para el tutor.", "part_of_speech": "Noun", "difficulty": "medium"},
        {"word": "Entender", "translation": "To understand", "definition": "To perceive the intended meaning of words or ideas.", "pronunciation": "ehn-tehn-DEHR", "example": "Entiendo las explicaciones del tutor.", "part_of_speech": "Verb", "difficulty": "medium"},
        {"word": "La conversación", "translation": "Conversation", "definition": "A talk between two or more people in which thoughts are shared.", "pronunciation": "lah kohn-behr-sah-SYOHN", "example": "Disfruto cada conversación en clase.", "part_of_speech": "Noun", "difficulty": "medium"}
    ]

    for item in starter_words:
        v = Vocabulary(
            user_id=user.id,
            word=item["word"],
            target_language=target_lang,
            translation=item["translation"],
            definition=item["definition"],
            pronunciation=item["pronunciation"],
            example_sentence=item["example"],
            part_of_speech=item["part_of_speech"],
            difficulty=item["difficulty"],
            status="learning",
            box=1,
            next_review_date=date.today()
        )
        db.session.add(v)

    # 3. Seed Starter Quiz
    quiz_questions = [
        {
            "id": 1,
            "type": "multiple_choice",
            "question": f"Which greeting is used when meeting someone in the morning in {target_lang}?",
            "options": ["Buenos días", "Buenas tardes", "Buenas noches", "Hasta mañana"],
            "correct_answer": "Buenos días",
            "explanation": "'Buenos días' is the proper greeting used until mid-day.",
            "hint": "Good day / morning"
        },
        {
            "id": 2,
            "type": "fill_in_blank",
            "question": "Mucho ___ (Pleasure to meet you).",
            "options": ["gusto", "tiempo", "amigo", "libro"],
            "correct_answer": "gusto",
            "explanation": "'Mucho gusto' is standard polite etiquette.",
            "hint": "Means pleasure"
        },
        {
            "id": 3,
            "type": "multiple_choice",
            "question": "What is the translation of the verb 'Aprender'?",
            "options": ["To learn", "To teach", "To listen", "To write"],
            "correct_answer": "To learn",
            "explanation": "'Aprender' directly means to acquire knowledge (to learn).",
            "hint": "Think of apprentice"
        },
        {
            "id": 4,
            "type": "multiple_choice",
            "question": "¿Qué hora es a las 13:00?",
            "options": ["Es la una de la tarde", "Son las dos", "Son las una", "Es las tres"],
            "correct_answer": "Es la una de la tarde",
            "explanation": "One o'clock is singular ('Es la una').",
            "hint": "Singular hour"
        }
    ]

    q = Quiz(
        user_id=user.id,
        title=f"Diagnostic Quiz: Foundations of {target_lang}",
        target_language=target_lang,
        proficiency_level=level,
        topic="Foundations & Etiquette",
        questions_json=json.dumps(quiz_questions)
    )
    db.session.add(q)

    # 4. Create an Initial Conversation Session
    conv = Conversation(
        user_id=user.id,
        title=f"Welcome Chat with LinguaAI ({target_lang})",
        target_language=target_lang
    )
    db.session.add(conv)
    db.session.flush()

    welcome_ai_msg = ChatMessage(
        conversation_id=conv.id,
        sender="ai",
        message=f"¡Hola {user.username}! Welcome to your personalized language learning journey. I am your LinguaAI Tutor for {target_lang}. Whenever you're ready, say hello or ask me any question in {target_lang} or English!",
        corrections_json=json.dumps({
            "has_corrections": False,
            "corrections": None,
            "improved_version": "¡Hola! Estoy listo para aprender.",
            "pronunciation_tip": "Remember to pronounce vowels clearly and rhythmically.",
            "vocabulary_spotlight": [
                {"word": "listo/a", "meaning": "ready", "example": "Estoy listo para practicar."}
            ],
            "encouragement": "Welcome aboard! Let's reach your fluency goals together."
        })
    )
    db.session.add(welcome_ai_msg)

    # 5. Seed an initial onboarding activity
    act = LearningActivity(
        user_id=user.id,
        activity_type="conversation",
        title=f"Onboarded & Initialized {target_lang} Journey",
        target_language=target_lang,
        duration_minutes=5,
        score=100.0,
        status="completed",
        timestamp=datetime.utcnow() - timedelta(minutes=10),
        details=f"Configured learning goal ({prefs.learning_goal}) and daily target ({prefs.daily_target_minutes} mins)."
    )
    db.session.add(act)

    db.session.commit()
