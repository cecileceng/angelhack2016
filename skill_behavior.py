import response_helper

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    session_attributes['currentScene'] = 'hotelBar'

    session_attributes['scene'] = {}
    session_attributes['scene']['hotelBar'] = {}
    session_attributes['scene']['hotelBar']['examine:bar'] = "This is the test description of the hotel bar"
    session_attributes['scene']['hotelBar']['smash']

    #session_attributes['descriptions'] = {}
    #session_attributes['descriptions']['camel'] = "This is a test description of the camel"
    #session_attributes['descriptions']['desk'] = "This is a test description of the desk"

    card_title = "Welcome"
    speech_output = "Welcome to the Alexa mud simulator. " \
                    "Are you ready to begin?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Are you ready to begin?"
    should_end_session = False
    return intent_handler.build_response(session_attributes, intent_handler.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa mud simulator. " \
                    "Have a nice day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return intent_handler.build_response({}, intent_handler.build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def handle_action_intent(intent, session):
    card_title = "Handle Action" #intent['scene']
    session_attributes = {}
    should_end_session = False

    scene = get_scene_from_session(session)

    if 'Action' in intent['slots']:
        # get and sanitize action value
        action = intent['slots']['Action']['value']
        action = str.lower(str(action))
        action = num_to_word.sanitize_numericals_in_string(action)

        action_description = get_action_description_from_scene(scene, action)
        speech_output = action_description
        reprompt_text = "I'm not sure what that is. " \
                        "Please try again."
    else:
        speech_output = "I'm not sure what that is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what that is. " \
                        "Please try again."

    return intent_handler.build_response(session_attributes, intent_handler.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_help_intent(intent, session):
    card_title = "Help"
    should_end_session = False

    speech_output = "How do I shot web?"
    reprompt_text = "I'm not sure what that is. " \
                    "Please try again."

    return intent_handler.build_response(session_attributes, intent_handler.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_quit_intent(intent, session):
    card_title = "Quit"
    should_end_session = True

    speech_output = "Goodbye."

    return intent_handler.build_response(session_attributes, intent_handler.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_session_attributes(session):
    return session.get('attributes', {})

def get_scene_from_session(session):

    if "currentScene" in session.get('attributes', {}):
        return session['attributes']['currentScene']
    else:
        return 'ERROR'

def get_scene_description_from_scene(session, scene):
        return get_session_attributes(session)['scene'][scene]
        # TODO parse description text from scene map
        #return 'Llamas'

def get_action_description_from_scene(scene, action):
        # TODO parse action description text from scene map
        return 'Do a flip!'

def load_scene_data():
        # TODO load scene data from file
        return

