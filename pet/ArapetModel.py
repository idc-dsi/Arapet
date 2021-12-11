from pet.wrapper import TransformerModelWrapper
wrapper_config = {"py/object": "pet.wrapper.WrapperConfig", "model_type": "bert", "model_name_or_path": "DSI/personal_sentiment", "wrapper_type": "sequence_classifier", "task_name": "arabic_multilabel", "max_seq_length": 256, "label_list": ["no_ref", "neutral", "positive", "negative"], "pattern_id": 0, "verbalizer_file": None, "cache_dir": ""}
#model = TransformerModelWrapper.from_pretrained(wrapper_config)

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
#args = wrapper_config

def InitArapetModel(wrapper_config=wrapper_config):
    wrapper_config = Struct(**wrapper_config)
    model = TransformerModelWrapper(wrapper_config)
    return model