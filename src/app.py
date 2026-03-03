"""
Flask 메인 애플리케이션
웹 인터페이스 및 API 엔드포인트
"""

from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import os
import sys
from datetime import datetime
from werkzeug.utils import secure_filename

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(__file__))

from excel_parser import parse_excel_file
from excel_parser_multi_date import parse_multi_date_excel, get_latest_and_previous_tests
from report_analyzer import analyze_test_results
from report_generator import generate_report
from comparison import compare_test_results, generate_comparison_summary

app = Flask(__name__)
app.config['SECRET_KEY'] = 'medical-report-generator-2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 업로드 및 출력 디렉토리 설정
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'output')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# 허용된 파일 확장자
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}


def allowed_file(filename):
    """파일 확장자 검사"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """파일 업로드 및 처리"""
    try:
        # 파일 확인
        if 'file' not in request.files:
            return jsonify({'error': '파일이 업로드되지 않았습니다.'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '지원하지 않는 파일 형식입니다. (.xlsx, .xls만 가능)'}), 400
        
        # 파일 저장
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 먼저 다중 날짜 파일인지 확인
        multi_date_data = parse_multi_date_excel(filepath)
        
        comparison_data = None
        comparison_summary = None
        parsed_data = None
        
        if multi_date_data:
            # 다중 날짜 파일인 경우
            print(f"✅ 다중 날짜 파일 감지: {len(multi_date_data['dates'])}개 날짜")
            
            # 최신 및 이전 검사 추출
            current_tests, previous_tests = get_latest_and_previous_tests(multi_date_data)
            
            if current_tests and previous_tests:
                print(f"📊 자동 비교: 최신({len(current_tests)}개) vs 이전({len(previous_tests)}개)")
                
                # 비교 수행
                comparison_data = compare_test_results(
                    current_tests=current_tests,
                    previous_tests=previous_tests
                )
                comparison_summary = generate_comparison_summary(comparison_data)
            
            # parsed_data 형식으로 변환
            parsed_data = {
                'tests': current_tests if current_tests else [],
                'patient_info': multi_date_data['patient_info']
            }
        else:
            # 기존 단일 결과 파일
            print("📋 단일 결과 파일")
            parsed_data = parse_excel_file(filepath)
        
        # 이전 검사 파일 처리 (별도 파일이 업로드된 경우, 다중 날짜가 아닐 때만)
        if not multi_date_data and 'prev_file' in request.files:
            prev_file = request.files['prev_file']
            if prev_file.filename != '' and allowed_file(prev_file.filename):
                # 이전 파일 저장
                prev_filename = secure_filename(prev_file.filename)
                prev_filename = f"{timestamp}_prev_{prev_filename}"
                prev_filepath = os.path.join(app.config['UPLOAD_FOLDER'], prev_filename)
                prev_file.save(prev_filepath)
                
                # 이전 파일 파싱
                prev_parsed_data = parse_excel_file(prev_filepath)
                
                # 검사 결과 비교
                comparison_data = compare_test_results(
                    current_tests=parsed_data['tests'],
                    previous_tests=prev_parsed_data['tests']
                )
                comparison_summary = generate_comparison_summary(comparison_data)
        
        # 당뇨 유무 확인
        has_diabetes = request.form.get('has_diabetes') == '1'
        
        # 검사 결과 분석 (당뇨 유무 전달)
        analysis = analyze_test_results(parsed_data['tests'], has_diabetes=has_diabetes)
        
        # 환자 정보 가져오기
        patient_info = parsed_data['patient_info']
        
        # 폼 데이터에서 추가 정보 가져오기
        if request.form.get('patient_name'):
            patient_info['name'] = request.form.get('patient_name')
        if request.form.get('patient_age'):
            patient_info['age'] = request.form.get('patient_age')
        if request.form.get('patient_gender'):
            patient_info['gender'] = request.form.get('patient_gender')
        if request.form.get('patient_id'):
            patient_info['id'] = request.form.get('patient_id')
        
        # 의료진 코멘트
        doctor_comment = request.form.get('doctor_comment', '')
        
        # 권장사항 포함 여부
        include_recommendations = request.form.get('include_recommendations') == '1'
        
        # 출력 형식
        output_format = request.form.get('output_format', 'pdf')
        
        # 리포트 생성
        output_file = generate_report(
            analysis_data=analysis,
            patient_info=patient_info,
            doctor_comment=doctor_comment,
            output_format=output_format,
            output_dir=app.config['OUTPUT_FOLDER'],
            include_recommendations=include_recommendations,
            comparison_data=comparison_data,
            comparison_summary=comparison_summary
        )
        
        # 생성된 파일 반환
        return send_file(
            output_file,
            as_attachment=True,
            download_name=os.path.basename(output_file)
        )
    
    except Exception as e:
        return jsonify({'error': f'처리 중 오류가 발생했습니다: {str(e)}'}), 500


@app.route('/preview', methods=['POST'])
def preview_report():
    """리포트 미리보기"""
    try:
        # 파일 확인
        if 'file' not in request.files:
            return jsonify({'error': '파일이 업로드되지 않았습니다.'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '지원하지 않는 파일 형식입니다.'}), 400
        
        # 파일 저장
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 먼저 다중 날짜 파일인지 확인
        multi_date_data = parse_multi_date_excel(filepath)
        
        comparison_summary = None
        parsed_data = None
        
        if multi_date_data:
            # 다중 날짜 파일인 경우
            current_tests, previous_tests = get_latest_and_previous_tests(multi_date_data)
            
            if current_tests and previous_tests:
                comparison_data = compare_test_results(
                    current_tests=current_tests,
                    previous_tests=previous_tests
                )
                comparison_summary = generate_comparison_summary(comparison_data)
            
            parsed_data = {
                'tests': current_tests if current_tests else [],
                'patient_info': multi_date_data['patient_info']
            }
        else:
            # 기존 단일 결과 파일
            parsed_data = parse_excel_file(filepath)
        
        # 이전 검사 파일 처리 (미리보기용, 선택적, 단일 결과 파일인 경우만)
        if not multi_date_data and 'prev_file' in request.files:
            prev_file = request.files['prev_file']
            if prev_file.filename != '' and allowed_file(prev_file.filename):
                prev_filename = secure_filename(prev_file.filename)
                prev_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                prev_filename = f"{prev_timestamp}_prev_{prev_filename}"
                prev_filepath = os.path.join(app.config['UPLOAD_FOLDER'], prev_filename)
                prev_file.save(prev_filepath)
                
                prev_parsed_data = parse_excel_file(prev_filepath)
                comparison_data = compare_test_results(
                    current_tests=parsed_data['tests'],
                    previous_tests=prev_parsed_data['tests']
                )
                comparison_summary = generate_comparison_summary(comparison_data)
        
        # 당뇨 유무는 미리보기에서 확인 불가 (기본값: False)
        has_diabetes = False
        
        # 검사 결과 분석 (당뇨 유무 전달)
        analysis = analyze_test_results(parsed_data['tests'], has_diabetes=has_diabetes)
        
        # 분석 결과 반환
        response_data = {
            'success': True,
            'patient_info': parsed_data['patient_info'],
            'summary': analysis['summary'],
            'grouped_tests': {
                k: {
                    'info': v['info'],
                    'tests': v['tests'],
                    'abnormal_count': v['abnormal_count']
                }
                for k, v in analysis['grouped_tests'].items()
            },
            'recommendations': analysis['recommendations'],
            'filename': filename
        }
        
        # 비교 요약이 있으면 추가
        if comparison_summary:
            response_data['comparison_summary'] = comparison_summary
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': f'미리보기 생성 중 오류: {str(e)}'}), 500


@app.route('/health')
def health():
    """헬스 체크"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


if __name__ == '__main__':
    print("=" * 60)
    print("🏥 의료 검사 리포트 생성기 시작")
    print("=" * 60)
    print(f"📁 업로드 폴더: {UPLOAD_FOLDER}")
    print(f"📁 출력 폴더: {OUTPUT_FOLDER}")
    print("🌐 서버 주소: http://localhost:5000")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
