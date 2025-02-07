# podcast_toolkit/podcast_toolkit/transcribe/transcribe_tool.py
import argparse
import os
import whisper
import warnings

def transcribe_audio(video_path, output_dir=None, output_name=None):
    """
    Transcribes audio from a video file using Whisper.

    Args:
        video_path (str): Path to the video file.
        output_dir (str, optional): Directory to save the transcript. Defaults to None (same as video dir).
        output_name (str, optional): Filename for the transcript. Defaults to None (video filename + .txt).
    """

    # Suppress warnings
    warnings.filterwarnings("ignore", message=".*You are using `torch.load`.*", category=FutureWarning)
    warnings.filterwarnings("ignore", message=".*FP16 is not supported on CPU.*", category=UserWarning)

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found at '{video_path}'")

    base_name, _ = os.path.splitext(os.path.basename(video_path))

    output_dir = output_dir if output_dir else os.path.dirname(video_path)
    output_name = output_name if output_name else base_name + ".txt"
    output_path = os.path.join(output_dir, output_name)

    model = whisper.load_model("base", device="cpu") # Let's make this selectable in the future
    result = model.transcribe(video_path)

    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"Transcription saved to: {output_path}")
    return output_path  # Return the output path for potential further use


def main_cli(args):
    parser = argparse.ArgumentParser(description="Transcribe video files to text using Whisper.")
    parser.add_argument("video_path", help="Path to the video file to transcribe")
    parser.add_argument("-o", "--output_dir", help="Directory to save the transcript (default: same as video)")
    parser.add_argument("-n", "--output_name", help="Filename for the transcript (default: video filename with .txt extension)")
    
    # Args are parsed in cli.py; Let's not parse again
    try:
        transcribe_audio(args.video_path, args.output_dir, args.output_name)
    except FileNotFoundError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main_cli()