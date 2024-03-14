# C8 Interface

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contact](#contact)

## Installation

For Colab installation, follow the steps below

1. Connect to the repo through pip

```bash
!pip install git+https://github.com/Saaaen/C8InterfacePrototype.git
```

2. import the package
```bash
from C8InterfacePrototype import c8
```

## Usage

1. Run the prompt
```bash
c8.run(openai_key, prompt)
```
2. Add new functions to the algorithm library
```bash
c8.load_function(funcaiton_name, function_description)
```
3. Show all the existing functions in the library
```bash
c8.show_available_functions()
```


## Contact
Saen Chen - saenc2@berkeley.edu