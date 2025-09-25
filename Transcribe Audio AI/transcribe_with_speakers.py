#!/usr/bin/env python3
"""
Audio Transcription Script with Speaker Diarization
Transcribes audio files and separates speakers using AI neural networks.
"""

import whisper
import torch
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
import os
import sys
from pathlib import Path
import argparse
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

def load_models(whisper_model_size="base"):
    """
    Load Whisper and speaker diarization models
    """
    print(f"Loading Whisper model: {whisper_model_size}")
    whisper_model = whisper.load_model(whisper_model_size)
    
    print("Loading speaker diarization model...")
    print("Note: This requires a Hugging Face token for pyannote models.")
    print("You can get one free at: https://huggingface.co/settings/tokens")
    
    try:
        # Try to load the diarization pipeline
        diarization_pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=None  # Will use HF_TOKEN environment variable if set
        )
    except Exception as e:
        print(f"Warning: Could not load speaker diarization model: {e}")
        print("Falling back to simple speaker detection...")
        diarization_pipeline = None
    
    return whisper_model, diarization_pipeline

def simple_speaker_detection(segments, num_speakers=2):
    """
    Simple speaker detection based on audio characteristics when diarization fails
    This is a fallback method that alternates speakers based on silence gaps
    """
    speakers = []
    current_speaker = 0
    
    for i, segment in enumerate(segments):
        # Simple heuristic: alternate speakers on longer pauses
        if i > 0:
            gap = segment['start'] - segments[i-1]['end']
            if gap > 2.0:  # 2 second gap suggests speaker change
                current_speaker = 1 - current_speaker
        
        speakers.append(f"Speaker {current_speaker + 1}")
    
    return speakers

def perform_diarization(audio_file, diarization_pipeline):
    """
    Perform speaker diarization on the audio file
    """
    if diarization_pipeline is None:
        return None
    
    try:
        print("Performing speaker diarization...")
        with ProgressHook() as hook:
            diarization = diarization_pipeline(audio_file, hook=hook)
        return diarization
    except Exception as e:
        print(f"Diarization failed: {e}")
        return None

def align_transcription_with_speakers(whisper_result, diarization):
    """
    Align Whisper transcription segments with speaker diarization
    """
    if diarization is None:
        # Fallback to simple detection
        return simple_speaker_detection(whisper_result['segments'])
    
    aligned_segments = []
    
    for segment in whisper_result['segments']:
        segment_start = segment['start']
        segment_end = segment['end']
        segment_mid = (segment_start + segment_end) / 2
        
        # Find which speaker is active at the midpoint of this segment
        active_speaker = None
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            if turn.start <= segment_mid <= turn.end:
                active_speaker = speaker
                break
        
        if active_speaker is None:
            active_speaker = "Unknown"
        
        aligned_segments.append(active_speaker)
    
    return aligned_segments

def transcribe_with_speakers(audio_file_path, whisper_model_size="base", num_speakers=2):
    """
    Transcribe audio with speaker separation
    """
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
    
    # Load models
    whisper_model, diarization_pipeline = load_models(whisper_model_size)
    
    # Transcribe with Whisper
    print(f"Transcribing audio: {audio_file_path}")
    whisper_result = whisper_model.transcribe(audio_file_path)
    
    # Perform speaker diarization
    diarization = perform_diarization(audio_file_path, diarization_pipeline)
    
    # Align transcription with speakers
    print("Aligning transcription with speakers...")
    speakers = align_transcription_with_speakers(whisper_result, diarization)
    
    # Create enhanced result with speaker information
    enhanced_result = {
        'text': whisper_result['text'],
        'segments': [],
        'language': whisper_result.get('language', 'unknown')
    }
    
    for i, segment in enumerate(whisper_result['segments']):
        enhanced_segment = segment.copy()
        enhanced_segment['speaker'] = speakers[i] if i < len(speakers) else "Unknown"
        enhanced_result['segments'].append(enhanced_segment)
    
    return enhanced_result

def save_speaker_transcription(result, audio_file_path, output_format="txt"):
    """
    Save transcription with speaker labels
    """
    audio_path = Path(audio_file_path)
    base_name = audio_path.stem
    output_dir = audio_path.parent
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if output_format == "txt":
        output_file = output_dir / f"{base_name}_speakers_transcript_{timestamp}.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("AUDIO TRANSCRIPTION WITH SPEAKER SEPARATION\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Source File: {audio_file_path}\n")
            f.write(f"Transcribed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model Used: Whisper AI + Speaker Diarization\n")
            f.write(f"Language: {result.get('language', 'unknown')}\n\n")
            
            f.write("TRANSCRIPT BY SPEAKER:\n")
            f.write("-" * 30 + "\n\n")
            
            current_speaker = None
            for segment in result['segments']:
                speaker = segment.get('speaker', 'Unknown')
                text = segment['text'].strip()
                start_time = segment['start']
                end_time = segment['end']
                
                # Add speaker header when speaker changes
                if speaker != current_speaker:
                    f.write(f"\n[{speaker}] ({format_time(start_time)} - {format_time(end_time)}):\n")
                    current_speaker = speaker
                
                f.write(f"{text} ")
            
            f.write("\n\n" + "=" * 60 + "\n")
            f.write("DETAILED TIMELINE:\n")
            f.write("-" * 20 + "\n\n")
            
            for segment in result['segments']:
                speaker = segment.get('speaker', 'Unknown')
                text = segment['text'].strip()
                start_time = format_time(segment['start'])
                end_time = format_time(segment['end'])
                
                f.write(f"[{start_time} - {end_time}] {speaker}: {text}\n")
                
    elif output_format == "srt":
        output_file = output_dir / f"{base_name}_speakers_transcript_{timestamp}.srt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(result['segments'], 1):
                speaker = segment.get('speaker', 'Unknown')
                text = segment['text'].strip()
                start_time = format_timestamp_srt(segment['start'])
                end_time = format_timestamp_srt(segment['end'])
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"[{speaker}] {text}\n\n")
    
    print(f"Speaker-separated transcription saved to: {output_file}")
    return output_file

def format_time(seconds):
    """Format seconds to MM:SS format"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def format_timestamp_srt(seconds):
    """Format timestamp for SRT subtitle format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio with speaker separation")
    parser.add_argument("audio_file", help="Path to the audio file to transcribe")
    parser.add_argument("--model", "-m", default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size (default: base)")
    parser.add_argument("--format", "-f", default="txt",
                       choices=["txt", "srt"],
                       help="Output format (default: txt)")
    parser.add_argument("--speakers", "-s", type=int, default=2,
                       help="Expected number of speakers (default: 2)")
    
    args = parser.parse_args()
    
    try:
        # Check for Hugging Face token
        if not os.getenv('HF_TOKEN'):
            print("\nIMPORTANT: For best speaker separation results, set your Hugging Face token:")
            print("1. Get a free token at: https://huggingface.co/settings/tokens")
            print("2. Set it as environment variable: export HF_TOKEN=your_token_here")
            print("3. Or create a .env file with: HF_TOKEN=your_token_here")
            print("\nProceeding with fallback speaker detection...\n")
        
        # Transcribe with speaker separation
        result = transcribe_with_speakers(args.audio_file, args.model, args.speakers)
        
        # Save the transcription
        output_file = save_speaker_transcription(result, args.audio_file, args.format)
        
        # Print summary
        print("\n" + "=" * 60)
        print("SPEAKER-SEPARATED TRANSCRIPTION COMPLETE")
        print("=" * 60)
        print(f"Input file: {args.audio_file}")
        print(f"Output file: {output_file}")
        print(f"Model used: {args.model}")
        print(f"Expected speakers: {args.speakers}")
        print(f"Text length: {len(result['text'])} characters")
        print(f"Total segments: {len(result['segments'])}")
        
        # Show speaker summary
        speakers = set(seg.get('speaker', 'Unknown') for seg in result['segments'])
        print(f"Detected speakers: {', '.join(sorted(speakers))}")
        
        # Show preview
        preview_segments = result['segments'][:3]
        print(f"\nPreview:")
        for segment in preview_segments:
            speaker = segment.get('speaker', 'Unknown')
            text = segment['text'].strip()[:100]
            if len(segment['text']) > 100:
                text += "..."
            print(f"  [{speaker}]: {text}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

