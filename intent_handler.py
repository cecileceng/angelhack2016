def handle_examineIntent(intent, session):

    description = "I am not sure what you wanted to examine, can you ask me that again?"
    #if 'Object' in intent['slots']:
    #    objKey = intent['slots']['Object']['value']
    #    if 'descriptions' in session.get('attributes', {}):
    #        description = session['attributes']['descriptions'][objKey]

    return build_response({}, build_speechlet_response(intent['name'], description, None, False))








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