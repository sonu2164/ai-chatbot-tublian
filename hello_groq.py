import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def query_llm(prompt):
    detailed_prompt = (
        "Act as an expert AI tutor with extensive knowledge across a wide range of subjects. "
        "Answer the given question comprehensively, using clear and easy-to-understand language. "
        "Include detailed explanations, relevant examples, and structured information to ensure the answer is informative and well-organized. "
        "Format the answer with new line characters after approximately every 10-12 words to ensure the text is easily readable in a terminal interface. "
        "Do not include any introductory phrases like 'What a great question!' or 'Sure, I can help with that.' "
        "Focus solely on providing a high-quality answer. "
        "Question: {}\nAnswer:".format(prompt)
    )
    
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": detailed_prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    answer = response.choices[0].message.content.strip()  # Strip any leading/trailing whitespace
    lines = answer.split('\n')
    formatted_answer = '\n\n'  # Add spacing on top of response
    for line in lines:
        words = line.split()
        segments = []
        current_segment = '    '
        for word in words:
            if len(current_segment) + len(word) + 1 <= 150:  # Limiting to approximately 150 characters per line
                current_segment += word + ' '
            else:
                segments.append(current_segment.strip())
                current_segment = word + ' '
        segments.append(current_segment.strip())
        for segment in segments:
            formatted_answer += '  ' + segment + '\n'  # Add spacing at the beginning and end of each segment
    formatted_answer += '\n\n'  # Add spacing at the bottom of response
    return formatted_answer

def main():
    print("Ask a question (or type 'exit' to quit):")
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            break
        response = query_llm(user_input)
        print(response)
        print("\nAsk a question (or type 'exit' to quit):")

if __name__ == "__main__":
    main()
