import os
import sys
import argparse
import subprocess
import shutil
import platform
import tempfile

def main():
  chdir()
  if os.name == "nt":
    yarn = os.path.abspath(os.path.join(tempfile.gettempdir(), "..", "..", "Roaming", "npm", "yarn.cmd"))
    npm = os.path.abspath(os.path.join("C:\\", "Program Files", "nodejs", "npm.cmd"))
  else:
    yarn = os.path.abspath(os.path.join(tempfile.gettempdir(), "..", "..", "Roaming", "npm", "yarn"))
    npm = os.path.abspath(os.path.join("C:\\", "Program Files", "nodejs", "npm"))
  
  parser = argparse.ArgumentParser(
    """
    This tool is use to setup this repo which includes performing a fresh
    install of node_modules in all directories, setting up the pipenv
    environment, and installing all of the git submodules.
    """)
  parser.add_argument(
    "--npm_path",
    help=f"The path to npm executable.\ndefault: {npm}",
    type=str,
    default=npm
  )
  parser.add_argument(
    "--yarn_path",
    help=f"The path to yarn executable.\ndefault: {yarn}",
    type=str,
    default=yarn
  )
  args = parser.parse_args()
  
  setup_pipenv(args)
  setup_node_modules(args)
  
def setup_pipenv(args):
  cwd = chdir()
  
  if not os.path.exists(os.path.join(cwd, "Pipfile")):
    print(f"Pipfile could not be found at {cwd}");
    return
  
  os.environ["PIPENV_VENV_IN_PROJECT"] = "1"

  try:
    subprocess.run(["pipenv", "install"], check=True)
  except:
    print("Failed to setup pipenv")
    sys.exit(1)
  print("Done!")
  
def setup_node_modules(args):
  cwd = chdir()
  
  node_modules_path = os.path.join(cwd, 'node_modules')
  if os.path.exists(node_modules_path):
    print(f"Removing {node_modules_path}...")
    shutil.rmtree(node_modules_path)
    
  print("Detecting package manager...")
  if os.path.exists('package-lock.json'):
    package_manager = args.npm_path
  elif os.path.exists('yarn.lock'):
    package_manager = args.yarn_path
  else:
    print("No lock file found, using npm...")
    package_manager = args.npm_path
    
  
  if not os.path.exists(package_manager):
    print(f"Cannot find {os.path.basename(package_manager)} at {package_manager}")
    sys.exit(1)
  
  try:
    print(f"Installing node_modules with {os.path.basename(package_manager)}...")
    subprocess.run([package_manager, "install"], check=True)
  except:
    print("Failed to install node_modules")
    sys.exit(1)
  print("Done!")
  
# ---------------------------------------------------------------------------- #
#                                     utils                                    #
# ---------------------------------------------------------------------------- #

def chdir(path: str = ""):
  if path == "":
    path = os.path.dirname(os.path.abspath(__file__))
  
  if os.path.exists(path):
    os.chdir(path)
  else:
    print(f"Path does not exist: {path}")
    sys.exit(1)
    
  return path

if __name__ == "__main__":
  main()