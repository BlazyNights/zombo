import subprocess
import os
import shlex
import configparser

# Read config file
parser = configparser.ConfigParser()
parser.read('zombo.ini')

ffmpeg_path = parser.get('ffmpeg', 'path')
ffmpeg_args = parser.get('ffmpeg', 'args')

input_path = parser.get('input', 'path')
# Filter empty entries, turn it into a list
input_list = list(filter(None, parser.get('input', 'files').splitlines()))

output_path = parser.get('output', 'path')
output_list = list(filter(None, parser.get('output', 'files').splitlines()))
if not os.path.isdir(output_path):
    os.mkdir(output_path)


# Run the commands, mapping the input and output lists 1:1
for in_item, out_item in zip(input_list, output_list):
    command = shlex.split(f'"{ffmpeg_path}"'
                          f' -i "{os.path.join(input_path, in_item)}"'
                          f' {ffmpeg_args}'
                          f' "{os.path.join(output_path, out_item)}"')
    print(command)
    subprocess.run(command, check=True)
