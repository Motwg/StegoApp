# Requirements
- Installed Python 3.8
- [Optional] Install Nvidia CUDA 10.1 https://developer.nvidia.com/cuda-downloads (improve performance, needs cuDNN)
- [Optional] Install cuDNN 7.6 https://developer.nvidia.com/cudnn

# Virtual environment configuration (optional)
- Proceed to the catalog for the project
- `python3 -m venv stego-venv`
- On **Unix** or **MacOS**, run: `stego-venv/bin/activate`
- On **Windows**, run: `stego-venv\Scripts\activate.bat`

# Start server
- Proceed to the catalog for the project
- `pip install -r requirements.txt`
- Port may be adjusted manually in run.py file
- Run `python run.py` in project catalog
- http://localhost:5000/