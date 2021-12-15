# Local Imports
from crawler_services.native_services.topic_classifier_manager.topic_classifier_enums import TOPIC_CLASSFIER_MODEL, \
    TOPIC_CLASSFIER_TRAINER, TOPIC_CLASSFIER_COMMANDS
from crawler_services.shared_model.request_handler import request_handler
from crawler_services.native_services.topic_classifier_manager.topic_classifier_model import topic_classifier_model
from crawler_services.native_services.topic_classifier_manager.topic_classifier_trainer import topic_classifier_trainer


class topic_classifier(request_handler):

    __instance = None
    __m_classifier_trainer = None
    __m_classifier = None

    # Initializations
    @staticmethod
    def get_instance():
        if topic_classifier.__instance is None:
            topic_classifier()
        return topic_classifier.__instance

    def __init__(self):
        topic_classifier.__instance = self
        self.__m_classifier_trainer = topic_classifier_trainer()
        self.__m_classifier = topic_classifier_model()

    def __generate_classifier(self):
        self.__m_classifier_trainer.invoke_trigger(TOPIC_CLASSFIER_TRAINER.S_GENERATE_CLASSIFIER)

    def __predict_classifier(self, p_title,p_description, p_keyword):
        return self.__m_classifier.invoke_trigger(TOPIC_CLASSFIER_MODEL.S_PREDICT_CLASSIFIER, [p_title, p_description, p_keyword])

    def invoke_trigger(self, p_command, p_data=None):
        if p_command == TOPIC_CLASSFIER_COMMANDS.S_GENERATE_CLASSIFIER:
            self.__generate_classifier()
        if p_command == TOPIC_CLASSFIER_COMMANDS.S_PREDICT_CLASSIFIER:
            return self.__predict_classifier(p_data[0], p_data[1], p_data[2])
        pass
