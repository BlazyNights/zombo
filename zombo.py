import subprocess
import os
import shlex
import configparser
import sys


def run_command(__command: str, print_only=False):
    """
    Runs a given str on the system shell.
    :param __command: str, command to run in shell
    :param print_only: bool, default False, use if you want to just preview the command
    :return: None
    """
    if print_only:
        print(f'{__command} \n')

    else:
        print(f'Running command: {__command} \n')
        __command = shlex.split(__command)
        subprocess.run(__command, check=True)


def main():
    # Read config file
    parser = configparser.ConfigParser()
    parser.read('zombo.ini')

    preview_mode = bool(int(parser.get('preview', 'print_only')))

    ffmpeg_path = parser.get('ffmpeg', 'path')
    ffmpeg_args = parser.get('ffmpeg', 'args')

    input_path = parser.get('input', 'path')
    # Filter empty entries, turn it into a list
    input_list = list(filter(None, parser.get('input', 'files').splitlines()))

    use_additional_files = bool(int(parser.get('additional_files', 'use_additional_files')))
    additional_files_path = parser.get('additional_files', 'path')
    additional_files_list = list(filter(None, parser.get('additional_files', 'files').splitlines()))

    output_path = parser.get('output', 'path')
    output_list = list(filter(None, parser.get('output', 'files').splitlines()))
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    # Run the commands, mapping the input and output lists 1:1 (or 1:1:1 if using additional files)
    if use_additional_files:
        for in_item, additional_file, out_item in zip(input_list, additional_files_list, output_list):
            command = f'"{ffmpeg_path}"' \
                      f' -i "{os.path.join(input_path, in_item)}"' \
                      f' -i "{os.path.join(additional_files_path, additional_file)}"' \
                      f' {ffmpeg_args}' \
                      f' "{os.path.join(output_path, out_item)}"'
            run_command(command, print_only=preview_mode)

    else:
        for in_item, out_item in zip(input_list, output_list):
            command = f'"{ffmpeg_path}"'\
                      f' -i "{os.path.join(input_path, in_item)}"'\
                      f' {ffmpeg_args}'\
                      f' "{os.path.join(output_path, out_item)}"'
            run_command(command, print_only=preview_mode)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print('Stopping...')
        sys.exit(-1)
