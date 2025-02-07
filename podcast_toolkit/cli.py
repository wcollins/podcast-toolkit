# podcast-toolkit/podcast_toolkit/cli.py
import sys
import argparse
from podcast_toolkit.transcribe import transcribe_tool

def main():
    parser = argparse.ArgumentParser(description="Podcast Post-Processing Toolkit")
    subparsers = parser.add_subparsers(title='subcommands', dest='command', help='Available tools')

    # Subparser for transcribe_tool
    transcribe_parser = subparsers.add_parser('transcribe', help='Transcribe audio from a video/audio file')
    transcribe_parser.add_argument("video_path", help="Path to the video/audio file to transcribe")
    transcribe_parser.add_argument("-o", "--output_dir", help="Directory to save the transcript")
    transcribe_parser.add_argument("-n", "--output_name", help="Filename for the transcript")
    transcribe_parser.set_defaults(func=transcribe_tool.main_cli)  # Associate with the transcribe tool's CLI

    # Parse args
    args = parser.parse_args()
    print(f"Parsed args: {args}")  # Print args that are being parsed

    if args.command == 'transcribe':
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()