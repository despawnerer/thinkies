class Service:
    @classmethod
    def create_for_user(cls, user):
        raise NotImplementedError

    def get_friends(self):
        raise NotImplementedError

    def get_profile(self):
        raise NotImplementedError


class Profile:
    uid = None
    name = None
    image = None
