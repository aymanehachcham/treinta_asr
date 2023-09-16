# Speech and Text Processing with OpenAI and Llama

This repository focuses on both Speech-to-Text (STT) and Text Generation functionalities. 
Currently using a local version of whisper and llama based on the work of 
[whisper.cpp](https://github.com/ggerganov/whisper.cpp), [llama.cpp](https://github.com/ggerganov/llama.cpp)
with a python biding. 

The idea would be to create a seamless integration between the two modules.
Could also be integrated in more complex pipelines using the [LangChain](https://github.com/langchain-ai/langchain) library.

## Table of Contents

- [About the Repository](#about-the-repository)
- [Installation](#installation)
- [Modules Explanation](#modules-explanation)
- [Contributing](#contributing)
- [License](#license)

## About the Repository

This repository provides an integrated solution for STT and Text Generation tasks. We use a mix of cloud-based services and local modules to ensure both flexibility and power.

## Installation

1. **Create a virtual environment**:

   ```bash
    conda create -n virtual_env python=3.10
    ```
   
2. **Clone the repo**:

   ```bash
   git clone https://github.com/aymanehachcham/treinta_asr.git
     ```
3. **Install the requirements**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Download the local models**:

   ```bash
   Will have a script bash doing it.
   ```   
## Modules Explanation

- **STT Modules**:
  - **OpenAI Whisper**: This is a cloud-based STT service that provides accurate speech recognition. To learn more about its usage in this repo, see [this module's documentation](link-to-module-docs).
  - **Whisper Local**: Our local instance of the Whisper system provides flexibility when an internet connection is not available.

- **Text Generation Modules**:
  - **OpenAI API**: This cloud-based service offers state-of-the-art text generation capabilities.
  - **Llama Local**: An in-house solution for generating text offline or when more control over the model is required.

## Contributing

Contributions are always welcome! Please see our [contributing guidelines](link-to-contributing.md) for more details.

## License

This project is licensed under the XYZ License - see the [LICENSE](LICENSE) file for details.
