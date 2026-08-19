from agent import ask_agent


print("=" * 60)
print("🤖 PLEXIMUS AI ACTION AGENT")
print("=" * 60)

print("\nI can currently:")
print("  🧮 Calculate")
print("  🌤️  Check weather")
print("  🔤 Analyze/modify text")
print("\nType 'exit' to quit.\n")


while True:

    user_input = input("You: ").strip()

    if user_input.lower() in ["exit", "quit"]:
        print("\nAgent: Goodbye! 👋")
        break

    if not user_input:
        print("Agent: Please enter something.")
        continue

    try:

        answer = ask_agent(user_input)

        print(f"\nAgent: {answer}\n")

    except Exception as e:

        print(f"\n❌ Error: {e}\n")