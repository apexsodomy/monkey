import unittest

from infection_monkey.utils.commands import build_monkey_commandline_explicitly


class TestHelpers(unittest.TestCase):
    def test_build_monkey_commandline_explicitly(self):
        test1 = [
            "-p",
            "101010",
            "-t",
            "10.10.101.10",
            "-s",
            "127.127.127.127:5000",
            "-d",
            "0",
            "-l",
            "C:\\windows\\abc",
            "-vp",
            "80",
        ]
        result1 = build_monkey_commandline_explicitly(
            101010, "10.10.101.10", "127.127.127.127:5000", 0, "C:\\windows\\abc", 80
        )

        self.assertEqual(test1, result1)


if __name__ == "__main__":
    unittest.main()
