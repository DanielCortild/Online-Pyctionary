class Chat:
    def __init__(self):
        self.content = []

    def update_chat(self, msg):
        """
        Updates chat with the given message
        :param msg: str
        :return: None
        """
        self.content.append(msg)

    def get_chat(self):
        return self.content

    def clear_chat(self):
        self.content = []
