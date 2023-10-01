

class Model:
    
    @classmethod
    def load(cls, config: CFGModel) -> Union[Whisper, Llama]:
        pass
    
    @classmethod
    def __compute_checksum(cls, config: CFGModel) -> str:
        pass

    @classmethod
    def __download_model(cls, config: CFGModel) -> str:
        pass

    @classmethod
    def __check_available(cls, config: CFGModel) -> bool:
        pass

    @classmethod
    def __load_from_config(cls, config: CFGModel) -> Union[Whisper, Llama]:
        pass

