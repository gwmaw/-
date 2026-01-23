"""
리포트 생성 모듈
HTML 템플릿 렌더링 및 PDF/PNG 출력
"""

from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os
import base64


class ReportGenerator:
    """검사 결과 리포트를 생성하는 클래스"""
    
    def __init__(self, template_dir):
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def generate_html(self, data, doctor_comment='', logo_path=''):
        """HTML 리포트 생성"""
        template = self.env.get_template('report_template.html')
        
        # 현재 날짜/시간
        now = datetime.now()
        
        # 로고 경로가 없으면 기본 경로 사용 (simple 버전)
        if not logo_path:
            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                    'assets', 'hospital_logo_simple.png')
        
        # 로고를 base64로 인코딩
        logo_base64 = ''
        if os.path.exists(logo_path):
            try:
                with open(logo_path, 'rb') as f:
                    logo_data = f.read()
                    logo_base64 = base64.b64encode(logo_data).decode('utf-8')
                    logo_base64 = f"data:image/png;base64,{logo_base64}"
            except Exception as e:
                print(f"⚠️  로고 로드 실패: {e}")
        
        # 템플릿 데이터 준비
        template_data = {
            'report_date': now.strftime('%Y년 %m월 %d일'),
            'generated_at': now.strftime('%Y-%m-%d %H:%M:%S'),
            'patient_name': data.get('patient_info', {}).get('name', '환자'),
            'patient_id': data.get('patient_info', {}).get('id', '-'),
            'patient_age': data.get('patient_info', {}).get('age', '-'),
            'patient_gender': data.get('patient_info', {}).get('gender', '-'),
            'test_date': data.get('patient_info', {}).get('date', now.strftime('%Y-%m-%d')),
            'grouped_tests': data['grouped_tests'],
            'summary': data['summary'],
            'recommendations': data.get('recommendations', []),
            'doctor_comment': doctor_comment,
            'logo_path': logo_base64
        }
        
        html_content = template.render(**template_data)
        return html_content
    
    def save_html(self, html_content, output_path):
        """HTML 파일 저장"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return output_path
    
    def generate_pdf(self, html_content, output_path):
        """PDF 생성 - WeasyPrint를 사용한 한글 지원"""
        try:
            # WeasyPrint 사용 (최신 버전, 한글 폰트 자동 임베딩)
            from weasyprint import HTML
            
            # HTML 문자열에서 직접 PDF 생성
            HTML(string=html_content).write_pdf(output_path)
            
            # 생성 성공 확인
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"✅ PDF 생성 성공: {output_path} ({file_size:,} bytes)")
                return output_path
            else:
                raise Exception("PDF 파일이 생성되지 않았습니다.")
            
        except ImportError as e:
            # WeasyPrint가 설치되지 않은 경우
            error_msg = (
                "WeasyPrint가 설치되지 않았습니다. "
                "다음 명령어로 설치하세요: pip install weasyprint"
            )
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
            
        except Exception as e:
            # 기타 오류 발생 시
            import traceback
            print(f"❌ PDF 생성 오류:")
            traceback.print_exc()
            
            # HTML 파일로라도 저장
            html_path = output_path.replace('.pdf', '.html')
            try:
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"💾 대체 출력: HTML 파일 저장됨 - {html_path}")
                print(f"   브라우저에서 열어 PDF로 인쇄하세요.")
            except:
                pass
            
            raise Exception(f"PDF 생성 실패: {str(e)}")
    
    def generate_png(self, html_content, output_path, width=800, dpi=200):
        """PNG 이미지 생성 - PyMuPDF 사용"""
        try:
            import fitz  # PyMuPDF
            from PIL import Image
            
            # 임시 PDF 생성
            temp_pdf = output_path.replace('.png', '_temp.pdf')
            self.generate_pdf(html_content, temp_pdf)
            
            # PDF를 PyMuPDF로 열기
            doc = fitz.open(temp_pdf)
            
            # 모든 페이지를 PNG로 변환
            images = []
            zoom = dpi / 72.0  # 72 DPI가 기본
            mat = fitz.Matrix(zoom, zoom)
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=mat, alpha=False)
                
                # PIL Image로 변환
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                images.append(img)
            
            doc.close()
            
            # 모든 페이지를 하나의 이미지로 결합
            if len(images) == 1:
                # 단일 페이지
                images[0].save(output_path, 'PNG', quality=95)
            else:
                # 여러 페이지를 세로로 이어붙이기
                total_height = sum(img.height for img in images)
                max_width = max(img.width for img in images)
                
                combined = Image.new('RGB', (max_width, total_height), 'white')
                y_offset = 0
                
                for img in images:
                    combined.paste(img, (0, y_offset))
                    y_offset += img.height
                
                # 너비 조정
                if width and width != max_width:
                    ratio = width / max_width
                    new_height = int(total_height * ratio)
                    combined = combined.resize((width, new_height), Image.Resampling.LANCZOS)
                
                combined.save(output_path, 'PNG', quality=95)
            
            # 임시 파일 삭제
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)
            
            file_size = os.path.getsize(output_path)
            print(f"✅ PNG 생성 성공: {output_path} ({file_size:,} bytes)")
            
            return output_path
            
        except ImportError as e:
            print(f"⚠️  PyMuPDF가 설치되지 않았습니다: {e}")
            return self._generate_png_fallback(html_content, output_path)
        except Exception as e:
            import traceback
            print(f"❌ PNG 생성 오류:")
            traceback.print_exc()
            raise Exception(f"PNG 생성 오류: {str(e)}")
    
    def _generate_png_fallback(self, html_content, output_path):
        """PNG 생성 대체 방법 (pdf2image 없이)"""
        try:
            # PDF로 생성
            temp_pdf = output_path.replace('.png', '_temp.pdf')
            self.generate_pdf(html_content, temp_pdf)
            
            # PDF를 유지하고 PNG는 수동 변환 안내
            return temp_pdf
        except Exception as e:
            raise Exception(f"PNG 생성 오류: {str(e)}")


def generate_report(analysis_data, patient_info, doctor_comment='', 
                   output_format='pdf', output_dir='output', filename=None,
                   include_recommendations=True):
    """
    리포트 생성 헬퍼 함수
    
    Args:
        analysis_data: 분석된 검사 데이터
        patient_info: 환자 정보
        doctor_comment: 의료진 코멘트
        output_format: 출력 형식 ('pdf', 'png', 'html')
        output_dir: 출력 디렉토리
        filename: 파일명 (없으면 자동 생성)
        include_recommendations: 권장사항 포함 여부 (기본값: True)
    
    Returns:
        생성된 파일 경로
    """
    # 템플릿 디렉토리
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    
    # 로고 경로 (simple 버전)
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                            'assets', 'hospital_logo_simple.png')
    
    # 리포트 생성기 초기화
    generator = ReportGenerator(template_dir)
    
    # 데이터 준비
    report_data = {
        'patient_info': patient_info,
        'grouped_tests': analysis_data['grouped_tests'],
        'summary': analysis_data['summary'],
        'recommendations': analysis_data.get('recommendations', []) if include_recommendations else []
    }
    
    # HTML 생성
    html_content = generator.generate_html(report_data, doctor_comment, logo_path)
    
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 파일명 생성
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        patient_name = patient_info.get('name', 'patient')
        filename = f"report_{patient_name}_{timestamp}"
    
    # 확장자 제거
    filename = filename.replace('.pdf', '').replace('.png', '').replace('.html', '')
    
    # 형식에 따라 출력
    if output_format == 'html':
        output_path = os.path.join(output_dir, f"{filename}.html")
        return generator.save_html(html_content, output_path)
    elif output_format == 'pdf':
        output_path = os.path.join(output_dir, f"{filename}.pdf")
        return generator.generate_pdf(html_content, output_path)
    elif output_format == 'png':
        output_path = os.path.join(output_dir, f"{filename}.png")
        return generator.generate_png(html_content, output_path)
    else:
        raise ValueError(f"지원하지 않는 출력 형식: {output_format}")
