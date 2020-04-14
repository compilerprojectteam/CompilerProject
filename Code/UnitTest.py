import unittest
import Code.Compiler as Compiler
import os
import sys
import subprocess

Compiler.parser_errors = open("../out/parser-error.txt", "w", encoding="utf-8")
Compiler.parser_output = open("../out/parser-output.txt", "w", encoding="utf-8")

test_files = filter(lambda x: "while_scope" not in x, os.listdir("../test/tests/"))
desired_output_files = filter(lambda x: "while_scope" not in x, os.listdir("../test/desired_outputs/"))
test_files = sorted(test_files)
desired_output_files = sorted(desired_output_files)


def compile_and_run_tester(code_file):
    p = Compiler.Parser(code_file)
    p.parse()
    with open("output.txt", mode='w') as f:
        i = 0
        for line in p.sa.code_block:
            f.write("{}\t{}\n".format(i, line))
            # print("{}\t{}".format(i, line))
            i += 1
        f.close()
    if sys.platform == "linux":
        # os.system("./tester.out 2> null")
        result = subprocess.run("./tester.out".split(), stdout=subprocess.PIPE, stderr=0)
        os.remove("output.txt")
        return result.stdout.decode('utf-8')
        # os.system("./tester.out > test_output.txt")
    else:
        result = subprocess.run("tester.exe".split(), stdout=subprocess.PIPE, stderr=0)
        os.remove("output.txt")
        return result.stdout.decode('utf-8')
        # os.system("tester.exe &> test_output.txt")


class CompilerTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CompilerTest, self).__init__(*args, **kwargs)
        os.chdir("../test/")

    def test_code_generation(self):
        for test_file, output_file in zip(test_files, desired_output_files):
            with self.subTest(msg=test_file):
                result = compile_and_run_tester("tests/" + test_file)
                with open("desired_outputs/" + output_file) as o:
                    desired_output = "".join(o.readlines())

                result = result.strip()
                result = " ".join(result.split())
                result.replace(" ", "\t")
                desired_output = " ".join(desired_output.strip().split())
                desired_output.replace(" ", "\t")

                self.assertEqual(result, desired_output, "Should be \n " + desired_output)


if __name__ == "__main__":
    unittest.main()
