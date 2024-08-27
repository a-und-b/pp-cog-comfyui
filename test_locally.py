import subprocess
import json

def run_prediction():
    command = [
        "cog",
        "predict",
        "-i", "animal_lora_url=https://example.com/cat_lora.safetensors",
        "-i", "animal_type=cat",
        "-i", "ip_adapter_image_url=https://example.com/reference_image.jpg",
        "-i", "watercolor_seed=42",
        "-i", "pixar_seed=123",
        "-i", "popart_seed=789",
        "-i", "output_format=png",
        "-i", "output_quality=95"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Prediction successful!")
        print("Output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error occurred during prediction:")
        print(e.stderr)

if __name__ == "__main__":
    run_prediction()