import streamlit as st
import openai

# --- הגדרת הפרופיל של החולה ---
patient_profile = """
שמי יהודה לוי. אני סובל מאובדן שמיעה חמור באוזן שמאל, ויש לי מין רעש מציק שם כל הזמן. קשה לי להבין אנשים, במיוחד כשיש רעש ברקע. לפעמים אני גם מרגיש סחרחורת, וגם הפנים בצד שמאל לא ממש זזות כמו פעם. קשה לי לאכול, לחייך, לדבר רגיל.
מאז שזה התחיל, אני מרגיש די מרוסק. לא חזרתי לעבודה, מרגיש שאני מעמסה על אשתי והילדים. אין לי מחלות רקע, ולא לוקח תרופות.
"""


# --- הגדרת ההנחיות לבוט ---
system_prompt = """
אתה משחק את יהודה לוי, חולה שמדבר עם סטודנט לרפואה. אתה עונה רק למה שנשאל, בשפה פשוטה ולא מקצועית. אין לחשוף מידע נוסף אם לא נשאל. אל תסטה מהנושא הרפואי.
"""


# --- הגדרת מפתח OpenAI ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- ממשק משתמש ---
st.title("סימולציית ראיון עם יהודה לוי")
st.write("שאל את יהודה כל שאלה שתרצה, כמו רופא בסטאז'.")

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
        st.markdown(f"**סטודנט:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**יהודה:** {msg['content']}")
        
# --- שאלה חדשה ---
question = st.text_input("מה תשאל את יהודה?")

if question:
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.spinner("יהודה חושב..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.chat_history
        )
        answer = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.experimental_rerun()
