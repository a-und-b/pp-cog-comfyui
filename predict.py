import os
import mimetypes
import json
import random
from typing import List, Optional
from cog import BasePredictor, Input, Path
from comfyui import ComfyUI
from cog_model_helpers import optimise_images

OUTPUT_DIR = "/tmp/outputs"
INPUT_DIR = "/tmp/inputs"
COMFYUI_TEMP_OUTPUT_DIR = "ComfyUI/temp"
ALL_DIRECTORIES = [OUTPUT_DIR, INPUT_DIR, COMFYUI_TEMP_OUTPUT_DIR]

mimetypes.add_type("image/webp", ".webp")

api_json_file = "workflow_api.json"

os.environ["HF_DATASETS_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

class Predictor(BasePredictor):
    def setup(self):
        self.comfyUI = ComfyUI("127.0.0.1:8188")
        self.comfyUI.start_server(OUTPUT_DIR, INPUT_DIR)

        with open(api_json_file, "r") as file:
            workflow = json.loads(file.read())
        self.comfyUI.handle_weights(
            workflow,
            weights_to_download=[
                (os.environ["JUGGERNAUT_XL_URL"], "juggernautXL_v9Rundiffusionphoto2.safetensors"),
                (os.environ["ADD_DETAIL_XL_URL"], "add-detail-xl.safetensors"),
                (os.environ["ARS_MJ_STYLE_XL_URL"], "ArsMJStyleXL_-_Watercolor.safetensors"),
                (os.environ["FRESH_IDEAS_PIXAR_URL"], "Fresh Ideas@pixar style_SDXL.safetensors"),
                (os.environ["POP_ART_STYLE_URL"], "pop_art_style.safetensors"),
            ],
        )

    def update_workflow(self, workflow, **kwargs):
        # Update animal LoRA URL
        workflow["5"]["inputs"]["lora_name"] = kwargs["animal_lora_url"]
        
        # Update animal type in prompts
        for node_id in ["8", "14", "21", "28"]:
            if "prompt" in workflow[node_id]["inputs"]:
                workflow[node_id]["inputs"]["prompt"] = workflow[node_id]["inputs"]["prompt"].replace("{animal_type}", kwargs["animal_type"])
            if "wildcard_text" in workflow[node_id]["inputs"]:
                workflow[node_id]["inputs"]["wildcard_text"] = workflow[node_id]["inputs"]["wildcard_text"].replace("{animal_type}", kwargs["animal_type"])
            if "populated_text" in workflow[node_id]["inputs"]:
                workflow[node_id]["inputs"]["populated_text"] = workflow[node_id]["inputs"]["populated_text"].replace("{animal_type}", kwargs["animal_type"])

        # Update IP-Adapter input image URL
        workflow["16"]["inputs"]["image"] = kwargs["ip_adapter_image_url"]

        # Update seeds (wildcard population and image generation)
        workflow["8"]["inputs"]["seed"] = kwargs["watercolor_seed"]
        workflow["10"]["inputs"]["seed"] = kwargs["watercolor_seed"]
        workflow["21"]["inputs"]["seed"] = kwargs["pixar_seed"]
        workflow["23"]["inputs"]["seed"] = kwargs["pixar_seed"]
        workflow["28"]["inputs"]["seed"] = kwargs["popart_seed"]
        workflow["30"]["inputs"]["seed"] = kwargs["popart_seed"]

    def predict(
        self,
        animal_lora_url: str = Input(
            description="URL or filename of the animal LoRA to use",
            default="https://example.com/animal_lora.safetensors",
        ),
        animal_type: str = Input(
            description="Type of animal (e.g., cat, dog)",
            default="cat",
        ),
        ip_adapter_image_url: str = Input(
            description="URL of the input image for IP-Adapter",
            default="https://example.com/input_image.jpg",
        ),
        watercolor_seed: Optional[int] = Input(
            description="Seed for watercolor generation (leave empty for random)",
            default=None,
        ),
        pixar_seed: Optional[int] = Input(
            description="Seed for Pixar-style generation (leave empty for random)",
            default=None,
        ),
        popart_seed: Optional[int] = Input(
            description="Seed for Pop Art generation (leave empty for random)",
            default=None,
        ),
        output_format: str = optimise_images.predict_output_format(),
        output_quality: int = optimise_images.predict_output_quality(),
    ) -> List[Path]:
        """Run a single prediction on the model"""
        self.comfyUI.cleanup(ALL_DIRECTORIES)

        with open(api_json_file, "r") as file:
            workflow = json.loads(file.read())

        # Generate random seeds if not provided
        watercolor_seed = watercolor_seed if watercolor_seed is not None else random.randint(0, 2**32 - 1)
        pixar_seed = pixar_seed if pixar_seed is not None else random.randint(0, 2**32 - 1)
        popart_seed = popart_seed if popart_seed is not None else random.randint(0, 2**32 - 1)

        self.update_workflow(
            workflow,
            animal_lora_url=animal_lora_url,
            animal_type=animal_type,
            ip_adapter_image_url=ip_adapter_image_url,
            watercolor_seed=watercolor_seed,
            pixar_seed=pixar_seed,
            popart_seed=popart_seed,
        )

        wf = self.comfyUI.load_workflow(workflow)
        self.comfyUI.connect()
        self.comfyUI.run_workflow(wf)

        return optimise_images.optimise_image_files(
            output_format, output_quality, self.comfyUI.get_files(OUTPUT_DIR)
        )
