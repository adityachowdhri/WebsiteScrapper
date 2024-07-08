import ollama
question = "What is your name"
response = ollama.generate(model='llama3', prompt=question)
print("The response is: ", response["response"])