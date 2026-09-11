"""
Interactive Terminal Test Script for AgriDrone Chatbot.
Run this script to simulate chat interactions directly in your terminal without LINE.
"""
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.dispatcher import dispatcher

def main():
    print("=" * 65)
    print("🌾 AgriDrone AI Chatbot - Interactive Terminal Tester 🌾")
    print("=" * 65)
    print("Simulates user inputs to test Rule Engine, RAG, Citations & Guardrails.")
    print("Type 'exit' or 'quit' to stop.\n")
    print("💡 Example questions to try:")
    print("  1. โดรนบินได้สูงกี่เมตรครับ (Rule: Drone Laws)")
    print("  2. อยากขึ้นทะเบียนโดรนต้องทำยังไง (Rule: Registration)")
    print("  3. เทคนิคการพ่นข้าวต้องใช้น้ำกี่ลิตรต่อไร่ (Rule: Rice Spraying)")
    print("  4. การฉีดพ่นมันสำปะหลังต้องบินสูงเท่าไรและระวังศัตรูพืชอะไร (RAG: Crops)")
    print("  5. แบตเตอรี่โดรนควรชาร์จอย่างไรให้ปลอดภัย (RAG: Maintenance)")
    print("  6. ขอสูตรทำส้มตำหน่อย (Guardrail: Out of scope)")
    print("-" * 65)

    while True:
        try:
            user_input = input("\n👤 User: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                print("Exiting tester. Goodbye!")
                break

            start_t = time.time()
            result = dispatcher.handle_text_message(
                user_id="terminal_test_user",
                reply_token="test_token",
                text=user_input
            )
            elapsed = round((time.time() - start_t) * 1000, 2)

            is_rule = result.get("is_rule_based", False)
            engine = "Rule Engine (Instant)" if is_rule else "RAG Pipeline (Knowledge Retrieval)"
            
            print(f"\n🤖 AgriDrone Bot [{engine}] (Latency: {elapsed} ms):")
            print(result.get("response"))

            citations = result.get("citations", [])
            if citations:
                print("\n📚 Grounded Citations:")
                for idx, c in enumerate(citations, 1):
                    url_str = f" -> {c['url']}" if c.get('url') else ""
                    print(f"   [{idx}] {c.get('source_name')} ({c.get('title')}){url_str}")

        except KeyboardInterrupt:
            print("\nExiting tester. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error during processing: {e}")

if __name__ == "__main__":
    main()
