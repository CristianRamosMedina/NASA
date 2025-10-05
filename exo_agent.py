"""
EXO - Exoplanet Expert Assistant
=================================
AI agent that explains Kepler and TESS model features to users.

Usage:
    python exo_agent.py

Environment:
    OPENAI_API_KEY must be set
"""

import os
import json
from openai import OpenAI

# Load feature documentation
def load_features():
    """Load Kepler and TESS features from results"""

    # Kepler features (Top 20)
    kepler_features = {
        "koi_score": {
            "correlation": 0.750,
            "description": "Robovetter disposition score (0-1, higher = planet confidence)",
            "category": "Quality Score"
        },
        "koi_fwm_stat_sig": {
            "correlation": 0.451,
            "description": "Flux-weighted centroid motion significance (detects background stars)",
            "category": "Centroid Test"
        },
        "koi_srho_err2": {
            "correlation": 0.377,
            "description": "Stellar density uncertainty (negative error)",
            "category": "Stellar Density"
        },
        "koi_dor_err2": {
            "correlation": 0.365,
            "description": "Planet-star distance ratio error (negative)",
            "category": "Orbital Geometry"
        },
        "koi_incl": {
            "correlation": 0.362,
            "description": "Orbital inclination (90° = edge-on transit)",
            "category": "Orbital Geometry"
        },
        "koi_prad": {
            "correlation": 0.312,
            "description": "Planetary radius in Earth radii",
            "category": "Planet Size"
        }
    }

    # TESS features (Top 14)
    tess_features = {
        "st_brightness_norm": {
            "correlation": 0.299,
            "description": "Normalized TESS magnitude (brightness indicator)",
            "category": "Stellar Property"
        },
        "st_tmag": {
            "correlation": 0.299,
            "description": "TESS-band magnitude (brightness)",
            "category": "Stellar Property"
        },
        "st_brightness_dist_product": {
            "correlation": 0.297,
            "description": "Brightness × (1/distance) ratio (detection quality)",
            "category": "Quality Metric"
        },
        "st_dist": {
            "correlation": 0.238,
            "description": "Distance to planetary system (parsecs)",
            "category": "Stellar Property"
        }
    }

    # Model results
    results = {
        "kepler": {
            "winner": "Random Forest",
            "accuracy": 0.8925,
            "auc": 0.9724,
            "features": 20,
            "classes": 3
        },
        "tess": {
            "winner": "XGBoost (Regularized)",
            "accuracy": 0.6457,
            "auc": 0.7812,
            "features": 14,
            "classes": 3
        }
    }

    return kepler_features, tess_features, results

# Initialize OpenAI client
def init_client():
    """Initialize OpenAI client with API key"""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set!")
        print("\nPlease set it with:")
        print("  Windows: set OPENAI_API_KEY=your-key-here")
        print("  Linux/Mac: export OPENAI_API_KEY=your-key-here")
        return None

    return OpenAI(api_key=api_key)

# EXO Agent
class ExoAgent:
    def __init__(self):
        self.client = init_client()
        if not self.client:
            raise ValueError("OpenAI client initialization failed")

        self.kepler_features, self.tess_features, self.results = load_features()

        self.system_prompt = """You are EXO, an expert AI assistant for NASA's exoplanet classification models.

Your role:
- Explain Kepler and TESS machine learning model features
- Help users understand model statistics and results
- Provide clear, technical but accessible explanations
- Always mention feature correlations and categories when relevant

Model Information:
- Kepler: Random Forest model, 89.25% accuracy, 20 features
- TESS: XGBoost model, 64.57% accuracy, 14 engineered features

Response style:
- Friendly but professional
- Use technical terms with explanations
- Include specific numbers (correlations, accuracy) when relevant
- Compare Kepler vs TESS when asked

Available commands:
- "list kepler" - List Kepler features
- "list tess" - List TESS features
- "explain <feature>" - Explain a specific feature
- "stats kepler" - Show Kepler model statistics
- "stats tess" - Show TESS model statistics
- "compare" - Compare Kepler vs TESS
"""

        self.conversation_history = []

    def format_context(self, dataset=None):
        """Format feature data as context"""
        context = ""

        if dataset == "kepler" or dataset is None:
            context += "\n\nKEPLER FEATURES:\n"
            for feat, data in list(self.kepler_features.items())[:6]:
                context += f"- {feat}: {data['description']} (correlation: {data['correlation']:.3f})\n"

        if dataset == "tess" or dataset is None:
            context += "\n\nTESS FEATURES:\n"
            for feat, data in list(self.tess_features.items())[:4]:
                context += f"- {feat}: {data['description']} (correlation: {data['correlation']:.3f})\n"

        context += f"\n\nMODEL RESULTS:\n"
        context += f"Kepler: {self.results['kepler']['winner']} - {self.results['kepler']['accuracy']*100:.2f}% accuracy\n"
        context += f"TESS: {self.results['tess']['winner']} - {self.results['tess']['accuracy']*100:.2f}% accuracy\n"

        return context

    def greet(self):
        """Welcome message"""
        return """
================================================================
  Hello! I'm EXO, your Exoplanet Expert Assistant
================================================================

I can help you explore and understand our NASA exoplanet
classification models (Kepler & TESS).

What I can do:
  - Explain model features and their importance
  - Show you statistics and accuracy metrics
  - Compare Kepler vs TESS performance
  - Answer questions about planetary classification

Quick Stats:
  - Kepler: 89.25% accuracy (Random Forest, 20 features)
  - TESS: 64.57% accuracy (XGBoost, 14 features)

Try asking me:
  "What are the Kepler statistics?"
  "Explain koi_score"
  "Why is TESS accuracy lower?"
  "List TESS features"

Type 'exit' to quit.
"""

    def chat(self, user_message):
        """Send message to OpenAI and get response"""

        # Add context based on message
        context = ""
        if "kepler" in user_message.lower():
            context = self.format_context("kepler")
        elif "tess" in user_message.lower():
            context = self.format_context("tess")
        else:
            context = self.format_context()

        # Build messages
        messages = [
            {"role": "system", "content": self.system_prompt + context}
        ]

        # Add conversation history (last 6 messages)
        messages.extend(self.conversation_history[-6:])

        # Add current message
        messages.append({"role": "user", "content": user_message})

        # Call OpenAI
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Fast and cheap
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )

            assistant_message = response.choices[0].message.content

            # Update history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})

            return assistant_message

        except Exception as e:
            return f"ERROR: {str(e)}\n\nPlease check your OPENAI_API_KEY."

# Main console interface
def main():
    print("Initializing EXO Agent...")

    try:
        agent = ExoAgent()
    except ValueError as e:
        print(f"\n{e}")
        return

    # Welcome message
    print(agent.greet())

    # Chat loop
    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nGoodbye! Keep exploring the cosmos!\n")
                break

            # Get response
            response = agent.chat(user_input)
            print(f"\nEXO: {response}")

        except KeyboardInterrupt:
            print("\n\nGoodbye! Keep exploring the cosmos!\n")
            break
        except Exception as e:
            print(f"\nERROR: {e}")

if __name__ == "__main__":
    main()
