
import streamlit as st
from groq import (
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
    APIStatusError,
    BadRequestError,
    GroqError
)
from roadmap import generate_roadmap

st.set_page_config(
    page_title="AI Learning Roadmap Generator",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 AI Learning Roadmap Generator")
st.write(
    "Build your personalized learning plan with AI."
)

st.divider()

field = st.text_input(
    "What do you want to learn?",
    placeholder="e.g. Cybersecurity, Python, Web Development"
)

level = st.selectbox(
    "Choose your skill level",
    ["Beginner", "Intermediate", "Advanced"]
)

weeks = st.number_input(
    "How many weeks do you have?",
    min_value=1,
    max_value=104,
    value=8
)

hours = st.number_input(
    "Available study hours per week",
    min_value=1,
    max_value=80,
    value=5
)


def get_api_key():
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
        if key:
            return key
    except Exception:
        pass

    import os
    return os.environ.get("GROQ_API_KEY", "")


if st.button("Generate My Roadmap", type="primary"):

    if not field.strip():
        st.warning("Please enter a learning field.")

    else:
        api_key = get_api_key()

        if not api_key:
            st.error(
                "API key not found. Add GROQ_API_KEY "
                "in your Streamlit app Secrets settings."
            )

        else:
            try:
                with st.spinner(
                    "AI is preparing your roadmap..."
                ):
                    roadmap = generate_roadmap(
                        field.strip(),
                        level,
                        int(weeks),
                        int(hours),
                        api_key
                    )

                st.success("Your roadmap is ready!")
                st.markdown(roadmap)

                st.download_button(
                    label="Download Your Roadmap",
                    data=roadmap,
                    file_name="learning_roadmap.md",
                    mime="text/markdown"
                )

            except AuthenticationError:
                st.error(
                    "Groq rejected the API key. "
                    "Check your key in Streamlit Secrets."
                )

            except RateLimitError:
                st.error(
                    "Groq API rate limit or quota reached. "
                    "Check your Groq Console."
                )

            except APIConnectionError:
                st.error(
                    "Could not connect to Groq. "
                    "Try again later."
                )

            except BadRequestError as e:
                st.error(
                    "Groq rejected the request. "
                    "Check the model and request settings."
                )
                st.caption(f"Details: {e}")

            except APIStatusError as e:
                st.error(
                    f"Groq API error: HTTP {e.status_code}"
                )
                st.caption(str(e))

            except GroqError as e:
                st.error("A Groq API error occurred.")
                st.caption(str(e))
                import streamlit as st

try:
    key = st.secrets.get("GROQ_API_KEY", "")
    st.write("Secret found:", bool(key))
    st.write("Key has surrounding spaces:", key != key.strip())
    st.write("Key length:", len(key))
except Exception as e:
    st.error(f"Secrets configuration error: {type(e).__name__}")

            except Exception as e:
                st.error(
                    "An unexpected error occurred. "
                    "Check your app logs."
                )
                st.caption(
                    f"{type(e).__name__}: {e}"
                )
