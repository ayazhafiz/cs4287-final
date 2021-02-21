import subprocess as sp
import tempfile
import os
from pathlib import Path
from .describe import get_server_lang


HOME = os.environ["HOME"]


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
    orig = os.getcwd()
    os.chdir("/playground/build")
    with tempfile.NamedTemporaryFile('w', dir=".", suffix=".cpp") as tmp:
        tmp.write(code)
        tmp.flush()
        out = Path(tmp.name).stem
        compilation = sp.Popen(
            ['c++', tmp.name,
             '@conanbuildinfo.args',
             '-std=c++17',
             '-fdiagnostics-color=always',
             '-o', out],
            stdin=sp.PIPE,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
        )
        compilation.wait()
    if compilation.returncode != 0:
        return response(compilation.returncode,
                        compilation.stdout.read(),
                        compilation.stderr.read())
    evaluation = sp.Popen([f"./{out}"],
                          stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    evaluation.wait()
    os.chdir(orig)
    return response(evaluation.returncode,
                    evaluation.stdout.read(), evaluation.stderr.read())


def execute_rust(code):
    orig = os.getcwd()
    os.chdir(f"{HOME}/playground")
    with tempfile.NamedTemporaryFile('w', dir="src/bin",
                                     suffix=".rs") as tmp:
        tmp.write(code)
        tmp.flush()
        bin_name = Path(tmp.name).stem
        cmd = sp.Popen(
            [f"{HOME}/.cargo/bin/cargo", 'run',
             "--color", "always",
             '--bin', bin_name],
            stdin=sp.PIPE,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
        )
        cmd.wait()
    os.chdir(orig)
    return response(cmd.returncode, cmd.stdout.read(), cmd.stderr.read())


def execute(code):
    lang = get_server_lang()
    if lang == "python":
        return execute_python(code)
    if lang == "javascript":
        return execute_javascript(code)
    if lang == "cpp":
        return execute_cpp(code)
    if lang == "rust":
        return execute_rust(code)
    else:
        raise Exception(f"Language not suppported {lang}")
