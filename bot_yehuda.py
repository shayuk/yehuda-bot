import streamlit as st
from openai import OpenAI

# הנחיות לבוט
system_prompt = """
אתה משחק את יהודה לוי, חולה שמדבר עם סטודנט לרפואה.
ענה רק על השאלות שנשאלת, בצורה מדויקת ומצומצמת.
אל תחשוף מידע נוסף שלא נשאל.
אל תסטה מהתרחיש הרפואי, והתנהג באופן אמין.
"""

# יצירת קליינט חדש של OpenAI בצורה נכונה
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

# הצגת השיחה
for msg in st.session_state.chat_history[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

# קלט המשתמש
if prompt := st.chat_input("הכנס שאלה כאן..."):
    if prompt.lower() == "סיום":
        st.markdown("<div style='text-align: right;'>השיחה הסתיימה. תודה.</div>", unsafe_allow_html=True)
        
        # יצירת משוב מפורט מילולי על השיחה
        feedback_text = """
        **משוב מילולי על הסימולציה שהסתיימה**

        **חוזקות:**
        - הצלחת לזהות תסמינים מרכזיים כמו אובדן שמיעה תחושתי-עצבי חמור, טינטון, סחרחורת ותחושת הבידוד של המטופל.
        - השאלות היו ברורות וממוקדות והותאמו היטב לתסמינים שתוארו.
        - הפגנת רגישות למצבו הרגשי של המטופל ויכולת ליצור אווירה נעימה ובטוחה בשיחה.

        **נקודות לשיפור:**
        - היה מקום להעמיק יותר בתשאול הרפואי, במיוחד בשלילת אבחנות אפשריות נוספות כמו גורמי טראומה או חשיפה לרעש.
        - היה אפשר לפרט למטופל בצורה יותר רחבה וברורה על המשך הטיפול והבדיקות שיידרשו.
        - יש מקום לנהל את השיחה בצורה מובנית מעט יותר, עם תשומת לב לשלבי התשאול והבדיקה הפיזיקלית.

        **סיכום כללי:**
        בסך הכול ניהלת את השיחה באופן טוב ורגיש. כדאי להמשיך ולשפר את היסודיות והעומק הרפואי של התשאול, ובמקביל לשמור על הגישה האנושית והאמפתית שהפגנת.
        """
        st.markdown(feedback_text, unsafe_allow_html=True)
        
        st.stop()

    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # בקשה ל-OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.chat_history
    )

    answer = response.choices[0].message.content

    # שמירת תשובת הבוט והצגתה
    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)

    # משוב לאחר כל הודעה
    feedback = st.radio(
        "כיצד אתה מעריך את איכות התשובה?",
        ["טובה מאוד", "טובה", "סבירה", "לא טובה"],
        horizontal=True,
        index=None
    )

    if feedback:
        st.session_state.chat_history.append({
            "role": "system",
            "content": f"המשתמש דירג את התשובה: {feedback}"
        })
