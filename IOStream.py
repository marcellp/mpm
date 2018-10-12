class IOStream(object):
    def __init__(self):
        pass

    def out(self, string):
        print(string)

    def send_in(self, prompt = "> "):
        return input(prompt)
