# When implementing a new feature, please add at least one test case for it to this file.
# Your function name MUST begin with "test_", and SHOULD have a somewhat descriptive name.
# You can either have separate functions to test XML -> Object and Object -> XML,
# or can write a single function that tests both are working fully (the latter is probably sensible for easy cases
# such as integer etc. only). Note that each of these functions should
# have at least one 'assert' statement.

# Tests can all be run together by running 'python setup.py test' from the project root.
# Tests are automatically run by Travis when you push to version control or make a pull request,
# and an email should be sent to you if you push broken code.


# first ever test
def test_setup():
    assert 1 == 1