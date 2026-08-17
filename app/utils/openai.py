def call_openai(client, messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=800,
    )
    return response.choices[0].message.content