import json_repair
from ..utils.llm import create_chat_completion
from gpt_researcher.prompts.prompts import generate_search_queries_prompt
from typing import Any, List, Dict
from ..config import Config
import logging

logger = logging.getLogger(__name__)

async def get_search_results(query: str, retriever: Any) -> List[Dict[str, Any]]:
    """
    Get web search results for a given query.
    
    Args:
        query: The search query
        retriever: The retriever instance
    
    Returns:
        A list of search results
    """
    search_retriever = retriever(query)
    return search_retriever.search()

async def generate_sub_queries(
    query: str,
    type: str,
    context: List[Dict[str, Any]],
    cfg: Config,
    cost_callback: callable = None
) -> List[str]:
    """
    Generate sub-queries using the specified LLM model.
    
    Args:
        query: The original query
        parent_query: The parent query
        report_type: The type of report
        max_iterations: Maximum number of research iterations
        context: Search results context
        cfg: Configuration object
        cost_callback: Callback for cost calculation
    
    Returns:
        A list of sub-queries
    """
    gen_queries_prompt = generate_search_queries_prompt(
        query,
        type,
        max_iterations=cfg.max_iterations or 1,
        context=context
        # context=[]
    )

    print("gen_queries_prompt", gen_queries_prompt)
    # print(c)
    if not gen_queries_prompt:
        return []
    try:
        response = await create_chat_completion(
            model=cfg.strategic_llm_model,
            messages=[{"role": "user", "content": gen_queries_prompt}],
            temperature=1,
            llm_provider=cfg.strategic_llm_provider,
            max_tokens=None,
            llm_kwargs=cfg.llm_kwargs,
            cost_callback=cost_callback,
        )
    except Exception as e:
        logger.warning(f"Error with strategic LLM: {e}. Falling back to smart LLM.")
        response = await create_chat_completion(
            model=cfg.smart_llm_model,
            messages=[{"role": "user", "content": gen_queries_prompt}],
            temperature=cfg.temperature,
            max_tokens=cfg.smart_token_limit,
            llm_provider=cfg.smart_llm_provider,
            llm_kwargs=cfg.llm_kwargs,
            cost_callback=cost_callback,
        )

    print("gen_queries_prompt response", response)
    # print(c)

    return json_repair.loads(response)

async def plan_research_outline(
    query: str,
    search_results: List[Dict[str, Any]],
    cfg: Config,
    type: str = 'query',
    cost_callback: callable = None,
) -> List[str]:
    """
    Plan the research outline by generating sub-queries.
    
    Args:
        query: Original query
        retriever: Retriever instance
        agent_role_prompt: Agent role prompt
        cfg: Configuration object
        report_type: Report type
        cost_callback: Callback for cost calculation
    
    Returns:
        A list of sub-queries
    """
    
    sub_queries = await generate_sub_queries(
        query,
        type,
        search_results,
        cfg,
        cost_callback
    )

    return sub_queries