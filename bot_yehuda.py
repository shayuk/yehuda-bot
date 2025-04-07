import streamlit as st
import openai

# --- הגדרת הפרופיל של החולה ---
patient_profile = """
שמי יהודה לוי. אני סובל מאובדן שמיעה חמור באוזן שמאל, ויש לי מין רעש מציק שם כל הזמן.
קשה לי להבין אנשים, במיוחד כשיש רעש ברקע.
לפעמים אני גם מרגיש סחרחורת, וגם הפנים בצד שמאל לא ממש זזות כמו פעם.
קשה לי לאכול, לחייך, לדבר רגיל.
מאז שזה התחיל, אני מרגיש די מרוסק. לא חזרתי לעבודה, מרגיש שאני מעמסה על אשתי והילדים.
אין לי מחלות רקע, ולא לוקח תרופות.
"""

# --- הגדרת ההנחיות לבוט ---
system_prompt = """
אתה משחק את יהודה לוי, חולה שמדבר עם סטודנט לרפואה.
ענה רק למה שנשאל, בשפה פשוטה ולא מקצועית.
אל תחשוף מידע נוסף אם לא נשאל.
אל תסטה מהנושא הרפואי, והתנהג באופן טבעי.
"""

openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- ממשק משתמש ---
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: right;'>סימולציית ראיון עם יהודה לוי</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: right;'>שאל את יהודה כל שאלה שתרצה, כמו רופא בסטאז'. (הקלד 'סיום' לסיום השיחה)</div>", unsafe_allow_html=True)

# --- זיכרון שיחה ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "שלום יהודה, מה שלומך?"},
        {"role": "assistant", "content": "לא כל כך משהו אם להיות כן... האוזן שלי עושה לי צרות."}
    ]

# --- תצוגת שיחה ---
for msg in st.session_state.chat_history[1:]:
    if msg["role"] == "user":
        st.markdown(f"<div style='text-align: right;'><b>סטודנט:</b> {msg['content']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"<div style='text-align: right;'><b>יהודה:</b> {msg['content']}</div>", unsafe_allow_html=True)

# --- פונקציה ליצירת משוב ---
def generate_feedback(chat_history):
    feedback_prompt = f"""
    לפניך שיחה בין סטודנט לרפואה למטופל בשם יהודה לוי.
    תן משוב קצר לסטודנט על איכות השאלות, אבחון נכון, התייחסות מתאימה לבעיה של יהודה, ונקודות לשיפור.
    השיחה:
    {chat_history}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": feedback_prompt}]
    )
    return response.choices[0].message.content

# --- קלט משתמש (שאלות) ---
question = st.text_input("מה תרצה לשאול את יהודה?", key="input", placeholder="הקלד שאלה כאן...")

if question:
    if question.strip() == "סיום":
        st.markdown("<div style='text-align: right;'>השיחה הסתיימה. מייצר משוב עבורך...</div>", unsafe_allow_html=True)
        feedback = generate_feedback(st.session_state.chat_history)
        st.markdown("<div style='text-align: right;'><b>משוב:</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: right;'>{feedback}</div>", unsafe_allow_html=True)
    else:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.spinner("יהודה חושב..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=st.session_state.chat_history
            )
            answer = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.experimental_rerun()
