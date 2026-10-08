from .telemetry import validate
from .rules import detect_and_classify, load_rules

class Monitor:
    def __init__(self, store):
        self.store = store
        self.rules = load_rules()

    def process(self, data):
        result = detect_and_classify(validate(data), self.rules)
        result['id'] = self.store.save(result)
        return result
