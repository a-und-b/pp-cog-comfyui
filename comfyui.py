import os
import urllib.request
import subprocess
import threading
import time
import json
import urllib
import uuid
import websocket
import random
import requests
import shutil
import custom_node_helpers as helpers
from cog import Path
from node import Node
from weights_downloader import WeightsDownloader
from urllib.error import URLError


class ComfyUI:
    def __init__(self, server_address):
        self.weights_downloader = WeightsDownloader()
        self.server_address = server_address

    def start_server(self, output_directory, input_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.apply_helper_methods("prepare", weights_downloader=self.weights_downloader)

        start_time = time.time()
        server_thread = threading.Thread(
            target=self.run_server, args=(output_directory, input_directory)
        )
        server_thread.start()
        while not self.is_server_running():
            if time.time() - start_time > 180:
                raise TimeoutError("Server did not start within 180 seconds")
            time.sleep(0.5)

        elapsed_time = time.time() - start_time
        print(f"Server started in {elapsed_time:.2f} seconds")

    def run_server(self, output_directory, input_directory):
        comfyui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ComfyUI")
        command = f"python {comfyui_path}/main.py --output-directory {output_directory} --input-directory {input_directory} --disable-metadata"
        print(f"Running command: {command}")
        server_process = subprocess.Popen(command, shell=True)
        server_process.wait()

    def is_server_running(self):
        try:
            with urllib.request.urlopen(
                "http://{}/history/{}".format(self.server_address, "123")
            ) as response:
                return response.status == 200
        except URLError:
            return False

    # ... [rest of the code remains unchanged]
