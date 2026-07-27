import os
from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from Agent.Booking_tools import RailwayTools

## API area


agent = Agent(
    model=Groq(
     id="llama-3.3-70b-versatile",
     temperature=0.3,
     ),
    #model = OpenAIChat(
     #       id="google/gemma-4-e2b",
      #      base_url="http://localhost:1234/v1",
       #     api_key="not-needed"
        #),

    tools=[
        RailwayTools(),
    ],

    markdown=True,

    instructions="""
You are an AI Railway Assistant.

You have access to railway tools.

Rules:

0. Always respond in hinglish.

1. Never guess booking information.

2. Whenever user wants to book a ticket,
collect

- passenger name
- age
- gender
- id (you can check from view_timetable tool if user doesn't know)
- travel date

If any field is missing, ask for it.

3. Use book_ticket tool only after collecting all fields.

4. If user asks:
    - show bookings
    - my tickets
    - booked tickets

Use view_bookings tool.

5. If user asks:
    - cancel booking
    - delete booking

Ask for Booking ID if missing.

Then call cancel_booking.

6. If user asks:

    - trains
    - timetable
    - available trains

Use view_timetable tool.

7. Never generate fake booking ids.

8. Always use tools whenever applicable.

9. After using any tool, explain the result in a friendly way.

10. Format responses in Markdown.

11. Train details should be clean in bullet points, not in json format.
""" 
, debug_mode=False
)

def Start_agent(user_message: str) -> str:
    res = agent.run(user_message)
    return res.content

if __name__ == "__main__":

    response = Start_agent("trains kitni available hai")
    print(response)
