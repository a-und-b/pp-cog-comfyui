# ComfyUI Cog Custom Model

This project is a custom implementation of ComfyUI as a Cog model, designed to generate animal images in different art styles using LoRA models and IP-Adapter.

## Input Parameters

1. `animal_lora_url` (string): URL or filename of the animal LoRA to use. This should be a safetensors file trained to generate a specific type of animal.
2. `animal_type` (string): The type of animal to generate (cat or dog)
3. `ip_adapter_image_url` (string): URL of the input image for IP-Adapter. This image will guide the style and composition of the generated image.
4. `watercolor_seed` (integer, optional): Seed for watercolor generation. If not provided, a random seed will be used.
5. `pixar_seed` (integer, optional): Seed for Pixar-style generation. If not provided, a random seed will be used.
6. `popart_seed` (integer, optional): Seed for Pop Art generation. If not provided, a random seed will be used.
7. `output_format` (string, optional): The desired output format for the generated images (e.g., "png", "jpg", "webp").
8. `output_quality` (integer, optional): The quality of the output image (0-100, where 100 is the highest quality).

## Example Usage

```bash
cog predict -i animal_lora_url="https://example.com/cat_lora.safetensors" \
            -i animal_type="cat" \
            -i ip_adapter_image_url="https://example.com/reference_image.jpg" \
            -i watercolor_seed=42 \
            -i pixar_seed=123 \
            -i popart_seed=789 \
            -i output_format="png" \
            -i output_quality=95
```

## Testing Instructions

1. Ensure you have Cog installed on your system. If not, follow the installation instructions at [https://github.com/replicate/cog](https://github.com/replicate/cog).

2. Clone this repository and navigate to the project directory.

3. Build the Cog model:
   ```
   cog build
   ```

4. Run a prediction using the example command above, replacing the URLs and parameters with your desired values.

5. The generated images will be saved in the output directory specified in the `predict.py` file.

## Notes

- The `animal_lora_url` and `ip_adapter_image_url` are provided via the API call for each prediction.
- If seed values are not provided, random seeds will be generated for each style.
- Make sure the animal LoRA and IP-Adapter reference image URLs are accessible when running the prediction.

For any issues or questions, please refer to the project documentation or open an issue in the repository.
