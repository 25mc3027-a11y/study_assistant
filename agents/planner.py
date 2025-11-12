import datetime

def create_revision_plan(topics):
    """
    Generates a simple spaced-repetition revision plan based on a list of topics.
    
    Args:
        topics (list): A list of topic strings.
        
    Returns:
        list: A list of dictionaries, each with 'topic' and 'revise_on'.
    """
    if not topics:
        return []
        
    plan = []
    today = datetime.date.today()
    
    print(f"Generating revision plan for {len(topics)} topics...")
    
    for i, topic in enumerate(topics):
        # Simple logic from PDF: revise in 2 days, 4 days, 6 days, etc.
        revise_date = today + datetime.timedelta(days=(i + 1) * 2)
        plan.append({
            "topic": topic,
            # Format date as YYYY-MM-DD
            "revise_on": revise_date.strftime("%Y-%m-%d") 
        })
        
    return plan