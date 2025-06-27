import os

from openai import OpenAI


class MarkdownResponderService:
    def __init__(self):
        self.openai_client = None
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.openai_client = OpenAI(api_key=api_key)

    def generate_markdown_response(self, user_query, sql_query, df):
        if not self.openai_client:
            return "", "No LLM configured - using fallback response"

        if df.empty:
            data_summary = "No results found"
        elif len(df) <= 20:  # Increased from 5 to 20 to give LLM full data to work with
            data_summary = f"Full data:\n{df.to_string(index=False)}"
        else:
            data_summary = f"Found {len(df)} rows. Sample data:\n{df.head(5).to_string(index=False)}"

        prompt = f"""
        You are an expert SEC filing analyst. Given the user's question, SQL query, and data results, provide a crisp, direct answer and a brief explanation.

        User Question: {user_query}
        SQL Query: {sql_query}
        Data Results: {data_summary}

        Instructions:
        1. Start with a bolded 'Answer:' section containing a concise, direct answer to the user's question.
        2. If there are results, include a properly formatted markdown table of the data.
        3. Be succinct and avoid unnecessary verbosity.
        4. If there are no results, state so clearly in the Answer section.
        """
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert SEC analyst creating crisp, direct markdown answers and explanations.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=800,
                temperature=0.3,
            )

            markdown_response = response.choices[0].message.content
            return markdown_response, prompt
        except Exception as e:
            print(f"Error generating markdown response: {e}")
            fallback_response = "**Answer:** No results found.\n\n**Explanation:**\nThere were no matching records for your query."
            return fallback_response, prompt
