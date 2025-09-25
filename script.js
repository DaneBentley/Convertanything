// ConvertAnything - AI Audio Transcription Web App
// Main JavaScript functionality

class AudioTranscriber {
    constructor() {
        this.currentFile = null;
        this.transcriptionResult = null;
        this.isProcessing = false;
        
        this.initializeElements();
        this.bindEvents();
        this.initializeApp();
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

    initializeApp() {
        // Initialize with backend API - supports both local and Vercel deployment
        this.apiUrl = this.getApiUrl();
        console.log('Initializing ConvertAnything with backend API at:', this.apiUrl);
        
        // Test API connection on startup
        this.testApiConnection();
    }
    
    getApiUrl() {
        // Auto-detect API URL based on environment
        const hostname = window.location.hostname;
        const port = window.location.port;
        
        // If running on Vercel or production domain
        if (hostname.includes('vercel.app') || (hostname !== 'localhost' && hostname !== '127.0.0.1')) {
            return `${window.location.protocol}//${hostname}/api`;
        }
        
        // Local development - check if custom port is specified
        if (port === '8000') {
            // Frontend on 8000, backend likely on 5000
            return 'http://localhost:5000/api';
        }
        
        // Default to same origin with /api path
        return `${window.location.protocol}//${hostname}${port ? ':' + port : ''}/api`;
    }

    async testApiConnection() {
        try {
            const response = await fetch(`${this.apiUrl}/health`);
            if (response.ok) {
                console.log('✓ Backend API is available');
                this.showStatus('Backend connected successfully', 'success');
            } else {
                throw new Error('API not responding');
            }
        } catch (error) {
            console.error('❌ Backend API connection failed:', error);
            this.showError('Backend API not available. Please ensure the Python backend is running on port 5000.');
        }
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
        // Reset any previous error states
        this.clearErrors();
        
        // Validate file type
        const validTypes = ['audio/mpeg', 'audio/wav', 'audio/mp4', 'audio/m4a', 'audio/flac', 'audio/ogg'];
        const validExtensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.mp4'];
        
        const fileName = file.name.toLowerCase();
        const hasValidExtension = validExtensions.some(ext => fileName.endsWith(ext));
        const hasValidMimeType = validTypes.some(type => file.type.startsWith('audio/') || file.type.startsWith('video/'));
        
        if (!hasValidExtension && !hasValidMimeType) {
            this.showError('Please select a valid audio file. Supported formats: MP3, WAV, M4A, FLAC, OGG');
            return;
        }

        // Validate file size (100MB limit)
        const maxSize = 100 * 1024 * 1024; // 100MB
        if (file.size > maxSize) {
            this.showError(`File size must be less than ${Math.round(maxSize / (1024 * 1024))}MB. Your file is ${this.formatFileSize(file.size)}.`);
            return;
        }
        
        // Check for minimum file size (avoid empty files)
        if (file.size < 1024) { // 1KB minimum
            this.showError('File appears to be too small or empty. Please select a valid audio file.');
            return;
        }

        this.currentFile = file;
        this.displayFileInfo(file);
        this.showOptionsSection();
        this.showStatus('File loaded successfully. Configure options and start transcription.', 'success');
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
    
    hideProcessingSection() {
        this.processingSection.style.display = 'none';
        this.optionsSection.style.display = 'block';
    }

    showResultsSection() {
        this.processingSection.style.display = 'none';
        this.resultsSection.style.display = 'block';
    }

    toggleSpeakerOptions() {
        const isEnabled = this.speakerToggle.checked;
        this.speakerCountGroup.style.display = isEnabled ? 'block' : 'none';
    }

    // Utility methods
    clearErrors() {
        // Remove any existing error notifications
        const errorNotifications = document.querySelectorAll('.notification-error');
        errorNotifications.forEach(notification => notification.remove());
        
        // Clear error states from form elements
        const errorElements = document.querySelectorAll('.file-input-error, .error');
        errorElements.forEach(element => {
            element.classList.remove('file-input-error', 'error');
        });
    }
    
    validateSettings() {
        let isValid = true;
        
        // Validate model selection
        if (!this.modelSelect.value) {
            this.modelSelect.parentElement.classList.add('error');
            isValid = false;
        }
        
        // Validate speaker count if speaker separation is enabled
        if (this.speakerToggle.checked && !this.speakerCount.value) {
            this.speakerCount.parentElement.classList.add('error');
            isValid = false;
        }
        
        return isValid;
    }
    
    // Transcription process
    async startTranscription() {
        if (!this.currentFile || this.isProcessing) return;
        
        // Validate settings
        if (!this.validateSettings()) {
            this.showError('Please check your settings and try again.');
            return;
        }

        this.isProcessing = true;
        this.transcribeBtn.disabled = true;
        this.showProcessingSection();
        
        try {
            await this.runTranscription();
        } catch (error) {
            console.error('Transcription error:', error);
            this.showError('Transcription failed: ' + error.message);
            // Return to options section on error
            this.hideProcessingSection();
        } finally {
            this.isProcessing = false;
            this.transcribeBtn.disabled = false;
        }
    }

    async runTranscription() {
        // Create form data for API request
        const formData = new FormData();
        formData.append('audio', this.currentFile);
        formData.append('model', this.modelSelect.value);
        formData.append('speaker_separation', this.speakerToggle.checked);
        formData.append('speaker_count', this.speakerCount.value);

        try {
            // Update progress
            this.updateProgress(5, 'Uploading file to server...');
            
            // Create abort controller for request timeout
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minute timeout
            
            // Make API request with timeout
            const response = await fetch(`${this.apiUrl}/transcribe`, {
                method: 'POST',
                body: formData,
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                let errorMessage = 'Transcription service unavailable';
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.error || errorMessage;
                } catch (e) {
                    // If we can't parse error response, use status text
                    errorMessage = response.statusText || errorMessage;
                }
                throw new Error(errorMessage);
            }
            
            this.updateProgress(15, 'Processing with AI models...');
            
            // Parse response
            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error || 'Transcription failed');
            }
            
            // Simulate progress updates for better UX
            await this.simulateProgress();
            
            // Set result
            this.transcriptionResult = data.result;
            this.updateProgress(100, 'Complete!');
            
            // Brief delay to show completion
            await this.delay(500);
            
            // Display results
            this.displayResults();
            
        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('Request timed out. Please try with a smaller file or check your connection.');
            }
            console.error('Transcription failed:', error);
            throw error;
        }
    }

    async simulateProgress() {
        // Simulate processing progress for better UX
        const steps = [
            { progress: 30, status: 'Running speech recognition...' },
            { progress: 60, status: 'Analyzing audio patterns...' },
            { progress: 80, status: 'Separating speakers...' },
            { progress: 95, status: 'Finalizing transcription...' }
        ];

        for (const step of steps) {
            this.updateProgress(step.progress, step.status);
            await this.delay(800);
        }
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
        // Create a proper error notification
        this.showNotification(message, 'error');
        
        // Also log to console for debugging
        console.error('ConvertAnything Error:', message);
    }
    
    showStatus(message, type = 'info') {
        this.showNotification(message, type);
    }
    
    showNotification(message, type = 'info') {
        // Remove existing notifications
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }
        
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas ${this.getNotificationIcon(type)}"></i>
                <span>${message}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds for non-error notifications
        if (type !== 'error') {
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 5000);
        }
    }
    
    getNotificationIcon(type) {
        switch (type) {
            case 'success': return 'fa-check-circle';
            case 'error': return 'fa-exclamation-circle';
            case 'warning': return 'fa-exclamation-triangle';
            default: return 'fa-info-circle';
        }
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

// Production initialization
console.log('ConvertAnything v1.0 - Production Build');
console.log('Backend API required on localhost:5000');
