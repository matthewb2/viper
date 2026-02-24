class BaseAction:
    def match(self, ai_text):
        raise NotImplementedError
    def execute(self, ai_text, **kwargs): # 여기에 **kwargs만 넣어주면 됩니다.
        raise NotImplementedError