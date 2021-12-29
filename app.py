from native_services.application_manager.application_controller import application_controller
from native_services.application_manager.application_enums import APPICATION_COMMANDS
from crawler_services.native_services.mongo_manager.mongo_controller import mongo_controller
from crawler_services.native_services.mongo_manager.mongo_enums import MONGODB_COMMANDS, MONGO_CRUD

# mongo_controller.get_instance().invoke_trigger(MONGO_CRUD.S_DELETE, [MONGODB_COMMANDS.S_CLEAR_INDEX,[None],[None]])
# mongo_controller.get_instance().invoke_trigger(MONGO_CRUD.S_DELETE, [MONGODB_COMMANDS.S_CLEAR_BACKUP,[None],[None]])
# mongo_controller.get_instance().invoke_trigger(MONGO_CRUD.S_DELETE, [MONGODB_COMMANDS.S_CLEAR_TFIDF,[None],[None]])

mongo_controller.get_instance().invoke_trigger(MONGO_CRUD.S_UPDATE,[MONGODB_COMMANDS.S_RESET_BACKUP_URL,None,[False]])
application_controller.get_instance().invoke_trigger(APPICATION_COMMANDS.S_INSTALL_TOPIC_CLASSIFIER)
