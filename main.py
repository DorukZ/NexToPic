import argparse
import os
from pathlib import Path
import requests

API_ENDPOINT = 'https://dzengin.app.n8n.cloud/webhook-test/20c3d3bd-b5d8-4715-9ac9-ffc22dc4fa9a'

def upload_photo(file_path: Path, style: str, package: str, timeout: int = 30) -> dict:
    """Upload a photo to the N8N webhook.

    Args:
        file_path: Path to the image file to upload.
        style: Desired style category.
        package: Package selection.
        timeout: Request timeout in seconds.

    Returns:
        Parsed JSON response from the webhook.

    Raises:
        FileNotFoundError: If file_path does not exist.
        requests.RequestException: For network-related errors.
        ValueError: If the response cannot be parsed as JSON.
    """
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    with file_path.open('rb') as img:
        files = {'photo': (file_path.name, img, 'application/octet-stream')}
        data = {'style': style, 'package': package}
        response = requests.post(API_ENDPOINT, files=files, data=data, timeout=timeout)
        response.raise_for_status()
        try:
            return response.json()
        except ValueError as exc:
            raise ValueError('Invalid JSON response') from exc


def main() -> None:
    parser = argparse.ArgumentParser(description='Upload a photo to NexToPic API')
    parser.add_argument('file', type=Path, help='Path to image file')
    parser.add_argument('--style', default='LinkedIn Professional', help='Style category')
    parser.add_argument('--package', default='Starter', help='Package choice')
    args = parser.parse_args()

    try:
        result = upload_photo(args.file, args.style, args.package)
    except Exception as exc:  # broad exception for user-friendly output
        print(f'Error: {exc}')
        return

    print(result)


if __name__ == '__main__':
    main()
