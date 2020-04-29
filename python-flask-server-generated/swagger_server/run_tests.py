import unittest
import pathlib

# modules_to_test = ("*")
#
# suite = unittest.TestLoader().loadTests()
# unittest.TextTestRunner(verbosity=2).run(suite)

# unittest.loader.discover(".\\python-flask-server-generated\\swagger_server\\test")

loader = unittest.TestLoader()
# C:\Users\Cyrlynx\PycharmProjects\API_RDcode\python-flask-server-generated\swagger_server\test
start_dir = str(pathlib.Path("C:\\Users\\Cyrlynx\\PycharmProjects\\API_RDcode\\python-flask-server-generated\\swagger_server\\test"))
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
runner.run(suite)
