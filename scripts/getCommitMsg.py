import os
import sys
import argparse
import subprocess
import re


def main():
  uwd = os.getcwd()

  author = subprocess.run(
    ["git", "config", "--global", "user.name"], capture_output=True, text=True
  )
  author = author.stdout.strip()

  chdir()

  parser = argparse.ArgumentParser(
    description="""
    This script is used to format a list of git commit messages from the past x
    hours.
    """,
    formatter_class=argparse.RawTextHelpFormatter,
  )
  parser.add_argument(
    "hours", help="The number of hours to get the messages from", type=int
  )
  parser.add_argument(
    "--author",
    help=f'The author of the git commits (default: "{author}")',
    type=str,
    default=author,
  )
  parser.add_argument(
    "--branch",
    help="The branch to get the commit messages from (default: )",
    type=str,
    default="",
  )
  parser.add_argument(
    "--uwd",
    help=f"The git directory to get the commit messages from (default: {uwd})",
    type=str,
    default=uwd,
  )
  parser.add_argument(
    "--group",
    help="Whether to group the commits by the branch they come from",
    action="store_true",
  )
  args = parser.parse_args()

  if args.group:
    group_commit_msg(args)
  else:
    get_commit_msg(args, args.branch)

  print("Done!")


def group_commit_msg(args):
  chdir()

  if not os.path.exists(args.uwd):
    print(f"Could not find path {args.uwd}")
    sys.exit(1)

  chdir(args.uwd)
  # Get list of all branches
  branches = subprocess.run(
    ["git", "branch", "--all", "--format=%(refname:short)"],
    stdout=subprocess.PIPE,
    text=True,
  )

  if branches.returncode != 0:
    print(f"Error: {branches.stderr}")
    sys.exit(1)

  branches = branches.stdout.strip().split("\n")

  local_branches = []
  for branch in branches:
    if not branch.startswith("origin/"):
      local_branches.append(branch)

  for branch in branches:
    if branch.replace("origin/", "") not in local_branches:
      local_branches.append(branch)

  logs = ""
  for branch in local_branches:
    branch_logs = get_commit_msg(args, branch)
    if branch_logs:
      logs += f"{branch}\n"
      logs += branch_logs
      logs += "\n\n"
  print(f"{logs}")

  if os.name == "nt":
    process = subprocess.Popen(["clip"], stdin=subprocess.PIPE, text=True)
    process.communicate(input=logs)
  else:
    process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE, text=True)
    process.communicate(input=logs)


def get_commit_msg(args, branch):
  chdir()
  if not args.group:
    print(
      f"""
      Getting all commit messages for {args.author} from {args.hours} hours ago
      """
    )

  if not os.path.exists(args.uwd):
    print(f"Could not find path {args.uwd}")
    sys.exit(1)

  chdir(args.uwd)

  if branch == "":
    logs = subprocess.run(
      [
        "git",
        "log",
        "--all",
        "--format=\n- %B",
        f"--author={args.author}",
        f"--after=format:relative:{args.hours}.hours.ago",
      ],
      stdout=subprocess.PIPE,
      text=True,
    )
  else:
    logs = subprocess.run(
      [
        "git",
        "log",
        branch,
        "--format=\n- %B",
        f"--author={args.author}",
        f"--after=format:relative:{args.hours}.hours.ago",
      ],
      stdout=subprocess.PIPE,
      text=True,
    )

  if logs.returncode != 0:
    print(f"Error: {logs.stderr}")
    sys.exit(1)

  logs = logs.stdout.strip()
  if logs == "":
    return ""

  logs = format_commit_messages(logs)

  if not args.group:
    print(f"{logs}")

  if os.name == "nt":
    process = subprocess.Popen(["clip"], stdin=subprocess.PIPE, text=True)
    process.communicate(input=logs)
  else:
    process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE, text=True)
    process.communicate(input=logs)

  return logs


def format_commit_messages(log):
  formatted_log = []
  for commit in log.split("\n\n\n"):
    lines = re.sub(r"\n\n", r"", commit)
    lines = commit.split("\n")
    if lines:
      formatted_log.append(lines[0])
      for line in lines[1:]:
        if line != "":
          formatted_log.append(f"\t{line}")
  return "\n".join(formatted_log)


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
