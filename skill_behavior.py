import response_helper
import csv

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = load_scene_data()
    session_attributes['currentScene'] = 'test_room+load'
    print 'session_attributes:', session_attributes

    # session_attributes['scene'] = {}
    # session_attributes['scene']['hotelBar'] = {}
    # session_attributes['scene']['hotelBar']['examine:bar'] = "This is the test description of the hotel bar"
    # session_attributes['scene']['hotelBar']['smash']

    card_title = "Welcome to AlexaRPG"
    speech_output = "Welcome to Alexa RPG. Let's begin!" + \
        session_attributes['scenes'][session_attributes['currentScene']]['description']
    should_end_session = False
    reprompt_text = None

    return response_helper.build_response(session_attributes, response_helper.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for playing Alexa RPG! " \
                    "Have a nice day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return response_helper.build_response({}, response_helper.build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def handle_action_intent(intent, session):
    card_title = "Handle Action" #intent['scene']
    should_end_session = False

    scene = get_scene_from_session(session)
    speech_output = ''

    if 'Action' in intent['slots'] and 'Object' in intent['slots']:
        verb = response_helper.get_intent_value(intent, 'Action')
        thing = response_helper.get_intent_value(intent, 'Object')
        action = verb + '-' + thing
        action_description = get_action_description_from_scene(scene, action)
        speech_output += action_description
        next_scene = get_next_scene(scene, action)
        scene_description = get_scene_description_from_scene(next_scene)
        speech_output += scene_description
        
        reprompt_text = "Sorry, I didn't catch that."
    else:
        speech_output = "I'm not sure what that is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what that is. " \
                        "Please try again."

    return response_helper.build_response(session_attributes, response_helper.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_help_intent(intent, session):
    card_title = "Help"
    should_end_session = False

    speech_output = "How do I shot web?"
    reprompt_text = "I'm not sure what that is. " \
                    "Please try again."

    return response_helper.build_response(session_attributes, response_helper.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_quit_intent(intent, session):
    card_title = "Quit"
    should_end_session = True

    speech_output = "Goodbye."

    return response_helper.build_response(session_attributes, response_helper.build_speechlet_response(
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
    all_data = list()
    with open('rpg_assets.tsv','rb') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            all_data.append(row)

    d = dict()
    d['scenes'] = {}
    for r in all_data:
        desc_action = dict()
        desc_action['description'] = r[2]
        desc_action['next_exec'] = r[3]

        new_key = r[0] + '+' + r[1]
        d['scenes'][new_key] = desc_action

    return d

if __name__ == '__main__':
    print load_scene_data()
