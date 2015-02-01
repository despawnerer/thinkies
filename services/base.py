class Service:
    @classmethod
    def create_for_user(cls, user):
        raise NotImplementedError

    def get_friends(self, user_id):
        raise NotImplementedError
