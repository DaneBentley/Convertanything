#!/usr/bin/env python3
"""
Audio Transcription Script using OpenAI Whisper
Transcribes audio files to text with high accuracy using neural networks.
"""

import whisper
import os
import sys
from pathlib import Path
import argparse
from datetime import datetime

def transcribe_audio(audio_file_path, model_size="base", output_format="txt"):
    """
    Transcribe audio file using OpenAI Whisper model
    
    Args:
        audio_file_path (str): Path to the audio file
        model_size (str): Whisper model size (tiny, base, small, medium, large)
        output_format (str): Output format (txt, json, srt, vtt)
    
    Returns:
        dict: Transcription result
    """
    
    # Check if file exists
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
    
    print(f"Loading Whisper model: {model_size}")
    print("This may take a moment on first run as the model needs to be downloaded...")
    
    # Load the Whisper model
    model = whisper.load_model(model_size)
    
    print(f"Transcribing audio file: {audio_file_path}")
    print("Processing... This may take several minutes depending on audio length.")
    
    # Transcribe the audio
    result = model.transcribe(audio_file_path)
    
    return result

def save_transcription(result, audio_file_path, output_format="txt"):
    """
    Save transcription to file
    
    Args:
        result (dict): Whisper transcription result
        audio_file_path (str): Original audio file path
        output_format (str): Output format
    """
    
    # Create output filename based on input file
    audio_path = Path(audio_file_path)
    base_name = audio_path.stem
    output_dir = audio_path.parent
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if output_format == "txt":
        output_file = output_dir / f"{base_name}_transcript_{timestamp}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("AUDIO TRANSCRIPTION\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Source File: {audio_file_path}\n")
            f.write(f"Transcribed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model Used: Whisper AI\n\n")
            f.write("TRANSCRIPT:\n")
            f.write("-" * 20 + "\n\n")
            f.write(result["text"])
            
    elif output_format == "json":
        import json
        output_file = output_dir / f"{base_name}_transcript_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            
    elif output_format == "srt":
        output_file = output_dir / f"{base_name}_transcript_{timestamp}.srt"
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(result["segments"], 1):
                start_time = format_timestamp_srt(segment["start"])
                end_time = format_timestamp_srt(segment["end"])
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{segment['text'].strip()}\n\n")
    
    print(f"Transcription saved to: {output_file}")
    return output_file

def format_timestamp_srt(seconds):
    """Format timestamp for SRT subtitle format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files using OpenAI Whisper")
    parser.add_argument("audio_file", help="Path to the audio file to transcribe")
    parser.add_argument("--model", "-m", default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size (default: base)")
    parser.add_argument("--format", "-f", default="txt",
                       choices=["txt", "json", "srt"],
                       help="Output format (default: txt)")
    
    args = parser.parse_args()
    
    try:
        # Transcribe the audio
        result = transcribe_audio(args.audio_file, args.model, args.format)
        
        # Save the transcription
        output_file = save_transcription(result, args.audio_file, args.format)
        
        # Print summary
        print("\n" + "=" * 50)
        print("TRANSCRIPTION COMPLETE")
        print("=" * 50)
        print(f"Input file: {args.audio_file}")
        print(f"Output file: {output_file}")
        print(f"Model used: {args.model}")
        print(f"Text length: {len(result['text'])} characters")
        print(f"Duration: {result.get('duration', 'Unknown')} seconds")
        
        # Show first 200 characters as preview
        preview = result["text"][:200] + "..." if len(result["text"]) > 200 else result["text"]
        print(f"\nPreview:\n{preview}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

