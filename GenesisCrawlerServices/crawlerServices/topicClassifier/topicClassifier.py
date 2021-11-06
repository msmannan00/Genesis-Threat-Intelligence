# Local Imports
from GenesisCrawlerServices.crawlerServices.topicClassifier.topicClassifierEnums import TOPIC_CLASSFIER_MODEL, \
    TOPIC_CLASSFIER_TRAINER, TOPIC_CLASSFIER_COMMANDS
from GenesisCrawlerServices.sharedModel.requestHandler import RequestHandler
from GenesisCrawlerServices.crawlerServices.topicClassifier.topicClassifierModel import TopicClassifierModel
from GenesisCrawlerServices.crawlerServices.topicClassifier.topicClassifierTrainer import topicClassifierTrainer


class TopicClassifier(RequestHandler):

    __instance = None
    __m_classifier_trainer = None
    __m_classifier = None

    # Initializations
    @staticmethod
    def get_instance():
        if TopicClassifier.__instance is None:
            TopicClassifier()
        return TopicClassifier.__instance

    def __init__(self):
        TopicClassifier.__instance = self
        self.__m_classifier_trainer = topicClassifierTrainer()
        self.__m_classifier = TopicClassifierModel()

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
