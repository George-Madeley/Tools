import argparse
import os
import sys


def main():
	directory = os.path.abspath(os.getcwd())
	chdir()
	parser = argparse.ArgumentParser(
		description="""
    This script is used to generate the index.{js|ts} files of the current
    directory
    """
	)
	parser.add_argument(
		"-r",
		"--recursive",
		help="""
    When set, makes the index.{js|ts} file recursively for each child directory
    of the given directory as well
    """,
		action="store_true",
	)
	parser.add_argument(
		"-v",
		"--verbose",
		help="""
    When set, details all of the index.{js|ts} files being created
    """,
		action="store_true",
	)
	parser.add_argument(
		"directory",
		help=f"""
    The directory to generate the index.{{js|ts}} file in. (default:
		{directory})
    """,
		nargs="?",
		default=directory,
	)
	parser.add_argument(
		"--ext",
		help="""
  	The file extension to use for the index.{js|ts} file. (default: '.ts')
   	""",
		choices=[".ts", ".js"],
		default=".ts",
	)
	args = parser.parse_args()

	if args.directory:
		args.directory = os.path.abspath(os.path.join(directory, args.directory))

	print(f"Starting at {args.directory}")

	if args.recursive:
		recursive(args)
	gen_index(args.directory, args)


def gen_index(dir: str, args):
	chdir()
	if args.verbose:
		dir_name = args.directory.replace(
			os.path.dirname(args.directory) + os.sep, ""
		)
		sub_dir = dir.replace(args.directory + os.sep, "").replace(
			args.directory, ""
		)
		relative_path = os.path.join(dir_name, sub_dir)
		print(f"Generating index{args.ext} at {os.sep}{relative_path}")
	chdir(dir)

	files = os.listdir(dir)

	files = [f for f in files if f != "index.ts" and f != "index.js"]

	valid_ext = [".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs"]

	index_path = os.path.join(dir, f"index{args.ext}")
	with open(index_path, "w") as index_file:
		for file in files:
			ext = os.path.splitext(os.path.basename(file))[-1]
			if ext in valid_ext or os.path.isdir(file):
				name = os.path.splitext(os.path.basename(file))[0]
				index_file.write(f'export * from "./{name}";\n')


def recursive(args):
	chdir()

	paths = []
	for root, dirs, files in os.walk(args.directory):
		for dir in dirs:
			path = os.path.abspath(os.path.join(root, dir))
			if not os.path.exists(path):
				print(f"Directory could not be found:\n{path}")
				sys.exit(1)
			paths.append(path)
	paths.sort()
	for path in paths:
		gen_index(path, args)


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
