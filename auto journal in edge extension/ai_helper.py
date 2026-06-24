def generate_standup_notes(raw_activities, git_commits):
    prompt = f"""
    You are an elite developer assistant. Analyze the following raw activity logs and Git commits from today and synthesize them into a clean, professional Daily Standup note.
    
    Group similar activities together. Ignore repetitive transitions (e.g., switching back and forth between the same tabs). Focus on outcomes.
    
    Raw Web Logs:
    {raw_activities}
    
    Git Commits:
    {git_commits}
    
    Format the output as:
    ### 🚀 What I Did Today
    - [High-level summary of feature/bug]
      - Technical details based on commits/documentation viewed
    ### 🚧 Blockers / Notes
    - [Inferred blockers based on heavy StackOverflow usage, or leave blank if none]
    """
    # Pass this prompt to your LLM library of choice
    return prompt