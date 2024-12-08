
from strings import system_prompt , resume_txt


from langchain.prompts.chat import SystemMessagePromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from pydantic import BaseModel
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()

class number(BaseModel):
    num: int = Field(description="The number of the option selected")
class chat(BaseModel):
    answer: str = Field(description="Answer to the asked question")

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

def chat_query(query):
  try:
      groq_chat = ChatGroq(
                      groq_api_key=GROQ_API_KEY, 
                      model_name="llama3-8b-8192"
              )
      messages = []
      template = system_prompt
      system_message_prompt = SystemMessagePromptTemplate.from_template(template)
      messages.append(system_message_prompt)
      
      human_template = """Given the following inputs:
      RESUME:
      --
      {resume_txt}
      --
      QUERY
      --
      {query}
      --
      
      Answer the question from the resume in the format

      {format}
      """
      
      output_parser = JsonOutputParser(pydantic_object=chat)
      format_instructions = output_parser.get_format_instructions()

      human_message = HumanMessagePromptTemplate.from_template(human_template)
      messages.append(human_message)
      chat_prompt = ChatPromptTemplate.from_messages(messages)
      request = chat_prompt.format_prompt(resume_txt=resume_txt,query=query,format=format_instructions).to_messages()
      
      response = groq_chat(request)
      print(response)

      fixing_parser = OutputFixingParser.from_llm(parser = output_parser, llm = groq_chat)
      for chance in range(1,7):
          try:
              fixed_output = fixing_parser.parse(response.content)
              print(fixed_output)
              return fixed_output["answer"]
          except:
              continue
          else:
              break
          
      
      return fixed_output["answer"]
  except Exception as e:
      print(f"error in Answering Question {e}")
      return "None"    

def radio_query(query):
  try:
      groq_chat = ChatGroq(
                      groq_api_key=GROQ_API_KEY, 
                      model_name="llama3-70b-8192"
              )
      messages = []
      template = system_prompt
      system_message_prompt = SystemMessagePromptTemplate.from_template(template)
      messages.append(system_message_prompt)
      
      human_template = """Given the following inputs:
      RESUME:
      --
      {resume_txt}
      --
      QUERY
      --
      {query}
      --
      
      Answer the question from the resume in the format
      IMPORTANT: ONE Option must be selected at all cost.
      NOTE: Return only the OPTION

      {format}
      """
      
      output_parser = JsonOutputParser(pydantic_object=number)
      format_instructions = output_parser.get_format_instructions()

      human_message = HumanMessagePromptTemplate.from_template(human_template)
      messages.append(human_message)
      chat_prompt = ChatPromptTemplate.from_messages(messages)
      request = chat_prompt.format_prompt(resume_txt=resume_txt,query=query,format=format_instructions).to_messages()
      
      response = groq_chat(request)
      print(response)

      fixing_parser = OutputFixingParser.from_llm(parser = output_parser, llm = groq_chat)
      for chance in range(1,7):
          try:
              fixed_output = fixing_parser.parse(response.content)
              print(fixed_output)
              return fixed_output["num"]
          except:
              continue
          else:
              break
          
      
      return fixed_output["num"]
  except Exception as e:
      print(f"error in Answering Question {e}")
      return "1"    