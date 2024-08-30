from langchain_openai import ChatOpenAI

def query_with_context(context, query):
    model = ChatOpenAI(model='gpt-4o-mini', temperature=0.0)
    template = [
            ('system', "From the given CONTEXT from a paper, answer the given QUERY."),
            ('user', f"CONTEXT: {context}"),
            ('user', f"QUERY: {query}")
        ]
    response = model.invoke(template)
    return response.content