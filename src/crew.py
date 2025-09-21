from src.tasks import create_tasks
from crewai import Crew

def create_crew(product_name, country, model_name):
    # Create agents and tasks using the create_tasks function
    search, data_cleaner, comparison, reporting_agent, search_task, cleaning_task, comparison_task, reporting_task = create_tasks(product_name, country, model_name)

    # Define the crew (agents and tasks)
    event_management_crew = Crew(
        agents=[search, data_cleaner, comparison, reporting_agent],
        tasks=[search_task, cleaning_task, comparison_task, reporting_task],
        verbose=True,
    )
    return event_management_crew