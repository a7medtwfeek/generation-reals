from flask import Flask, render_template, request, jsonify, send_file
from pathlib import Path
import threading
import uuid
from final_generator import FinalVideoGenerator
from quran_api import QuranAPI
from config import OUTPUT_DIR

app = Flask(__name__)
app.config['SECRET_KEY'] = 'quran-final-generator'

# Storage for generation jobs
jobs = {}

# Initialize
quran_api = QuranAPI()
final_generator = FinalVideoGenerator()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/reciters', methods=['GET'])
def get_reciters():
    try:
        reciters = quran_api.get_reciters()
        formatted = [
            {'id': rec_id, 'name_ar': info['name_ar'], 'name_en': info['name_en']}
            for rec_id, info in reciters.items()
        ]
        return jsonify({'success': True, 'reciters': formatted})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/surahs', methods=['GET'])
def get_surahs():
    try:
        surahs = quran_api.get_surahs()
        formatted = [
            {'number': num, 'name': name}
            for num, name in surahs.items()
        ]
        return jsonify({'success': True, 'surahs': formatted})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/generate', methods=['POST'])
def generate_video():
    try:
        data = request.json
        reciter_id = data.get('reciter_id')
        surah_number = int(data.get('surah_number'))
        verse_start = int(data.get('verse_start'))
        verse_end = int(data.get('verse_end'))
        
        if not reciter_id or not surah_number:
            return jsonify({'success': False, 'error': 'المعطيات غير مكتملة'}), 400
        
        if verse_start < 1 or verse_end < verse_start:
            return jsonify({'success': False, 'error': 'أرقام الآيات غير صحيحة'}), 400
        
        job_id = str(uuid.uuid4())
        jobs[job_id] = {
            'status': 'processing',
            'progress': 0,
            'message': 'جاري البدء...',
            'video_path': None,
            'error': None
        }
        
        def generate_in_background():
            def progress_callback(progress, message):
                jobs[job_id]['progress'] = progress
                jobs[job_id]['message'] = message
            
            try:
                video_path = final_generator.generate(
                    reciter_id=reciter_id,
                    surah_number=surah_number,
                    verse_start=verse_start,
                    verse_end=verse_end,
                    progress_callback=progress_callback
                )
                
                if video_path:
                    jobs[job_id]['status'] = 'completed'
                    jobs[job_id]['video_path'] = str(video_path.name)
                    jobs[job_id]['progress'] = 100
                    jobs[job_id]['message'] = 'تم الانتهاء!'
                else:
                    jobs[job_id]['status'] = 'failed'
                    jobs[job_id]['error'] = 'فشل في إنشاء الفيديو'
            except Exception as e:
                jobs[job_id]['status'] = 'failed'
                jobs[job_id]['error'] = str(e)
        
        thread = threading.Thread(target=generate_in_background)
        thread.daemon = True
        thread.start()
        
        return jsonify({'success': True, 'job_id': job_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/progress/<job_id>', methods=['GET'])
def get_progress(job_id):
    if job_id not in jobs:
        return jsonify({'success': False, 'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    return jsonify({
        'success': True,
        'status': job['status'],
        'progress': job['progress'],
        'message': job['message'],
        'video_path': job['video_path'],
        'error': job['error']
    })


@app.route('/api/download/<filename>', methods=['GET'])
def download_video(filename):
    try:
        video_path = OUTPUT_DIR / filename
        if not video_path.exists():
            return jsonify({'success': False, 'error': 'Video not found'}), 404
        return send_file(video_path, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    import os
    
    print("=" * 70)
    print("مُولِّد فيديوهات آيات القرآن - النسخة النهائية")
    print("Final Quran Video Generator")
    print("=" * 70)
    print("\n✨ المميزات:")
    print("  ✓ نص عربي نظيف بدون placeholders")
    print("  ✓ كل آية = فيديو مستقل (ayah_1.mp4, ayah_2.mp4, ...)")
    print("  ✓ دمج تلقائي في فيديو نهائي واحد")
    print("  ✓ تنظيف تلقائي للملفات المؤقتة")
    
    # Get port from environment variable (for deployment platforms)
    port = int(os.environ.get('PORT', 5000))
    
    print(f"\nالخادم يعمل على: http://localhost:{port}")
    print("\nاضغط Ctrl+C للإيقاف\n")
    
    app.run(debug=False, host='0.0.0.0', port=port, threaded=True)

