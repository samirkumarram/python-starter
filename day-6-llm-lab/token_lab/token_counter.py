import tiktoken
encoding = tiktoken.get_encoding("cl100k_base")
texts = {
    "English Prose": "Artificial intelligence is transforming the way businesses operate.",

    "Python Code": """
        def add_numbers(a, b):
            result = a + b
            return result
        """,

        "JSON": """
        {
            "name": "Samir",
            "role": "AI Engineer",
            "experience": 3
        }
        """,

    "English": "Machine learning helps computers learn from data.",

    "Hindi": "कृत्रिम बुद्धिमत्ता तकनीक की दुनिया को बदल रही है।",

    "Bengali": "কৃত্রিম বুদ্ধিমত্তা প্রযুক্তির জগৎ পরিবর্তন করছে।"
}

# Count tokens for each text
for text_type, text in texts.items():
    tokens = encoding.encode(text)

    print(f"{text_type}: {len(tokens)} tokens")
