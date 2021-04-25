"""Defines a test class with scenarios for the functions module."""

from marduk import functions


class TestFunctions():
    """Test class containing scenarios for the functions module."""

    # Define string tests.

    def test_stringify_list_001(self) -> None:
        """Tests stringify_list without quoted output."""
        # Define input list.
        input_list = [1, 2, 'a', 'b']

        # Define expected string output.
        exp = '1, 2, a, b'

        # Get actual string output.
        got = functions.stringify_list(list_=input_list, quoted=False)

        # Test output.
        assert got == exp


    def test_stringify_list_002(self) -> None:
        """Tests stringify_list with quoted output."""
        # Define input list.
        input_list = [1, 2, 'a', 'b']

        # Define expected string output.
        exp = "'1', '2', 'a', 'b'"

        # Get actual string output.
        got = functions.stringify_list(list_=input_list, quoted=True)

        # Test output.
        assert got == exp
