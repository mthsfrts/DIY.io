class OAuth:

    @staticmethod
    def get_token():
        """This Class is responsible for the Google OAuth """

        with open('../keys/google_authkey.txt', 'r') as passwrd:

            return passwrd.read()
