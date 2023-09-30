first load:
    - check default folder structure
      - if not exists create it
    - load default config
    - validate config
    - save config to the user root path

folder structure
    /home/user/.asr/models
    /home/user/.asr/config.toml

entrypoint
    - loading config:
        default if not exists
        user can specify config path
        or load from default path /home/user/.asr/config.toml
    - loading models
        default models:
        user can specify model path or name
        models are downloaded
            yes: load models
            no: donwload models () /home/user/.asr/models
    - Check permission on the microphone
    - whisper is loaded and llama 2 is loaded
    - Infinite Loop:
      - Whisper will start listening to the microphone (async)
          - this should produce a buffer that is init at root level
      - Route the buffer to llama 2
          - llama 2 will process the buffer and return a string
