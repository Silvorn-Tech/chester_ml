import json
from loguru import logger
from src.utils.statements_loader import StatementsLoader
from src.engines.remote_engine import RemoteEngine
from src.engines.local_engine import LocalEngine


def execute_providers(providers, output_path=None):
    """
    Ejecuta uno o varios proveedores (sql, mongo, files, o all).
    Si se especifica output_path, guarda los resultados en un JSON.
    """
    loader = StatementsLoader()
    loader.load_statements()

    available_providers = {
        "sql": ("remote", "SQL"),
        "mongo": ("remote", "MONGO"),
        "files": ("local", "FILES")
    }

    if "all" in providers:
        providers = ["sql", "mongo", "files"]

    all_results = {}

    logger.info("───────────────────────────────")
    logger.info("🚀 Starting Chester ML Engine")
    logger.info("───────────────────────────────")

    for p in providers:
        context, provider = available_providers[p]
        statements = loader.remote_statements if context == "remote" else loader.local_statements
        provider_statements = statements.get(provider, {})

        if not provider_statements:
            logger.warning(f"⚠️ No statements found for {provider} in {context}.")
            continue

        engine = RemoteEngine() if context == "remote" else LocalEngine()
        logger.info(f"🗄️ Provider: {provider} ({context})")

        all_results[provider] = {}

        for name, statement in provider_statements.items():
            logger.info(f"▶️ Running statement: {name}")
            try:
                result = engine.execute(provider, statement)
                if result is not None:
                    logger.success(f"✅ Completed: {name}")
                    all_results[provider][name] = result
                else:
                    logger.warning(f"⚠️ No results for {name}")
            except Exception as e:
                logger.error(f"❌ Failed {name}: {e}")

        logger.info("───────────────────────────────")

    if output_path:
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(all_results, f, indent=4)
            logger.success(f"💾 Results saved to {output_path}")
        except Exception as e:
            logger.error(f"❌ Failed to save results: {e}")

    logger.info("🎯 Execution complete!")
