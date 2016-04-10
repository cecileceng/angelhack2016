def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa mud simulator. " \
                    "Are you ready to begin?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Are you ready to begin?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa mud simulator. " \
                    "Have a nice day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def handle_scene_response(intent, session):
    card_title = intent['scene']
    session_attributes = {}
    should_end_session = False

    scene = get_scene_from_session(session)

    if 'Scene' in intent['slots']:
        scene = intent['slots']['Scene']['value']
        scene_description = get_scene_description_from_scene(scene)
        session_attributes = {"currentScene": scene}
        speech_output = scene_description

    elif 'Action' in intent['slots']:
        action = intent['slots']['Action']['value']
        action_description = get_action_description_from_scene(scene, action)
        speech_output = action_description
        reprompt_text = "I'm not sure what that is. " \
                        "Please try again."
    else:
        speech_output = "I'm not sure what that is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what that is. " \
                        "Please try again."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_scene_from_session(session):
    session_attributes = {}
    reprompt_text = None

    if "currentScene" in session.get('attributes', {}):
        scene = session['attributes']['currentScene']
    else:
        scene = 'start'

def get_scene_description_from_scene(scene):
        # TODO parse description text from scene map
        return 'Llamas'

def get_action_description_from_scene(scene, action):
        # TODO parse action description text from scene map
        return 'Do a flip!'

