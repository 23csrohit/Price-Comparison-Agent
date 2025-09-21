from crewai import Task
from src.agents import create_agents

def create_tasks(product_name, country, model_name):
    # Get the agents
    search, data_cleaner, comparison, reporting_agent = create_agents(product_name, country, model_name)

    # Task definitions
    search_task = Task(
        description=f"Collect current pricing data for {product_name} from at least 3 major e-commerce platforms in {country}. Include product name, model, specifications, price, and any ongoing promotions or discounts.",
        expected_output=f"A structured dataset containing {product_name} information and pricing from multiple sources, with complete pricing details.",
        agent=search
    )

    cleaning_task = Task(
        description=f"Process the raw pricing data for {product_name} to standardize formats, handle currency conversions, remove outliers, and identify any inconsistencies or errors in the collected price information.",
        expected_output=f"A cleaned dataset with uniformly formatted prices for {product_name}, standardized currencies, and annotations for any identified anomalies or special pricing conditions.",
        agent=data_cleaner
    )

    comparison_task = Task(
        description=f"Analyze the cleaned pricing data to identify the lowest available price for {product_name}, calculate price differences between retailers, and determine price-to-value ratios based on product specifications.",
        expected_output=f"A comparative analysis showing price rankings for {product_name}, percentage differences between retailers, and identification of the best value options across different price points.",
        agent=comparison
    )

    reporting_task = Task(
        description=f"Create a comprehensive market insights report based on the {product_name} pricing analysis, highlighting best deals, pricing trends, and actionable recommendations for price-conscious consumers.",
        expected_output=f"A detailed report for {product_name} with executive summary, visualizations of price comparisons, identification of pricing patterns, and specific recommendations for optimal purchasing decisions.",
        agent=reporting_agent
    )

    # Return both agents and tasks
    return search, data_cleaner, comparison, reporting_agent, search_task, cleaning_task, comparison_task, reporting_task