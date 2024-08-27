1. `animal_lora_url` (string): URL or filename of the animal LoRA to use. This should be a safetensors file trained to generate a specific type of animal.
2. `animal_type` (string): The type of animal to generate (cat or dog)
3. `ip_adapter_image_url` (string): URL of the input image for IP-Adapter. This image will guide the style and composition of the generated image.
4. `output_format` (string, optional): The desired output format for the generated images (e.g., "png", "jpg", "webp").
5. `output_quality` (integer, optional): The quality of the output image (0-100, where 100 is the highest quality).

## Example Usage

```bash
cog predict -i animal_lora_url="https://example.com/cat_lora.safetensors" \
            -i animal_type="cat" \
            -i ip_adapter_image_url="https://example.com/reference_image.jpg" \
            -i output_format="png" \
            -i output_quality=95
```
