import response_helper
import csv

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = load_scene_data()
    session_attributes['currentScene'] = 'introduction'
    print 'session_attributes:', session_attributes

    # session_attributes['scene'] = {}
    # session_attributes['scene']['hotelBar'] = {}
    # session_attributes['scene']['hotelBar']['examine:bar'] = "This is the test description of the hotel bar"
    # session_attributes['scene']['hotelBar']['smash']

    card_title = "Welcome to AlexaRPG"
    # debug output
    speech_output = 'Version 18. ' + \
        session_attributes['scene'][session_attributes['currentScene']+'+load']['description']
    #
    # sexy output
    # speech_output = "Welcome to Alexa R-P-G. Let's begin! " + \
    #     session_attributes['scene'][session_attributes['currentScene']]['description']
    should_end_session = False
    reprompt_text = "Sorry, I didn't catch that."

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
    session_attributes = session['attributes']

    print 'handle_action_intent.intent', intent
    print 'handle_action_intent.session', session

    scene = get_scene_from_session(session)
    speech_output = ''

    print 'handle_action_intent.scene', scene

    speech_output = "Sorry, I don't understand, please try again."
    reprompt_text = "Sorry, I didn't catch that."

    if ('Action' in intent['slots'] and 'Object' in intent['slots']) and ('value' in intent['slots']['Action'] and 'value' in intent['slots']['Object']):
        verb = response_helper.get_intent_value(intent, 'Action')
        thing = response_helper.get_intent_value(intent, 'Object')
        verb = response_helper.sanitize_verb(verb)
        action = verb + '-' + thing
        print 'handle_action_intent.action:',action

        if action_exists_in_scene(session, scene, action):
            action_description = get_action_description_from_scene(session, scene, action)
            next_scene = get_next_scene(session, scene, action)
            print 'handle_action_intent.next_scene', next_scene
            should_end_session = terminate_conversation(session, scene, action)
            session_attributes['currentScene'] = next_scene
            scene_description = get_scene_description_from_scene(session, next_scene)

            speech_output = action_description
            speech_output += scene_description

        reprompt_text = "You can: "
        available_actions = get_actions_in_scene(session, scene, action)
        for action_pair_index in range(len(available_actions)-1):
            ap = available_actions[action_pair_index]
            print "action pair: ", ap
            reprompt_text += ap[0] + " " + ap[1] + ", "
        if len(available_actions) > 1:
            reprompt_text += "or "
        if len(available_actions) > 0:
            reprompt_text += available_actions[-1][0] + " " + available_actions[-1][1]

    return response_helper.build_response(session_attributes, response_helper.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_help_intent(intent, session):
    card_title = "Help"
    should_end_session = False
    session_attributes = session['attributes']

    speech_output = "Try giving me an action and an object, like drink water."
    reprompt_text = "Sorry, I didn't catch that."

    return response_helper.build_response(session_attributes, response_helper.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_session_attributes(session, attribute):
    print 'get_session_attributes.(session,attribute):',session,attribute
    return session['attributes'][attribute]

def get_scene_from_session(session):
    return get_session_attributes(session, 'currentScene')

def get_scene_description_from_scene(session, scene):
    key = scene+'+load'
    return get_session_attributes(session, 'scene')[key]['description']

def terminate_conversation(session, scene, action):
    key = scene+'+'+action
    next_exec = get_session_attributes(session, 'scene')[key]['next_exec']

    if next_exec == 'exec_endgame':
        return True
    return False

def get_next_scene(session, scene, action):
    print 'get_next_scene.(scene,action)', scene, action
    key = scene+'+'+action
    next_exec = get_session_attributes(session, 'scene')[key]['next_exec']

    if next_exec[:10] == 'nextscene_':
        return next_exec[10:]
    return scene

def action_exists_in_scene(session, scene, action):
    key = scene + '+' + action
    print 'action_exists_in_scene.(key)', key
    return key in get_session_attributes(session, 'scene')

def get_action_description_from_scene(session, scene, action):
    key = scene+'+'+action
    return get_session_attributes(session, 'scene')[key]['description']

def get_actions_in_scene(session, scene, action):
    scenes = get_session_attributes(session, 'scene')
    actions = []
    for s in scenes:
        string = s.split('+')
        if scene == string[0]:
            action = string[1].split('-')
            if len(action) > 1:
                actions.append([action[0], action[1]])
    print 'get_actions_in_scene(): actions: ', actions
    return actions

def load_scene_data():
    all_data = list()
    with open('rpg_assets.tsv','rb') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            all_data.append(row)

    d = dict()
    d['scene'] = {}
    for r in all_data:
        desc_action = dict()
        desc_action['description'] = r[2]
        desc_action['next_exec'] = r[3]

        new_key = r[0] + '+' + r[1]
        d['scene'][new_key] = desc_action

    return d

if __name__ == '__main__':
    print load_scene_data()

