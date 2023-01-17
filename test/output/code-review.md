Potential bugs or security flaws: No input validation is performed on the SOURCE and DESTINATION variables, which could lead to a security vulnerability.

- Redundant code: The try/except block in the for loop is redundant as os.unlink will not throw an error if the file does not exist.

- Code that is hard to read or not idiomatic: The if statement for checking the return code of the subprocess is not idiomatic as it should be written as "if find_output.returncode == 0:" instead.
