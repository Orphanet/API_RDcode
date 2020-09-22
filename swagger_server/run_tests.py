import unittest
import pathlib

# modules_to_test = ("*")
#
# suite = unittest.TestLoader().loadTests()
# unittest.TextTestRunner(verbosity=2).run(suite)

# unittest.loader.discover(".\\RDcode_API_server\\swagger_server\\test")

if __name__ == "__main__":
    loader = unittest.TestLoader()
    start_dir = str(pathlib.Path(r"C:\Users\cbigot\PycharmProjects\API_RDcode\swagger_server\test"))
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)
