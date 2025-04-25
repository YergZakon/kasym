import streamlit as st
import random
from questions import all_questions

st.set_page_config(
    page_title="Тесты для 4 класса",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Функция для создания CSS
def local_css():
    st.markdown("""
    <style>
    .main {
        padding: 2rem;
        border-radius: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px;
        margin-top: 10px;
    }
    .correct-answer {
        color: green;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        background-color: #EAFFEA;
    }
    .wrong-answer {
        color: red;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        background-color: #FFEBEE;
    }
    .subject-btn {
        background-color: #F0F8FF;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s;
    }
    .subject-btn:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    .header {
        text-align: center;
        color: #3366CC;
        margin-bottom: 30px;
    }
    .final-score {
        font-size: 24px;
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        background-color: #E8F5E9;
    }
    .emoji-title {
        font-size: 48px;
        text-align: center;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    local_css()
    
    # Инициализация состояния сессии
    if 'current_subject' not in st.session_state:
        st.session_state.current_subject = None
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'current_question_idx' not in st.session_state:
        st.session_state.current_question_idx = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'answered' not in st.session_state:
        st.session_state.answered = False
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None
    if 'test_complete' not in st.session_state:
        st.session_state.test_complete = False
    if 'question_count' not in st.session_state:
        st.session_state.question_count = 10
    
    # Эмодзи для предметов
    subject_emoji = {
        "Математика": "🔢",
        "Русский язык": "🇷🇺",
        "Английский язык": "🇬🇧",
        "Казахский язык": "🇰🇿",
        "Познание мира": "🌍",
        "Литература": "📚"
    }
    
    # Главная страница
    st.markdown('<h1 class="header">Тесты для учеников 4 класса</h1>', unsafe_allow_html=True)
    
    if st.session_state.current_subject is None:
        st.markdown('<div class="emoji-title">📚✏️🎓</div>', unsafe_allow_html=True)
        st.write("### Привет! Выбери предмет для тестирования:")
        
        # Выбор количества вопросов перед началом теста
        st.session_state.question_count = st.slider(
            "Выбери количество вопросов:", 
            min_value=5, 
            max_value=20, 
            value=10,
            step=5
        )
        
        col1, col2 = st.columns(2)
        
        subjects_list = list(all_questions.keys())
        half_count = len(subjects_list) // 2
        
        with col1:
            for subject in subjects_list[:half_count]:
                if st.button(f"{subject_emoji[subject]} {subject}", key=subject):
                    st.session_state.current_subject = subject
                    st.session_state.questions = random.sample(
                        all_questions[subject], 
                        min(st.session_state.question_count, len(all_questions[subject]))
                    )
                    st.session_state.current_question_idx = 0
                    st.session_state.score = 0
                    st.session_state.answered = False
                    st.session_state.test_complete = False
                    st.experimental_rerun()
        
        with col2:
            for subject in subjects_list[half_count:]:
                if st.button(f"{subject_emoji[subject]} {subject}", key=subject):
                    st.session_state.current_subject = subject
                    st.session_state.questions = random.sample(
                        all_questions[subject], 
                        min(st.session_state.question_count, len(all_questions[subject]))
                    )
                    st.session_state.current_question_idx = 0
                    st.session_state.score = 0
                    st.session_state.answered = False
                    st.session_state.test_complete = False
                    st.experimental_rerun()
    else:
        # Страница тестирования
        st.markdown(f'<h2 class="header">{subject_emoji[st.session_state.current_subject]} {st.session_state.current_subject}</h2>', unsafe_allow_html=True)
        
        if not st.session_state.test_complete:
            # Отображение прогресса
            progress = st.progress((st.session_state.current_question_idx) / len(st.session_state.questions))
            st.write(f"Вопрос {st.session_state.current_question_idx + 1} из {len(st.session_state.questions)}")
            
            # Отображение текущего вопроса
            current_q = st.session_state.questions[st.session_state.current_question_idx]
            st.write(f"### {current_q['question']}")
            
            # Отображение вариантов ответа
            if not st.session_state.answered:
                for i, option in enumerate(current_q['options']):
                    if st.button(option, key=f"option_{i}"):
                        st.session_state.selected_option = option
                        st.session_state.answered = True
                        if option == current_q['correct_answer']:
                            st.session_state.score += 1
                        st.experimental_rerun()
            else:
                # Показать результаты ответа
                for option in current_q['options']:
                    if option == current_q['correct_answer']:
                        st.markdown(f'<div class="correct-answer">✅ {option}</div>', unsafe_allow_html=True)
                    elif option == st.session_state.selected_option and option != current_q['correct_answer']:
                        st.markdown(f'<div class="wrong-answer">❌ {option}</div>', unsafe_allow_html=True)
                    else:
                        st.write(option)
                
                # Кнопка для следующего вопроса
                if st.session_state.current_question_idx < len(st.session_state.questions) - 1:
                    if st.button("Следующий вопрос"):
                        st.session_state.current_question_idx += 1
                        st.session_state.answered = False
                        st.session_state.selected_option = None
                        st.experimental_rerun()
                else:
                    if st.button("Завершить тест"):
                        st.session_state.test_complete = True
                        st.experimental_rerun()
        else:
            # Отображение результатов теста
            percentage = (st.session_state.score / len(st.session_state.questions)) * 100
            st.markdown('<div class="emoji-title">🎉</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="final-score">Твой результат: {st.session_state.score} из {len(st.session_state.questions)} ({percentage:.1f}%)</div>', unsafe_allow_html=True)
            
            # Оценка результата
            if percentage >= 90:
                st.markdown('<div style="text-align: center; font-size: 24px; color: green;">Отлично! 👍</div>', unsafe_allow_html=True)
            elif percentage >= 70:
                st.markdown('<div style="text-align: center; font-size: 24px; color: blue;">Хорошо! 😊</div>', unsafe_allow_html=True)
            elif percentage >= 50:
                st.markdown('<div style="text-align: center; font-size: 24px; color: orange;">Неплохо! Можно лучше! 🙂</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align: center; font-size: 24px; color: red;">Надо больше учиться! 📚</div>', unsafe_allow_html=True)
            
            # Кнопки после завершения теста
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Вернуться на главную"):
                    st.session_state.current_subject = None
                    st.experimental_rerun()
            
            with col2:
                if st.button("Пройти тест еще раз"):
                    st.session_state.questions = random.sample(
                        all_questions[st.session_state.current_subject], 
                        min(st.session_state.question_count, len(all_questions[st.session_state.current_subject]))
                    )
                    st.session_state.current_question_idx = 0
                    st.session_state.score = 0
                    st.session_state.answered = False
                    st.session_state.test_complete = False
                    st.experimental_rerun()

if __name__ == "__main__":
    main() 