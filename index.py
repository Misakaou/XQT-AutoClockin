from clockin import *

def handler(event, context):
    logging.info(Language().get_message('name') + '-' + Config().get_config_str('app', 'name'))
    logging.info(Language().get_message('author') + '-' + Config().get_config_str('app', 'author'))
    logging.info(Language().get_message('version') + '-' + Config().get_config_str('app', 'version'))
    
    user_list = UserReader().get_user_list()
    if len(user_list) > 1:
        user_list = shuffle(user_list)
    
    for user in user_list:
        ShixiClockin(user).clockin()
        ClockinClockin(user).clockin()
        sleep(randint(1, 3))