from os import system

install_dir = "/opt/pytilingassistant"
main_file = "main.py"
local_bins = "/usr/local/bin"

system("pip install -r requirements.txt")
system(f"sudo mkdir {install_dir}")
system(f"sudo cp {main_file} {install_dir}")
system(f"sudo chmod +x {install_dir}/{main_file}")
system(f"sudo ln -s {install_dir}/{main_file} {local_bins}/pytiling")