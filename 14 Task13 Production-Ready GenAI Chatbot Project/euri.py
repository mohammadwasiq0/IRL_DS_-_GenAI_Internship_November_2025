from euriai import EuriaiClient

client = EuriaiClient(
    api_key="euri-......",
    model="gpt-4.1-nano"
)

response = client.generate_completion(
    prompt="Write a short poem about artificial intelligence.",
    temperature=0.7,
    max_tokens=1000
)

# print(response['choices']['message']) #['content'])
print(response["choices"][0]["message"]["content"])
