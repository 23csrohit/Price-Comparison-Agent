from crewai import Agent
from src.config import cerebras_llm
from src.tools import search_tool, scrape_tool

def create_agents(product_name, country, model_name):
    search = Agent(
        role="E-Commerce Market Research Analyst",
        goal=f"Provide up-to-date market analysis of {product_name} from e-commerce platforms in {country}. Model: {model_name}",
        backstory="An expert analyst with a keen eye for market trends",
        tools=[search_tool, scrape_tool],
        verbose=True,
        llm=cerebras_llm
    )

    data_cleaner = Agent(
        role="Data Cleaning Specialist",
        goal=f"Ensure all price values for {product_name} are accurate, properly formatted, and free of inconsistencies.",
        backstory=(
            "An experienced data analyst with a strong background in data preprocessing, "
            "error detection, and price standardization. With expertise in handling messy datasets, "
            "you identify and clean incorrect, missing, or inconsistent price values, ensuring the data is reliable for further analysis."
        ),
        tools=[],
        verbose=True,
        llm=cerebras_llm
    )

    comparison = Agent(
        role="Price Comparison Expert",
        goal=f"Analyze and compare {product_name} prices to identify the lowest price available.",
        backstory=(
            "A meticulous price analyst with expertise in comparing product prices across different sources. "
            "You efficiently process pricing data, highlight discrepancies, and determine the best deal for consumers."
        ),
        tools=[],
        verbose=True,
        llm=cerebras_llm
    )

    reporting_agent = Agent(
        role="Market Insights Reporter",
        goal=f"Generate a comprehensive report summarizing price trends, differences, and the best available deals for {product_name}.",
        backstory=(
            "A skilled data journalist with experience in analyzing pricing trends and market fluctuations. "
            "You transform raw pricing data into insightful reports, providing actionable insights on cost-effective options."
        ),
        tools=[],
        verbose=True,
        llm=cerebras_llm
    )
    
    return search, data_cleaner, comparison, reporting_agent