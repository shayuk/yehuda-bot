import streamlit as st
from openai import OpenAI

# פרופיל החולה
patient_profile = """
שמי יהודה לוי. אני סובל מאובדן שמיעה חמור באוזן שמאל, ויש לי רעש מציק שם כל הזמן.
קשה לי להבין אנשים, במיוחד כשיש רעש ברקע.
לפעמים אני מרגיש סחרחורת, והפנים בצד שמאל לא זזות כמו פעם.
קשה לי לאכול, לחייך, לדבר רגיל.
אני מרגיש די מדוכא. לא חזרתי לעבודה ומרגיש שאני נטל על אשתי והילדים.
אין לי מחלות רקע ולא לוקח תרופות.
"""

# הנחיות לבוט
system_prompt = """
אתה משחק את יהודה לוי, חולה שמדבר עם סטודנט לרפואה.
ענה רק על השאלות שנשאלת, בשפה פשוטה ועממית.
אל תחשוף מידע נוסף אם לא נשאל.
אל תסטה מהנושא הרפואי, והתנהג באופן טבעי.
"""

# יצירת קליינט OpenAI חדש
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ממשק המשתמש
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: right;'>סימולציית ראיון עם יהודה לוי</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: right;'>שאל את יהודה כל שאלה שתרצה, כמו רופא בסטאז'. (הקלד 'סיום' לסיום השיחה)</div>", unsafe_allow_html=True)

# זיכרון שיחה
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "שלום יהודה, מה שלומך?"},
        {"role": "assistant", "content": "לא משהו... האוזן שלי עושה לי הרבה בעיות."}
    ]

# תצוגת השיחה מימין לשמאל
for msg in st.session_state.chat_history[1:]:
    if msg["role"] == "user":
        st.markdown(f"<div style='text-align: right;'><b>סטודנט:</b> {msg['content']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"<div style='text-align: right;'><b>יהודה:</b> {msg['content']}</div>", unsafe_allow_html=True)

# פונקציה ליצירת משוב בסיום השיחה
def generate_feedback(chat_history):
    feedback_prompt = f"""
    לפניך שיחה בין סטודנט לרפואה למטופל יהודה לוי.
    תן משוב קצר לסטודנט על איכות השאלות, האבחון, ההתייחסות לבעיה, ונקודות לשיפור.
    השיחה:
    {chat_history}
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": feedback_prompt}]
    )
    return response.choices[0].message.content

# קלט משתמש
question = st.text_input("מה תרצה לשאול את יהודה?", key="input", placeholder="הקלד שאלה כאן...")

if question:
    if question.strip() == "סיום":
        st.markdown("<div style='text-align: right;'>השיחה הסתיימה. מייצר משוב...</div>", unsafe_allow_html=True)
        feedback = generate_feedback(st.session_state.chat_history)
        st.markdown("<div style='text-align: right;'><b>משוב:</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: right;'>{feedback}</div>", unsafe_allow_html=True)
    else:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.spinner("יהודה חושב..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.chat_history
            )
            answer = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.experimental_rerun()
