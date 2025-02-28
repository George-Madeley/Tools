dHISTTIMEFORMAT="%F %T "
HISTCONTROL=ignoreboth:erasedups
HISTIGNORE=?:??:history
HISTFILESIZE=99999
HISTSIZE=99999
PROMPT_COMMAND='history -a'
PROMPT_DIRTRIM=4

shopt -s cmdhist
shopt -s histappend histverify
shopt -s autocd
shopt -s cdspell
shopt -s direxpand dirspell
shopt -s globstar

if test -f ~/.config/git/git-prompt.sh; then
    . ~/.config/git/git-prompt.sh
fi

# Colors
blk='\[\033[01;30m\]' # Black
red='\[\033[01;31m\]' # Red
grn='\[\033[01;32m\]' # Green
ylw='\[\033[01;33m\]' # Yellow
blu='\[\033[01;34m\]' # Blue
pur='\[\033[01;35m\]' # Purple
cyn='\[\033[01;36m\]' # Cyan
wht='\[\033[01;37m\]' # White
clr='\[\033[00m\]'    # Reset

# bash commands
alias ls='ls -a --color=auto'
alias py='python'

# git commands
alias gs='git status'
alias ga='git add'
alias gaa='git add --all'
alias gc='git commit'
alias gl='git log --oneline'
alias gb='git checkout -b'
alias gd='git diff'
alias ..='cd ..;pwd'
alias ...='cd ../..;pwd'
alias ....='cd ../../..;pwd'
alias c='clear'
alias h='history'
alias tree='tree --dirsfirst -F'
alias mkdir='mkdir -p -v'

function git-publish() {
  branch=$(git symbolic-ref --short HEAD 2>/dev/null)
  git push --set-upstream origin "${1:-$branch}"
}

function git-init() {
    if [ -z "$1" ]; then
        printf "%s\n" "Please provide a directory name."
    else
        mkdir "$1"
        builtin cd "$1"
        pwd
        git init
        touch readme.md .gitignore LICENSE
        echo "# $(basename $PWD)" >>readme.md
    fi
}

function git-rename() {
  if [ -z "$1" ]; then
    echo "Usage: rename_git_branch <new-branch-name>"
    return 1
  fi

  current_branch=$(git branch --show-current)
  new_branch=$1

  # Rename the local branch
  git branch -m "$new_branch"

  # Delete the old branch from the remote
  git push origin --delete "$current_branch"

  # Push the new branch to the remote
  git push origin "$new_branch"

  # Set the upstream to the new branch
  git push --set-upstream origin "$new_branch"

  echo "Branch renamed from '$current_branch' to '$new_branch' both locally and remotely."
}

function git-parse-branch() {
    git branch 2>/dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}

function git-rebase() {
  if [ "$#" -ne 2 ]; then
    echo "Usage: my_function <main_branch> <merge_branch>"
    return 1
  fi

  git rebase --onto $1 $(git merge-base $2 $1) $2
}

function git-remove() {
  if [ "$#" -ne 1 ]; then
    echo "Usage: my_function <branch_name>"
    return 1
  fi

  git push origin -d $1
  git branch -D $1
}

function git-recommit() {
  if [ $# -eq 0 ]; then
      echo "No files specified. Usage: git_recommit <file1> <file2> ..."
      return 1
  fi

  last_commit_message=$(git log -1 --pretty=%B)
  git reset --soft HEAD~1
  git add "$@"
  git commit -m "$last_commit_message"
  git push --force
}

# calendar
alias jan='cal -m 01'
alias feb='cal -m 02'
alias mar='cal -m 03'
alias apr='cal -m 04'
alias may='cal -m 05'
alias jun='cal -m 06'
alias jul='cal -m 07'
alias aug='cal -m 08'
alias sep='cal -m 09'
alias oct='cal -m 10'
alias nov='cal -m 11'
alias dec='cal -m 12'

# Functions
function hg() {
    history | grep "$1"
}

function find_largest_files() {
    du -h -x -s -- * | sort -r -h | head -20
}

# PS1 Prompt
export GIT_PS1_SHOWSTASHSTATE=true
export GIT_PS1_SHOWDIRTYSTATE=true
export GIT_PS1_SHOWUNTRACKEDFILES=true
export GIT_PS1_SHOWUPSTREAM="auto"

function bash_prompt() {
    whoami | USERNAME=$(</dev/stdin)

    PIPENV_MSG=""
    if [ "$PIPENV_ACTIVE" = "1" ]; then
        PIPENV_MSG=" (pipenv)"
    fi

    PS1="\n${debian_chroot:+($debian_chroot)}"
    # set window title
    PS1="$PS1${wht}Git | Bash v\v | \W\007\]\n"
    # black text, magenta, 24h time
    PS1="$PS1${pur} [\A] "
    # black text, green, cleaned user
    PS1="$PS1${grn} $USERNAME "
    # black text, yellow, working directory
    PS1="$PS1${ylw} \w "
    # blue text, git branch
    PS1="$PS1${cyn}$(git-parse-branch)"
    # pipenv message
    PS1="$PS1${red}$PIPENV_MSG"
    PS1="$PS1${clr}\n$ "
}

PROMPT_COMMAND=bash_prompt

export PATH="$PATH:/c/git/Projects/Tools/dist"
