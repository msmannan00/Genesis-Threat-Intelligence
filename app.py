from native_services.application_manager.application_controller import application_controller
from native_services.application_manager.application_enums import APPICATION_COMMANDS
from crawler_services.native_services.mongo_manager.mongo_controller import mongo_controller
from crawler_services.native_services.mongo_manager.mongo_enums import MONGODB_COMMANDS, mongo_crud

# mongo_controller.get_instance().invoke_trigger(MONGODB_CRUD_COMMANDS.S_DELETE,[MONGODB_COMMANDS.S_CLEAR_INDEX])
# mongo_controller.get_instance().invoke_trigger(MONGODB_CRUD_COMMANDS.S_DELETE,[MONGODB_COMMANDS.S_CLEAR_BACKUP])
# mongo_controller.get_instance().invoke_trigger(MONGODB_CRUD_COMMANDS.S_DELETE,[MONGODB_COMMANDS.S_CLEAR_TFIDF])

mongo_controller.get_instance().invoke_trigger(mongo_crud.S_UPDATE, [MONGODB_COMMANDS.S_RESET_BACKUP_URL, False])
application_controller.get_instance().invoke_trigger(APPICATION_COMMANDS.S_LOAD_TOPIC_CLASSIFIER_DATASET)
