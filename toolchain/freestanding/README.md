`conan create .`

Reduce RAM/CPU: `conan create . -c tools.build:jobs=1`

On FreeBSD force the use of the gnu tools (like gcc, make). Using a profile for this:
~~~~
[conf]
tools.gnu:make_program = gmake
~~~~

