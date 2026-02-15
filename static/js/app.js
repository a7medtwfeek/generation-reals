// ============================
// DOM Elements
// ============================
const videoForm = document.getElementById('videoForm');
const reciterSelect = document.getElementById('reciter');
const surahSelect = document.getElementById('surah');
const verseStartInput = document.getElementById('verseStart');
const verseEndInput = document.getElementById('verseEnd');
const generateBtn = document.getElementById('generateBtn');

const progressSection = document.getElementById('progressSection');
const progressBar = document.getElementById('progressBar');
const progressMessage = document.getElementById('progressMessage');
const progressPercentage = document.getElementById('progressPercentage');

const resultSection = document.getElementById('resultSection');
const videoPreview = document.getElementById('videoPreview');
const downloadBtn = document.getElementById('downloadBtn');
const createAnotherBtn = document.getElementById('createAnotherBtn');

const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const retryBtn = document.getElementById('retryBtn');

let currentJobId = null;
let progressInterval = null;

// ============================
// API Functions
// ============================

async function fetchReciters() {
    try {
        const response = await fetch('/api/reciters');
        const data = await response.json();
        
        if (data.success) {
            populateReciters(data.reciters);
        } else {
            console.error('Failed to fetch reciters:', data.error);
        }
    } catch (error) {
        console.error('Error fetching reciters:', error);
    }
}

async function fetchSurahs() {
    try {
        const response = await fetch('/api/surahs');
        const data = await response.json();
        
        if (data.success) {
            populateSurahs(data.surahs);
        } else {
            console.error('Failed to fetch surahs:', data.error);
        }
    } catch (error) {
        console.error('Error fetching surahs:', error);
    }
}

async function generateVideo(formData) {
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            return data.job_id;
        } else {
            throw new Error(data.error || 'فشل في إنشاء الفيديو');
        }
    } catch (error) {
        throw error;
    }
}

async function checkProgress(jobId) {
    try {
        const response = await fetch(`/api/progress/${jobId}`);
        const data = await response.json();
        
        if (data.success) {
            return data;
        } else {
            throw new Error(data.error || 'فشل في التحقق من التقدم');
        }
    } catch (error) {
        throw error;
    }
}

// ============================
// UI Functions
// ============================

function populateReciters(reciters) {
    reciterSelect.innerHTML = '<option value="">اختر القارئ...</option>';
    
    reciters.forEach(reciter => {
        const option = document.createElement('option');
        option.value = reciter.id;
        option.textContent = reciter.name_ar;
        reciterSelect.appendChild(option);
    });
}

function populateSurahs(surahs) {
    surahSelect.innerHTML = '<option value="">اختر السورة...</option>';
    
    surahs.forEach(surah => {
        const option = document.createElement('option');
        option.value = surah.number;
        option.textContent = `${surah.number}. ${surah.name}`;
        surahSelect.appendChild(option);
    });
}

function showSection(section) {
    // Hide all sections
    progressSection.classList.add('hidden');
    resultSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    
    // Show requested section
    if (section === 'progress') {
        progressSection.classList.remove('hidden');
    } else if (section === 'result') {
        resultSection.classList.remove('hidden');
    } else if (section === 'error') {
        errorSection.classList.remove('hidden');
    }
}

function updateProgress(progress, message) {
    progressBar.style.width = `${progress}%`;
    progressPercentage.textContent = `${progress}%`;
    progressMessage.textContent = message;
}

function showError(message) {
    errorMessage.textContent = message;
    showSection('error');
}

function showSuccess(videoPath) {
    // Create video element
    const video = document.createElement('video');
    video.controls = true;
    video.src = `/api/download/${videoPath}`;
    
    videoPreview.innerHTML = '';
    videoPreview.appendChild(video);
    
    // Update download button
    downloadBtn.href = `/api/download/${videoPath}`;
    downloadBtn.download = videoPath;
    
    showSection('result');
}

function resetForm() {
    videoForm.reset();
    showSection(null);
    generateBtn.disabled = false;
    
    // Clear progress interval if exists
    if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
    }
}

// ============================
// Event Handlers
// ============================

videoForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Get form data
    const formData = {
        reciter_id: reciterSelect.value,
        surah_number: parseInt(surahSelect.value),
        verse_start: parseInt(verseStartInput.value),
        verse_end: parseInt(verseEndInput.value)
    };
    
    // Validate
    if (!formData.reciter_id || !formData.surah_number) {
        showError('الرجاء ملء جميع الحقول المطلوبة');
        return;
    }
    
    if (formData.verse_start < 1 || formData.verse_end < formData.verse_start) {
        showError('أرقام الآيات غير صحيحة');
        return;
    }
    
    // Disable button
    generateBtn.disabled = true;
    
    // Show progress
    showSection('progress');
    updateProgress(0, 'جاري البدء...');
    
    try {
        // Start generation
        currentJobId = await generateVideo(formData);
        
        // Poll for progress
        progressInterval = setInterval(async () => {
            try {
                const progressData = await checkProgress(currentJobId);
                
                updateProgress(progressData.progress, progressData.message);
                
                if (progressData.status === 'completed') {
                    clearInterval(progressInterval);
                    progressInterval = null;
                    showSuccess(progressData.video_path);
                    generateBtn.disabled = false;
                } else if (progressData.status === 'failed') {
                    clearInterval(progressInterval);
                    progressInterval = null;
                    showError(progressData.error || 'فشل في إنشاء الفيديو');
                    generateBtn.disabled = false;
                }
            } catch (error) {
                clearInterval(progressInterval);
                progressInterval = null;
                showError('حدث خطأ أثناء التحقق من التقدم');
                generateBtn.disabled = false;
            }
        }, 1000); // Check every second
        
    } catch (error) {
        showError(error.message || 'حدث خطأ غير متوقع');
        generateBtn.disabled = false;
    }
});

createAnotherBtn.addEventListener('click', () => {
    resetForm();
});

retryBtn.addEventListener('click', () => {
    resetForm();
});

// Auto-update verse end when start changes
verseStartInput.addEventListener('change', () => {
    const startValue = parseInt(verseStartInput.value);
    const endValue = parseInt(verseEndInput.value);
    
    if (endValue < startValue) {
        verseEndInput.value = startValue;
    }
});

// ============================
// Initialization
// ============================

document.addEventListener('DOMContentLoaded', () => {
    console.log('مُولِّد فيديوهات آيات القرآن - Loaded');
    
    // Load initial data
    fetchReciters();
    fetchSurahs();
});
