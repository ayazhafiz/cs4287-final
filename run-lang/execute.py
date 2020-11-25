import subprocess as sp


def response(code, stdout, stderr):
    return {
        "exitcode": code,
        "stdout": stdout.decode(),
        "stderr": stderr.decode(),
    }


def execute_python(code):
    # A python script can be executed directly.
    cmd = sp.Popen(
        ['python3'],
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
    )
    cmd.stdin.write(code.encode('utf-8'))
    cmd.stdin.close()
    cmd.wait()
    return response(cmd.returncode, cmd.stdout.read(), cmd.stderr.read())


def execute_javascript(code):
    # A JS script can be executed directly.
    cmd = sp.Popen(
        ['node'],
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
    )
    cmd.stdin.write(code.encode('utf-8'))
    cmd.stdin.close()
    cmd.wait()
    return response(cmd.returncode, cmd.stdout.read(), cmd.stderr.read())


def execute_cpp(code):
    # TODO
    cmd = sp.Popen(
        ['node'],
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
    )
    cmd.stdin.write(code.encode('utf-8'))
    cmd.stdin.close()
    cmd.wait()
    return response(cmd.returncode, cmd.stdout.read(), cmd.stderr.read())


EXECUTE_LANG_TABLE = {
    "python": execute_python,
    "javascript": execute_javascript,
    "cpp": execute_cpp,
}


class LanguageNotFound(BaseException):
    pass


def execute(lang, code):
    try:
        return EXECUTE_LANG_TABLE[lang](code)
    except KeyError:
        raise LanguageNotFound()
