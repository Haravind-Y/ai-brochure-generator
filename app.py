import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# Load environment variables
load_dotenv()

# Gemini Client
google_api_key = os.getenv("GOOGLE_API_KEY")

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

gemini = OpenAI(
    base_url=GEMINI_BASE_URL,
    api_key=google_api_key
)

# System Prompt
SYSTEM_MESSAGE = """
You are an assistant that analyzes the contents of a company website landing page
and creates a professional brochure for prospective customers, investors, and recruits.

Respond in markdown format.
"""

# Gemini Streaming Function
def stream_gemini(prompt):
    messages = [
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": prompt}
    ]

    stream = gemini.chat.completions.create(
        model="gemini-2.5-flash",
        messages=messages,
        stream=True
    )

    result = ""

    for chunk in stream:
        if chunk.choices[0].delta.content:
            result += chunk.choices[0].delta.content
            yield result

# Brochure Generator
def generate_brochure(company_name, url):

    prompt = f"""
    Create a professional company brochure.

    Company Name: {company_name}

    Website:
    {url}

    Include:
    - Company Overview
    - Products / Services
    - Key Strengths
    - Why Join the Company
    - Conclusion
    """

    yield from stream_gemini(prompt)

# Gradio UI
with gr.Blocks() as demo:

    gr.Markdown("# AI Brochure Generator")

    company_name = gr.Textbox(
        label="Company Name"
    )

    website_url = gr.Textbox(
        label="Website URL"
    )

    output = gr.Markdown()

    generate_btn = gr.Button("Generate Brochure")

    generate_btn.click(
        fn=generate_brochure,
        inputs=[company_name, website_url],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch()