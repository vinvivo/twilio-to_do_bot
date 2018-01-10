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

app = Flask(__name__)

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

    todolist = []   # store list items
    answer = ""     # store response text
    item = ""       # store item name

    if "add" in message:
        # remove keyword "add" from message
        item = removeHead(message, "add")

        # append item to todolist
        todolist.append(item)

        # Send confirmation reply
        answer = "{} was added to to-do list".format(item)
        print("Item added to list" + todolist)  # for development

    elif "list" in message:
        answer = "This is what's on your to-do list: <list items here>"
        print("Show user their to-do list" + todolist)

    elif "remove" in message:
        # remove keyword "remove #" from message
        item = removeHead(message, "remove")    # TODO: how to handle list number
        answer = "Removed item from to-do list"
        print("Removed item from to-do list" + todolist)

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
