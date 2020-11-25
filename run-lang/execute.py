import subprocess as sp
import tempfile
import os


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
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, 'out')
        compilation = sp.Popen(
            ['g++', '-x', 'c++', '-o', out, '-'],
            stdin=sp.PIPE,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
        )
        compilation.stdin.write(code.encode('utf-8'))
        compilation.stdin.close()
        compilation.wait()
        if compilation.returncode != 0:
            return response(compilation.returncode,
                            compilation.stdout.read(),
                            compilation.stderr.read())
        evaluation = sp.Popen([out],
                              stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        evaluation.wait()
        return response(evaluation.returncode,
                        evaluation.stdout.read(), evaluation.stderr.read())


def execute_rust(code):
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, 'out')
        compilation = sp.Popen(
            ['rustc', '-o', out, '-'],
            stdin=sp.PIPE,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
        )
        compilation.stdin.write(code.encode('utf-8'))
        compilation.stdin.close()
        compilation.wait()
        if compilation.returncode != 0:
            return response(compilation.returncode,
                            compilation.stdout.read(),
                            compilation.stderr.read())
        evaluation = sp.Popen([out],
                              stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        evaluation.wait()
        return response(evaluation.returncode,
                        evaluation.stdout.read(), evaluation.stderr.read())


EXECUTE_LANG_TABLE = {
    "python": execute_python,
    "javascript": execute_javascript,
    "cpp": execute_cpp,
    "rust": execute_rust,
}


class LanguageNotFound(BaseException):
    pass


def execute(lang, code):
    try:
        return EXECUTE_LANG_TABLE[lang](code)
    except KeyError:
        raise LanguageNotFound()
