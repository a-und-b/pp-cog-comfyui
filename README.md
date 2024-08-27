# ComfyUI Animal Art Generator

This project is a Cog-based implementation of a ComfyUI workflow that generates artistic images of animals using various AI models and techniques.

## Model Description

This model combines several powerful AI techniques to generate unique and artistic images of animals:

1. It uses a base SDXL (Stable Diffusion XL) model for high-quality image generation.
2. It incorporates animal-specific LoRA (Low-Rank Adaptation) models to enhance the generation of specific animal types.
3. It uses IP-Adapter technology to guide the image generation based on an input reference image.
4. It applies various artistic styles (e.g., watercolor, pop art, pixar style) to the generated images.

## Input Parameters

The model accepts the following input parameters:

1. `animal_lora_url` (string): URL or filename of the animal LoRA to use. This should be a safetensors file trained to generate a specific type of animal.
2. `animal_type` (string): The type of animal to generate (cat or dog)
3. `ip_adapter_image_url` (string): URL of the input image for IP-Adapter. This image will guide the style and composition of the generated image.
4. `output_format` (string, optional): The desired output format for the generated images (e.g., "png", "jpg", "webp").
5. `output_quality` (integer, optional): The quality of the output image (0-100, where 100 is the highest quality).

## Example Usage

To generate an artistic image of a cat using a specific cat LoRA and a reference image:

```bash
cog predict -i animal_lora_url="https://example.com/cat_lora.safetensors" \
            -i animal_type="cat" \
            -i ip_adapter_image_url="https://example.com/reference_image.jpg" \
            -i output_format="png" \
            -i output_quality=95
```

## Output

The model will generate a list of image files based on the input parameters. These images will be artistic renditions of the specified animal type, influenced by the provided LoRA and reference image, and styled according to various artistic techniques included in the workflow.

## Limitations

- The quality of the output heavily depends on the quality and specificity of the input LoRA and reference image.

