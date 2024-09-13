from knowledge_base.models import Document

# from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from langchain_community.llms import Tongyi
from langchain_community.llms import Tongyi
from typing import List, Dict, Generator
import time
import json


def stream_response_bk(llm, prompt):
    for chunk in llm.stream(prompt):
        response = {
            "created": int(time.time()),
            "choices": [
                {
                    "message": {"role": "assistant", "content": chunk},
                    "finish_reason": None,
                }
            ],
        }
        yield f"data: {json.dumps(response)}\n\n"

    final_response = {
        "created": int(time.time()),
        "choices": [
            {"message": {"role": "assistant", "content": ""}, "finish_reason": "stop"}
        ],
    }
    yield f"data: {json.dumps(final_response)}\n\n"


def stream_response(llm, prompt):
    for chunk in llm.stream(prompt):
        yield {
            "created": int(time.time()),
            "choices": [
                {
                    "message": {"role": "assistant", "content": chunk},
                    "finish_reason": None,
                }
            ],
        }

    yield {
        "created": int(time.time()),
        "choices": [
            {"message": {"role": "assistant", "content": ""}, "finish_reason": "stop"}
        ],
    }


def generate_response(llm, prompt):
    response = llm.generate([prompt])
    content = response.generations[0][0].text

    return {
        "created": int(time.time()),
        "usage": {
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": len(content.split()),
            "total_tokens": len(prompt.split()) + len(content.split()),
        },
        "choices": [
            {
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
    }


def get_single_document_qa(
    document_id: int, messages: List[Dict[str, str]], stream: bool
) -> str | Generator:
    document = Document.objects.get(id=document_id)
    llm = Tongyi(streaming=stream)

    # 构建提示词模板
    prompt_template = """
    以下是一份文档的内容：

    {document_content}

    历史对话：
    {chat_history}

    请根据上述文档内容和历史对话回答以下问题：

    {question}

    请只基于文档中提供的信息来回答，如果文档中没有相关信息，请说明无法回答。
    """

    # 处理历史消息
    chat_history = ""
    for message in messages[:-1]:  # 除了最后一条消息
        role = "Human" if message["role"] == "user" else "Assistant"
        chat_history += f"{role}: {message['content']}\n"

    # 获取最后一个用户消息作为问题
    question = messages[-1]["content"] if messages[-1]["role"] == "user" else ""

    # 构建完整的提示词
    full_prompt = prompt_template.format(
        document_content=document.content, chat_history=chat_history, question=question
    )

    # 生成回答
    if stream:
        return stream_response(llm, full_prompt)
    else:
        return generate_response(llm, full_prompt)


def get_multi_document_qa(document_id, messages, stream):
    document = Document.objects.get(id=document_id)

    # 初始化 LangChain 组件
    # llm = OpenAI(streaming=stream)
    llm = Tongyi(streaming=stream)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # 创建检索链
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=document.get_retriever(), memory=memory
    )

    # 处理消息历史
    for message in messages:
        if message["role"] == "user":
            memory.chat_memory.add_user_message(message["content"])
        else:
            memory.chat_memory.add_ai_message(message["content"])

    # 获取最后一个用户消息作为问题
    question = messages[-1]["content"] if messages[-1]["role"] == "user" else ""

    # 生成回答
    response = qa_chain({"question": question})

    return response["answer"]
