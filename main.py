#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: abrarlaghari
"""
import openai

# Set up OpenAI API credentials
openai.api_key = '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'

# Define the chunk size and overlap
chunk_size = 2000  # Maximum token limit for GPT-3.5 is 4096
overlap = 100  # Number of tokens for overlapping context

def extract_dialogues_from_chapter(chapter_file):
    with open(chapter_file, 'r') as file:
        chapter_text = file.read()

    # Split the chapter into overlapping chunks
    chunks = []
    start = 0
    end = chunk_size
    while start < len(chapter_text):
        chunks.append(chapter_text[start:end])
        start = end - overlap
        end = start + chunk_size

    dialogues = []
    for chunk in chunks:
        # Construct the conversation with overlapping context
        conversation = [
            {'role': 'system', 'content': 'You are a character in a novel.'},
            {'role': 'user', 'content': chunk}
        ]

        # Call the OpenAI API to generate the response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            max_tokens=4096  # Adjust if using a different model with a different token limit
        )

        # Extract dialogues and metadata from the API response
        for message in response['choices'][0]['message']['content']:
            if message['role'] == 'system':
                continue  # Skip system messages
            dialogues.append((message['role'], message['content']))

    return dialogues

# Example usage
chapter_file = 'path/to/chapter.txt'  # Provide the path to the chapter file

dialogues = extract_dialogues_from_chapter(chapter_file)

# Print the extracted dialogues
for speaker, dialogue in dialogues:
    print(f"{speaker}: {dialogue}")


