import os
import sys
import argparse
import subprocess
import re


def main():
  uwd = os.getcwd()
  chdir()

  author = subprocess.run(
    ["git", "config", "--global", "user.name"], capture_output=True, text=True
  )
  author = author.stdout.strip()
  format_scheme = "\n- %B"

  parser = argparse.ArgumentParser(
    description="""
    This script is used to format a list of git commit messages from the past x
    hours.
    """,
    formatter_class=argparse.RawTextHelpFormatter,
  )
  parser.add_argument(
    "hours",
    help="The number of hours to get the messages from",
    type=int,
  )
  parser.add_argument(
    "-a",
    "--author",
    help=f"The author of the git commits (default: {author})",
    type=str,
    default=author,
  )
  parser.add_argument(
    "-b",
    "--branch",
    help="The branch to get the commit messages from (default: )",
    type=str,
    default="",
  )
  parser.add_argument(
    "--format",
    help=f"The format scheme to use (default: {format_scheme})",
    type=str,
    default=format_scheme,
  )
  parser.add_argument(
    "--uwd",
    help=f"The git directory to get the commit messages from (default: {uwd})",
    type=str,
    default=uwd,
  )
  args = parser.parse_args()

  get_commit_msg(args)


def get_commit_msg(args):
  chdir()
  print(
    f"Getting all commit messages for {args.author} from {args.hours} hours ago"
  )

  logs = subprocess.run(
    [
      "git",
      "log",
      "--all",
      f"--format={args.format}",
      f"--author={args.author}",
      f"--after=format:relative:{args.hours}.hours.ago",
    ],
    capture_output=True,
    text=True,
  )
  logs = logs.stdout.strip()
  logs = re.sub(r"\n+", "\n", logs)

  print(logs)

  if os.name == "nt":
    process = subprocess.Popen(["clip"], stdin=subprocess.PIPE, text=True)
    process.communicate(input=logs)
  else:
    print("OS not supported")

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


def run(command: list, **kwargs):
  try:
    subprocess.run(command, **kwargs)
  except subprocess.CalledProcessError as e:
    print(f"Command failed: {e}")
    print(f"Error output: {e.stderr}")
    sys.exit(1)


# ============================================================================ #
#                                  ENTRY POINT                                 #
# ============================================================================ #

if __name__ == "__main__":
  main()
