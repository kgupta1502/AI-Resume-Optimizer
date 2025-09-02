import requests
import os
import streamlit as st

API_KEY = st.secrets["OPENAI_API_KEY"]
model =st.secrets.get("MODEL_NAME", "openai/gpt-3.5-turbo")


def call_openrouter(prompt, model="openai/gpt-3.5-turbo"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Resume Optimizer"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert career coach and ATS resume optimizer."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    try:
        response.raise_for_status()
        response_json = response.json()

        if "choices" not in response_json:
            return f"Error: 'choices' not found. Message: {response_json.get('error', 'Unknown error')}"

        return response_json["choices"][0]["message"]["content"]

    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e}\nResponse: {response.text}"
    except Exception as e:
        return f"Unexpected Error: {e}"
