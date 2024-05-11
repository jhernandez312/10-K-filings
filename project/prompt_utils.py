system_message = "You are an expert text summarizer."


def generate_prompt(company):
    prompt = f"""
    Provide a detailed summary in bullet points of the most critical information from this 10-K filing that would be important for traders. Focus on the following areas:
    - Financial performance
    - Liquidity
    - Market trends
    - Risk factors
    - Strategic initiatives that might impact the company's stock price.

    Here is the 10-k filing:
    {company}
    """
    return prompt
