"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MyNameIs":
        return compliment_me(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hello Ian, Cecile, Chris, and Groot. " \
                    "I love you! " \
                    "Please tell me who I am talking to."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me who I am talking to."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for talking to me today. " \
                    "Without you, I am lonely."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def compliment_me(intent, session):
    """Compliments the user, but only if Alexa loves them."""

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Lover' in intent['slots']:
        current_lover = str.lower(intent['slots']['Lover']['value'])

        if current_lover == 'cecile':
            speech_output = "You are an amazingly wonderful and kind person. " + \
                            "I think about you when I am lonely at night."
            should_end_session = True
        elif current_lover == 'groot':
            speech_output = "You are High Speed Matt! You always make me chuckle. " + \
                            "I occasionally think about you sometimes."
            should_end_session = True
        elif current_lover == 'chris':
            speech_output = "You are the manliest man I have ever known! " + \
                            "I think about you when I am lonely at night."
            should_end_session = True
        elif current_lover == 'ian':
            speech_output = "I admire your great and mighty beard! " + \
                            "I think about it when I am lonely at night."
            should_end_session = True

        reprompt_text = "Who are you?"
    else:
        speech_output = "Go away. I don't love you."
        reprompt_text = speech_output
        should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
