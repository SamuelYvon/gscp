# gscp: *G*it, *S*tage all, *C*ommit, *P*ush

I often find myself writing a bunch of code and wanting to commit it all, in one singular command. It's not
very hard:

```commandline
$ git add -u
$ git commit -v
$ git push
```

However, this is two commands two long. This should be in a singular command! This is why I once
had a `gscp` script in `$PATH` that did pretty much that. However, I wanted to add features over time:

- The ability to specify a commit message (sometimes)
- The ability to force push
- The ability to create amend commits
- And maybe more

It would have been easy enough to have those features in my shell script, but parsing
the flags in shell seemed harder than it needs to be. Therefore, I created a python package.
Yay python!

## Requirements

This is a rather simple script. It requires python 3.7 or higher. Because it uses git, you
obviously need to have git in path. It relies on the `pty` module. If the `pty` module is
limited in some OSes, those limits apply here. All the other requirements are in `pyproject.toml`.

## Building / Running

This project is built with poetry.


## Usage:

```commandline
usage: gscp [-h] [-a] [-f] [message]

positional arguments:
  message      Commit message to use. If no message specified, it falls back to git's default behaviour with verbose mode

options:
  -h, --help   show this help message and exit
  -a, --amend  If we using git amend mode (warning, this triggers a force push)
  -f, --force  If we use `git push --force`
```

## Disclaimer

Use at your own risk. This can force push stuff, after all.
