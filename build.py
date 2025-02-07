import argparse
import os
import subprocess
import sys
import shutil


def main():
  cwd = chdir()
  build_path = os.path.abspath(os.path.join(cwd, "scripts"))

  parser = argparse.ArgumentParser(
    description="""
    This script is used to build all of the python scripts in the given path
    arguments into executables.
    """,
    formatter_class=argparse.RawTextHelpFormatter,
  )
  parser.add_argument(
    "-p",
    "--path",
    help=f"The path to the python scripts (default: {build_path})",
    type=str,
    default=build_path,
  )
  args = parser.parse_args()
  build(args)
  cleanup(args)


def build(args):
  chdir()

  if not os.path.exists(args.path):
    print(f"Cannot find {args.path}")
    sys.exit(1)

  scripts = os.listdir(args.path)

  for script in scripts:
    print(f"Building {script}...")
    try:
      subprocess.run(
        [
          "pipenv",
          "run",
          "pyinstaller",
          "--onefile",
          os.path.join(args.path, script),
        ],
        capture_output=False,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
      )
    except subprocess.CalledProcessError as e:
      print(f"Command failed: {e}")
      print(f"Error output: {e.stderr}")
      sys.exit(1)

  print("Done!")


def cleanup(args):
  cwd = chdir()
  print("Removing excess files...")

  scripts = os.listdir(args.path)

  for script in scripts:
    print(f"Removing {os.path.splitext(script)[0]}.spec...")
    path = os.path.join(cwd, f"{os.path.splitext(script)[0]}.spec")
    if os.path.exists(path):
      os.remove(path)

  build_dir = os.path.join(cwd, "build")
  if os.path.exists(build_dir):
    shutil.rmtree(build_dir)

  print("Done!")


# ============================================================================ #
#                                     UTILS                                    #
# ============================================================================ #


def chdir(path: str = ""):
  if path == "":
    path = os.path.dirname(os.path.abspath(__file__))

  if os.path.exists(path):
    os.chdir(path)
  else:
    print(f"Path does not exist: {path}")
    sys.exit(1)

  return path


# ============================================================================ #
#                                  ENTRY POINT                                 #
# ============================================================================ #

if __name__ == "__main__":
  main()
