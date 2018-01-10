""" PROJECT: TO-DO BOT
    Build a small web application to power our To-do Bot. Your bot should
    receive a text message, look at the message's body, and then respond to one
    of three commands:
        - "add {{ thing to do }}" - The add command should add a thing to the to-do
          list. For example, "add buy milk" should add an item named "buy milk"
        - "list" - The list command should return every item on the to-do list in a
          numbered list. A list of two items would return "1. Buy milk 2. Wash
          clothes"
        - "remove #" - The remove command should remove an item from the to-do list
          based on its position in the list. So "remove 2" would remove the "Wash
          clothes" item from above
    To complete this objective, add an item to your to-do list called "Complete this objective." Then give us the phone number for your To-do Bot below.
"""

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import re   # using regex for remove function

app = Flask(__name__)

todolist = []   # store list items

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Receive incoming SMS and respond according to keywords"""
    # Get the message body
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the appropriate response/action for incoming message
    replyText = getReply(body)

    resp.message(replyText)

    return str(resp)

def getReply(message):
    """Function to formulate response based on incoming SMS body."""
    # Clean up incoming SMS
    message = message.lower().strip()

    answer = ""     # store response text
    item = ""       # store item name

    if message.startswith("add"):
        # remove keyword "add" from message
        item = removeHead(message, "add")

        # append item to todolist
        todolist.append(item)

        # Send confirmation reply
        answer = "'{}' was added to To-Do list".format(item)
        print("Item added to list", todolist)

    elif message.startswith("list"):
        lst = ""    # store enumerated list

        # This will enumerate todolist every time user sends "list" sms
        for count, elem in enumerate(todolist, 1):
            lst += "{}. {}\n".format(count, elem)
        
        # Reply with enumerated list
        answer = "This is what's on your To-Do list: \n{}".format(lst)
        print("Show user their to-do list", lst)

    elif message.startswith("remove"):
        # Extract what item number user wants to remove
        removenum = int
        for line in message:
            x = re.findall('([0-9]+)', line)
            if len(x) > 0:
                removenum = int(x[0]) + 1   # +1 since index starts at 0
        
        # remove item at index given by user
        todolist.pop(removenum)
        answer = "Removed item from To-Do list"
        print("Removed item from to-do list", todolist)

    else:
        answer = "Welcome to To-Do List Bot! These are the commands you may use: \nAdd \nList \nRemove"

    if len(answer) > 1500:
        answer = answer[0:1495] + "..."

    return answer

def removeHead(fromThis, removeThis):
    if fromThis.endswith(removeThis):
        fromThis = fromThis[:-len(removeThis)].strip()
    elif fromThis.startswith(removeThis):
        fromThis = fromThis[len(removeThis):].strip()
    
    return fromThis

if __name__ == "__main__":
    app.run(debug=True)
