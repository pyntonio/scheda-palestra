import openai

# Inserisci qui la tua chiave API di OpenAI
api_key = ""
openai.api_key = api_key

def chat_with_gpt(prompt, model="gpt-3.5-turbo"):
    try:
        # Metodo corretto
        response = openai.ChatChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )

        # Estrazione della risposta
        message = response['choices'][0]['message']['content']
        return message.strip()

    except Exception as e:
        return f"Errore: {str(e)}"

if __name__ == "__main__":
    print("Benvenuto nella chat con GPT!")
    while True:
        try:
            user_input = input("Tu: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Chiusura della chat. A presto!")
                break

            risposta = chat_with_gpt(user_input)
            print(f"GPT: {risposta}")
        except KeyboardInterrupt:
            print("\nChiusura della chat. A presto!")
            break
