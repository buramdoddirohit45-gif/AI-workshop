import json
from datetime import datetime, date, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bio = db.Column(db.String(250), default="Passionate language learner on LinguaAI.")

    # Relationships
    preferences = db.relationship('UserPreferences', backref='user', uselist=False, cascade='all, delete-orphan')
    lessons = db.relationship('Lesson', backref='creator', lazy='dynamic')
    lesson_progresses = db.relationship('LessonProgress', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    conversations = db.relationship('Conversation', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    vocabularies = db.relationship('Vocabulary', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    quiz_attempts = db.relationship('QuizAttempt', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    activities = db.relationship('LearningActivity', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    mistakes = db.relationship('MistakeTracker', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_or_create_preferences(self):
        if not self.preferences:
            pref = UserPreferences(user_id=self.id)
            db.session.add(pref)
            db.session.commit()
            return pref
        return self.preferences

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'bio': self.bio,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }


class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    target_language = db.Column(db.String(50), default='Spanish')
    native_language = db.Column(db.String(50), default='English')
    proficiency_level = db.Column(db.String(30), default='Beginner')  # Beginner, Intermediate, Advanced
    learning_goal = db.Column(db.String(50), default='Speaking')     # Speaking, Grammar, Vocabulary, Reading, Writing, Exam Preparation
    daily_target_minutes = db.Column(db.Integer, default=20)
    preferred_style = db.Column(db.String(50), default='Conversational practice')
    onboarding_completed = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'target_language': self.target_language,
            'native_language': self.native_language,
            'proficiency_level': self.proficiency_level,
            'learning_goal': self.learning_goal,
            'daily_target_minutes': self.daily_target_minutes,
            'preferred_style': self.preferred_style,
            'onboarding_completed': self.onboarding_completed
        }


class Lesson(db.Model):
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    target_language = db.Column(db.String(50), nullable=False)
    proficiency_level = db.Column(db.String(30), nullable=False)
    learning_objective = db.Column(db.String(100), default='General Fluency')
    topic = db.Column(db.String(100), nullable=False)
    duration_minutes = db.Column(db.Integer, default=15)
    content_json = db.Column(db.Text, nullable=False)  # JSON payload with objectives, grammar, vocab, exercises, assessment
    is_custom = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    progresses = db.relationship('LessonProgress', backref='lesson', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def content(self):
        try:
            return json.loads(self.content_json)
        except Exception:
            return {}

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'target_language': self.target_language,
            'proficiency_level': self.proficiency_level,
            'learning_objective': self.learning_objective,
            'topic': self.topic,
            'duration_minutes': self.duration_minutes,
            'content': self.content,
            'is_custom': self.is_custom,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }


class LessonProgress(db.Model):
    __tablename__ = 'lesson_progresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(30), default='completed')  # 'in_progress', 'completed'
    score = db.Column(db.Float, default=100.0)
    time_spent_minutes = db.Column(db.Integer, default=15)
    notes = db.Column(db.Text, nullable=True)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)


class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(150), default='New Chat Session')
    target_language = db.Column(db.String(50), default='Spanish')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = db.relationship('ChatMessage', backref='conversation', lazy='dynamic', cascade='all, delete-orphan', order_by='ChatMessage.created_at.asc()')


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False)
    sender = db.Column(db.String(10), nullable=False)  # 'user' or 'ai'
    message = db.Column(db.Text, nullable=False)
    corrections_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def feedback(self):
        if not self.corrections_json:
            return None
        try:
            return json.loads(self.corrections_json)
        except Exception:
            return None

    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'message': self.message,
            'feedback': self.feedback,
            'created_at': self.created_at.strftime('%H:%M')
        }


class Vocabulary(db.Model):
    __tablename__ = 'vocabularies'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    word = db.Column(db.String(100), nullable=False)
    target_language = db.Column(db.String(50), nullable=False)
    translation = db.Column(db.String(200), nullable=False)
    definition = db.Column(db.Text, nullable=True)
    pronunciation = db.Column(db.String(100), nullable=True)
    example_sentence = db.Column(db.Text, nullable=True)
    part_of_speech = db.Column(db.String(50), default='Noun')
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    status = db.Column(db.String(20), default='learning')    # learning, mastered
    box = db.Column(db.Integer, default=1)                   # Leitner box 1 to 5
    next_review_date = db.Column(db.Date, default=date.today)
    last_reviewed_at = db.Column(db.DateTime, nullable=True)
    review_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'word': self.word,
            'target_language': self.target_language,
            'translation': self.translation,
            'definition': self.definition or '',
            'pronunciation': self.pronunciation or '',
            'example_sentence': self.example_sentence or '',
            'part_of_speech': self.part_of_speech or 'Word',
            'difficulty': self.difficulty,
            'status': self.status,
            'box': self.box,
            'next_review_date': self.next_review_date.strftime('%Y-%m-%d') if self.next_review_date else '',
            'review_count': self.review_count
        }


class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    target_language = db.Column(db.String(50), nullable=False)
    proficiency_level = db.Column(db.String(30), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    questions_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    attempts = db.relationship('QuizAttempt', backref='quiz', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def questions(self):
        try:
            return json.loads(self.questions_json)
        except Exception:
            return []

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'target_language': self.target_language,
            'proficiency_level': self.proficiency_level,
            'topic': self.topic,
            'question_count': len(self.questions),
            'questions': self.questions,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }


class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    answers_json = db.Column(db.Text, nullable=False)
    time_spent_minutes = db.Column(db.Integer, default=5)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def answers_breakdown(self):
        try:
            return json.loads(self.answers_json)
        except Exception:
            return []


class LearningActivity(db.Model):
    __tablename__ = 'learning_activities'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    activity_type = db.Column(db.String(30), nullable=False)  # lesson, quiz, conversation, vocabulary
    title = db.Column(db.String(200), nullable=False)
    target_language = db.Column(db.String(50), nullable=False)
    duration_minutes = db.Column(db.Integer, default=10)
    score = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(30), default='completed')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    details = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'activity_type': self.activity_type,
            'title': self.title,
            'target_language': self.target_language,
            'duration_minutes': self.duration_minutes,
            'score': self.score,
            'status': self.status,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M'),
            'date': self.timestamp.strftime('%b %d, %Y')
        }


class MistakeTracker(db.Model):
    __tablename__ = 'mistake_trackers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    target_language = db.Column(db.String(50), nullable=False)
    mistake_text = db.Column(db.String(255), nullable=False)
    correction = db.Column(db.String(255), nullable=False)
    mistake_type = db.Column(db.String(50), default='grammar')  # grammar, vocabulary, spelling, pronunciation
    explanation = db.Column(db.Text, nullable=True)
    count = db.Column(db.Integer, default=1)
    last_occurred_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'mistake_text': self.mistake_text,
            'correction': self.correction,
            'mistake_type': self.mistake_type,
            'explanation': self.explanation,
            'count': self.count,
            'last_occurred_at': self.last_occurred_at.strftime('%Y-%m-%d')
        }
