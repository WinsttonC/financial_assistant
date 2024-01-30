import os
from operator import itemgetter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from dotenv import load_dotenv
load_dotenv()




def text_vectorization(texts : list):
    vectorstore = FAISS.from_texts( 
        texts, embedding=OpenAIEmbeddings()
    )
    return vectorstore.as_retriever()


def run_chain(texts, ticker):
    
    template = """Ответьте на вопрос, основываясь только на следующем контексте:
    {context}

    Вопрос: {question}
    """
    query = f"Сделай предположение относительно акций котировки {{${ticker}}}: в текстах скорее ожидают рост компании, падение или удержание цены актива."
    
    prompt = ChatPromptTemplate.from_template(template)

    model = ChatOpenAI(model='gpt-3.5-turbo-1106', api_key=os.getenv("OPENAI_API_KEY"))
    
    retriever = text_vectorization(texts)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return chain.invoke(query)
