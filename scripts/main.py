from modules import script_callbacks, scripts
import gradio as gr
from fastapi import FastAPI
import os
from launch import run

import string
import random as rd

key_characters = (string.ascii_letters + string.digits)


def random_string(length=20):
    return ''.join([rd.choice(key_characters) for _ in range(length)])


key = random_string()


def get_files(path):
    # Gets all files
    directories = set()
    for root, _, files in os.walk(path):
        for file in files:
            directories.add(root + '/' + file)

    return directories


# Force allow paths for fixing symlinked extension directory references
force_allow = get_files(f"{os.path.abspath(scripts.basedir())}/app")


def started(demo, app: FastAPI):
    # Add to allowed files list
    app.blocks.temp_file_sets.append(force_allow)


def add_tab():
    with gr.Blocks(analytics_enabled=False) as ui:
        #refresh = gr.Button(value="refresh", variant="primary")
        canvas = gr.HTML(
            f"<iframe id=\"openoutpaint-iframe\" class=\"border-2 border-gray-200\" src=\"file/{usefulDirs[0]}/{usefulDirs[1]}/app/index.html?noprompt\"></iframe>")
        keyinput = gr.HTML(
            f"<input id=\"openoutpaint-key\" type=\"hidden\" value=\"{key}\">")
        # refresh.click(

        # )

    return [(ui, "openOutpaint", "openOutpaint")]


usefulDirs = scripts.basedir().split(os.sep)[-2:]

with open(f"{scripts.basedir()}/app/key.json", "w") as keyfile:
    keyfile.write('{\n')
    keyfile.write(f"  \"key\": \"{key}\"\n")
    keyfile.write('}\n')
    keyfile.close()

script_callbacks.on_ui_tabs(add_tab)
script_callbacks.on_app_started(started)
