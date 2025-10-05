from openai import OpenAI
import os, json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# features simuladas
features = [
    "koi_score","koi_fwm_stat_sig","koi_srho_err2","koi_dor_err2","koi_dor_err1",
    "koi_incl","koi_prad_err1","koi_count","koi_dor","koi_dikco_mdec_err",
    "koi_period_err1","koi_period_err2","koi_dikco_mra_err","koi_prad_err2",
    "koi_dikco_msky_err","koi_max_sngle_ev","koi_prad","koi_dicco_mdec_err",
    "koi_model_snr","koi_dicco_mra_err"
]

system_prompt = """Eres un asistente experto en exoplanetas.
Explica o analiza características del dataset Kepler.
Si te piden explicar una feature, responde con lenguaje claro y técnico.
"""

user_prompt = f"Describe brevemente las características más relevantes de las features: {', '.join(features)}"

response = client.responses.create(
    model="gpt-4.1-mini",  # rápido y barato
    input=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)

print(response.output_text)
