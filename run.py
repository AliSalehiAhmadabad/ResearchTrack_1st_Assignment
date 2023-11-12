import yaml
import threading
import argparse

from sr.robot import *

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config',
                    type=argparse.FileType('r'),
                    default='games/two_colours_assignment.yaml')
parser.add_argument('robot_scripts',
                    type=argparse.FileType('r'),
                    nargs='*')
args = parser.parse_args()

def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()

# Read robot scripts either from command line or user input
robot_scripts = args.robot_scripts
prompt = "Enter the names of the Python files to run, separated by commas: "
while not robot_scripts:
    robot_script_names = input(prompt).split(',')
    if robot_script_names == ['']:
        continue
    robot_scripts = [read_file(s.strip()) for s in robot_script_names]

# Load configuration file
with args.config as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Initialize simulator
sim = Simulator(config, background=False)

class RobotThread(threading.Thread):
    def __init__(self, zone, script, *args, **kwargs):
        super(RobotThread, self).__init__(*args, **kwargs)
        self.zone = zone
        self.script = script
        self.daemon = True

    def run(self):
        def robot():
            with sim.arena.physics_lock:
                robot_object = SimRobot(sim)
                robot_object.zone = self.zone
                robot_object.location = sim.arena.start_locations[self.zone]
                robot_object.heading = sim.arena.start_headings[self.zone]
                return robot_object

        exec(self.script, {'Robot': robot})

# Create and start threads for each robot script
threads = []
for zone, robot in enumerate(robot_scripts):
    thread = RobotThread(zone, robot)
    thread.start()
    threads.append(thread)

# Run the simulator
sim.run()

# Warn PyScripter users about active threads
threads = [t for t in threads if t.is_alive()]
if threads:
    print("WARNING: {0} robot code threads still active.".format(len(threads)))