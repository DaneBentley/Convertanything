// ConvertAnything - AI Audio Transcription Web App
// Main JavaScript functionality

class AudioTranscriber {
    constructor() {
        this.currentFile = null;
        this.transcriptionResult = null;
        this.isProcessing = false;
        
        this.initializeElements();
        this.bindEvents();
        this.initializeDemo();
    }

    initializeElements() {
        // Upload elements
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.uploadSection = document.getElementById('uploadSection');
        
        // Options elements
        this.optionsSection = document.getElementById('optionsSection');
        this.fileInfo = document.getElementById('fileInfo');
        this.fileName = document.getElementById('fileName');
        this.fileSize = document.getElementById('fileSize');
        this.removeFileBtn = document.getElementById('removeFile');
        this.modelSelect = document.getElementById('modelSelect');
        this.speakerToggle = document.getElementById('speakerToggle');
        this.speakerCount = document.getElementById('speakerCount');
        this.speakerCountGroup = document.getElementById('speakerCountGroup');
        this.transcribeBtn = document.getElementById('transcribeBtn');
        
        // Processing elements
        this.processingSection = document.getElementById('processingSection');
        this.processingStatus = document.getElementById('processingStatus');
        this.progressFill = document.getElementById('progressFill');
        this.progressPercent = document.getElementById('progressPercent');
        this.estimatedTime = document.getElementById('estimatedTime');
        
        // Results elements
        this.resultsSection = document.getElementById('resultsSection');
        this.audioDuration = document.getElementById('audioDuration');
        this.speakersDetected = document.getElementById('speakersDetected');
        this.wordCount = document.getElementById('wordCount');
        this.transcriptContent = document.getElementById('transcriptContent');
        this.tabBtns = document.querySelectorAll('.tab-btn');
        this.exportBtns = document.querySelectorAll('.export-btn');
        this.newTranscriptionBtn = document.getElementById('newTranscriptionBtn');
    }

    bindEvents() {
        // Upload events
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.uploadArea.addEventListener('dragover', this.handleDragOver.bind(this));
        this.uploadArea.addEventListener('dragleave', this.handleDragLeave.bind(this));
        this.uploadArea.addEventListener('drop', this.handleDrop.bind(this));
        this.fileInput.addEventListener('change', this.handleFileSelect.bind(this));
        
        // Options events
        this.removeFileBtn.addEventListener('click', this.removeFile.bind(this));
        this.speakerToggle.addEventListener('change', this.toggleSpeakerOptions.bind(this));
        this.transcribeBtn.addEventListener('click', this.startTranscription.bind(this));
        
        // Results events
        this.tabBtns.forEach(btn => {
            btn.addEventListener('click', () => this.switchTab(btn.dataset.tab));
        });
        this.exportBtns.forEach(btn => {
            btn.addEventListener('click', () => this.exportTranscript(btn.dataset.format));
        });
        this.newTranscriptionBtn.addEventListener('click', this.resetApp.bind(this));
    }

    initializeDemo() {
        // Load demo data if no real transcription service is available
        this.demoMode = true;
        console.log('Demo mode initialized - using sample transcription data');
    }

    // File handling methods
    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('drag-over');
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('drag-over');
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    processFile(file) {
        // Validate file type
        const validTypes = ['audio/mpeg', 'audio/wav', 'audio/mp4', 'audio/m4a', 'audio/flac', 'audio/ogg'];
        if (!validTypes.some(type => file.type.startsWith('audio/'))) {
            this.showError('Please select a valid audio file (MP3, WAV, M4A, FLAC, OGG)');
            return;
        }

        // Validate file size (100MB limit for demo)
        if (file.size > 100 * 1024 * 1024) {
            this.showError('File size must be less than 100MB');
            return;
        }

        this.currentFile = file;
        this.displayFileInfo(file);
        this.showOptionsSection();
    }

    displayFileInfo(file) {
        this.fileName.textContent = file.name;
        this.fileSize.textContent = this.formatFileSize(file.size);
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    removeFile() {
        this.currentFile = null;
        this.fileInput.value = '';
        this.hideOptionsSection();
    }

    // UI state management
    showOptionsSection() {
        this.uploadSection.style.display = 'none';
        this.optionsSection.style.display = 'block';
    }

    hideOptionsSection() {
        this.uploadSection.style.display = 'block';
        this.optionsSection.style.display = 'none';
    }

    showProcessingSection() {
        this.optionsSection.style.display = 'none';
        this.processingSection.style.display = 'block';
    }

    showResultsSection() {
        this.processingSection.style.display = 'none';
        this.resultsSection.style.display = 'block';
    }

    toggleSpeakerOptions() {
        const isEnabled = this.speakerToggle.checked;
        this.speakerCountGroup.style.display = isEnabled ? 'block' : 'none';
    }

    // Transcription process
    async startTranscription() {
        if (!this.currentFile || this.isProcessing) return;

        this.isProcessing = true;
        this.showProcessingSection();
        
        try {
            if (this.demoMode) {
                await this.runDemoTranscription();
            } else {
                await this.runRealTranscription();
            }
        } catch (error) {
            this.showError('Transcription failed: ' + error.message);
        } finally {
            this.isProcessing = false;
        }
    }

    async runDemoTranscription() {
        const steps = [
            { status: 'Loading AI models...', progress: 10 },
            { status: 'Processing audio file...', progress: 30 },
            { status: 'Running speech recognition...', progress: 60 },
            { status: 'Separating speakers...', progress: 80 },
            { status: 'Finalizing transcription...', progress: 95 },
            { status: 'Complete!', progress: 100 }
        ];

        for (let i = 0; i < steps.length; i++) {
            const step = steps[i];
            this.updateProgress(step.progress, step.status);
            await this.delay(1500);
        }

        // Generate demo transcript based on the sample data
        this.transcriptionResult = this.generateDemoTranscript();
        this.displayResults();
    }

    generateDemoTranscript() {
        // Use the actual Spotify transcript data structure
        return {
            text: "This is a demo transcription. In a real implementation, this would contain the full transcribed text from your audio file using OpenAI Whisper AI technology.",
            duration: 1245, // ~20 minutes
            language: 'en',
            segments: [
                {
                    start: 0,
                    end: 4,
                    text: "Welcome to ConvertAnything, the AI-powered audio transcription service.",
                    speaker: "Speaker 1"
                },
                {
                    start: 4,
                    end: 8,
                    text: "This demo shows how your transcription would appear with speaker separation.",
                    speaker: "Speaker 2"
                },
                {
                    start: 8,
                    end: 12,
                    text: "The system uses OpenAI Whisper for speech recognition and Pyannote for speaker diarization.",
                    speaker: "Speaker 1"
                },
                {
                    start: 12,
                    end: 16,
                    text: "You can export your results in multiple formats including text, JSON, CSV, subtitles, and PDF.",
                    speaker: "Speaker 2"
                },
                {
                    start: 16,
                    end: 20,
                    text: "The interface is designed to be clean, modern, and easy to use for all your transcription needs.",
                    speaker: "Speaker 1"
                }
            ]
        };
    }

    async runRealTranscription() {
        // This would integrate with your Python backend
        // For now, showing the structure for future implementation
        
        const formData = new FormData();
        formData.append('audio', this.currentFile);
        formData.append('model', this.modelSelect.value);
        formData.append('speaker_separation', this.speakerToggle.checked);
        formData.append('speaker_count', this.speakerCount.value);

        // Example API call structure:
        /*
        const response = await fetch('/api/transcribe', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Transcription service unavailable');
        }
        
        this.transcriptionResult = await response.json();
        */
        
        // For now, fall back to demo
        await this.runDemoTranscription();
    }

    updateProgress(percent, status) {
        this.progressFill.style.width = `${percent}%`;
        this.progressPercent.textContent = `${percent}%`;
        this.processingStatus.textContent = status;
        
        if (percent < 100) {
            const remaining = Math.max(1, Math.floor((100 - percent) * 0.3));
            this.estimatedTime.textContent = `~${remaining}s remaining`;
        } else {
            this.estimatedTime.textContent = 'Complete!';
        }
    }

    displayResults() {
        const result = this.transcriptionResult;
        
        // Update stats
        this.audioDuration.textContent = this.formatDuration(result.duration);
        this.speakersDetected.textContent = this.getSpeakerCount(result.segments);
        this.wordCount.textContent = this.getWordCount(result.text);
        
        // Show results section
        this.showResultsSection();
        
        // Display initial tab (formatted)
        this.switchTab('formatted');
    }

    getSpeakerCount(segments) {
        const speakers = new Set(segments.map(s => s.speaker));
        return speakers.size;
    }

    getWordCount(text) {
        return text.split(/\s+/).filter(word => word.length > 0).length;
    }

    formatDuration(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }

    // Tab switching
    switchTab(tabName) {
        // Update active tab
        this.tabBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });

        // Display appropriate content
        switch (tabName) {
            case 'formatted':
                this.displayFormattedTranscript();
                break;
            case 'timeline':
                this.displayTimelineTranscript();
                break;
            case 'raw':
                this.displayRawTranscript();
                break;
        }
    }

    displayFormattedTranscript() {
        const segments = this.transcriptionResult.segments;
        const speakerGroups = this.groupBySpeaker(segments);
        
        let html = '';
        for (const [speaker, speakerSegments] of Object.entries(speakerGroups)) {
            html += `
                <div class="speaker-section">
                    <div class="speaker-header">${speaker}</div>
                    <div class="speaker-text">
                        ${speakerSegments.map(s => s.text.trim()).join(' ')}
                    </div>
                </div>
            `;
        }
        
        this.transcriptContent.innerHTML = html;
    }

    displayTimelineTranscript() {
        const segments = this.transcriptionResult.segments;
        
        let html = '';
        segments.forEach(segment => {
            html += `
                <div class="timeline-entry">
                    <div class="timestamp">${this.formatTimestamp(segment.start)}</div>
                    <div class="timeline-speaker">${segment.speaker}</div>
                    <div class="timeline-text">${segment.text.trim()}</div>
                </div>
            `;
        });
        
        this.transcriptContent.innerHTML = html;
    }

    displayRawTranscript() {
        this.transcriptContent.innerHTML = `
            <div style="white-space: pre-wrap; line-height: 1.8;">
                ${this.transcriptionResult.text}
            </div>
        `;
    }

    groupBySpeaker(segments) {
        const groups = {};
        let currentSpeaker = null;
        
        segments.forEach(segment => {
            const speaker = segment.speaker;
            if (speaker !== currentSpeaker) {
                if (!groups[speaker]) {
                    groups[speaker] = [];
                }
                currentSpeaker = speaker;
            }
            groups[speaker].push(segment);
        });
        
        return groups;
    }

    formatTimestamp(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    // Export functionality
    async exportTranscript(format) {
        if (!this.transcriptionResult) return;

        const result = this.transcriptionResult;
        const fileName = this.currentFile ? 
            this.currentFile.name.replace(/\.[^/.]+$/, '') : 
            'transcript';

        switch (format) {
            case 'txt':
                this.exportAsText(result, fileName);
                break;
            case 'json':
                this.exportAsJSON(result, fileName);
                break;
            case 'csv':
                this.exportAsCSV(result, fileName);
                break;
            case 'srt':
                this.exportAsSRT(result, fileName);
                break;
            case 'pdf':
                await this.exportAsPDF(result, fileName);
                break;
        }
    }

    exportAsText(result, fileName) {
        let content = 'AUDIO TRANSCRIPTION WITH SPEAKER SEPARATION\n';
        content += '='.repeat(60) + '\n\n';
        content += `Source File: ${this.currentFile?.name || 'demo-audio.mp3'}\n`;
        content += `Transcribed: ${new Date().toLocaleString()}\n`;
        content += `Model Used: Whisper AI + Speaker Diarization\n`;
        content += `Language: ${result.language || 'en'}\n\n`;
        content += 'TRANSCRIPT BY SPEAKER:\n';
        content += '-'.repeat(30) + '\n\n';

        const speakerGroups = this.groupBySpeakerForExport(result.segments);
        for (const [speaker, text] of Object.entries(speakerGroups)) {
            content += `[${speaker}]:\n${text}\n\n`;
        }

        content += '\n' + '='.repeat(60) + '\n';
        content += 'DETAILED TIMELINE:\n';
        content += '-'.repeat(20) + '\n\n';

        result.segments.forEach(segment => {
            const startTime = this.formatTimestamp(segment.start);
            const endTime = this.formatTimestamp(segment.end);
            content += `[${startTime} - ${endTime}] ${segment.speaker}: ${segment.text.trim()}\n`;
        });

        this.downloadFile(content, `${fileName}_transcript.txt`, 'text/plain');
    }

    exportAsJSON(result, fileName) {
        const exportData = {
            metadata: {
                sourceFile: this.currentFile?.name || 'demo-audio.mp3',
                transcribedAt: new Date().toISOString(),
                model: 'Whisper AI + Speaker Diarization',
                language: result.language || 'en',
                duration: result.duration,
                speakerCount: this.getSpeakerCount(result.segments),
                wordCount: this.getWordCount(result.text)
            },
            transcript: {
                fullText: result.text,
                segments: result.segments
            }
        };

        const content = JSON.stringify(exportData, null, 2);
        this.downloadFile(content, `${fileName}_transcript.json`, 'application/json');
    }

    exportAsCSV(result, fileName) {
        let content = 'Start Time,End Time,Speaker,Text\n';
        
        result.segments.forEach(segment => {
            const startTime = this.formatTimestamp(segment.start);
            const endTime = this.formatTimestamp(segment.end);
            const text = segment.text.trim().replace(/"/g, '""'); // Escape quotes
            content += `"${startTime}","${endTime}","${segment.speaker}","${text}"\n`;
        });

        this.downloadFile(content, `${fileName}_transcript.csv`, 'text/csv');
    }

    exportAsSRT(result, fileName) {
        let content = '';
        
        result.segments.forEach((segment, index) => {
            const startTime = this.formatSRTTimestamp(segment.start);
            const endTime = this.formatSRTTimestamp(segment.end);
            
            content += `${index + 1}\n`;
            content += `${startTime} --> ${endTime}\n`;
            content += `[${segment.speaker}] ${segment.text.trim()}\n\n`;
        });

        this.downloadFile(content, `${fileName}_transcript.srt`, 'text/plain');
    }

    async exportAsPDF(result, fileName) {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        
        // Title
        doc.setFontSize(20);
        doc.text('Audio Transcription', 20, 30);
        
        // Metadata
        doc.setFontSize(12);
        doc.text(`Source: ${this.currentFile?.name || 'demo-audio.mp3'}`, 20, 50);
        doc.text(`Date: ${new Date().toLocaleDateString()}`, 20, 60);
        doc.text(`Duration: ${this.formatDuration(result.duration)}`, 20, 70);
        doc.text(`Speakers: ${this.getSpeakerCount(result.segments)}`, 20, 80);
        
        // Transcript
        doc.setFontSize(10);
        let yPosition = 100;
        const pageHeight = doc.internal.pageSize.height;
        const margin = 20;
        const lineHeight = 6;
        
        result.segments.forEach(segment => {
            const startTime = this.formatTimestamp(segment.start);
            const speaker = segment.speaker;
            const text = segment.text.trim();
            
            // Check if we need a new page
            if (yPosition > pageHeight - 30) {
                doc.addPage();
                yPosition = 30;
            }
            
            // Speaker and timestamp
            doc.setFont(undefined, 'bold');
            doc.text(`[${startTime}] ${speaker}:`, margin, yPosition);
            
            // Text content
            doc.setFont(undefined, 'normal');
            const textLines = doc.splitTextToSize(text, 170);
            yPosition += lineHeight;
            
            textLines.forEach(line => {
                if (yPosition > pageHeight - 30) {
                    doc.addPage();
                    yPosition = 30;
                }
                doc.text(line, margin, yPosition);
                yPosition += lineHeight;
            });
            
            yPosition += lineHeight; // Extra space between segments
        });
        
        doc.save(`${fileName}_transcript.pdf`);
    }

    formatSRTTimestamp(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        const millisecs = Math.floor((seconds % 1) * 1000);
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')},${millisecs.toString().padStart(3, '0')}`;
    }

    groupBySpeakerForExport(segments) {
        const groups = {};
        
        segments.forEach(segment => {
            const speaker = segment.speaker;
            if (!groups[speaker]) {
                groups[speaker] = '';
            }
            groups[speaker] += segment.text.trim() + ' ';
        });
        
        // Clean up trailing spaces
        Object.keys(groups).forEach(speaker => {
            groups[speaker] = groups[speaker].trim();
        });
        
        return groups;
    }

    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        URL.revokeObjectURL(url);
    }

    // Utility methods
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    showError(message) {
        alert(message); // In production, use a proper modal/toast
    }

    resetApp() {
        this.currentFile = null;
        this.transcriptionResult = null;
        this.isProcessing = false;
        this.fileInput.value = '';
        
        // Reset UI
        this.resultsSection.style.display = 'none';
        this.processingSection.style.display = 'none';
        this.optionsSection.style.display = 'none';
        this.uploadSection.style.display = 'block';
        
        // Reset progress
        this.progressFill.style.width = '0%';
        this.progressPercent.textContent = '0%';
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AudioTranscriber();
});

// Service worker registration for PWA capabilities (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}
