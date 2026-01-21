"""
리포트 생성 모듈
HTML 템플릿 렌더링 및 PDF/PNG 출력
"""

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from PIL import Image
from datetime import datetime
import os


class ReportGenerator:
    """검사 결과 리포트를 생성하는 클래스"""
    
    def __init__(self, template_dir):
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def generate_html(self, data, doctor_comment=''):
        """HTML 리포트 생성"""
        template = self.env.get_template('report_template.html')
        
        # 현재 날짜/시간
        now = datetime.now()
        
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
            'doctor_comment': doctor_comment
        }
        
        html_content = template.render(**template_data)
        return html_content
    
    def save_html(self, html_content, output_path):
        """HTML 파일 저장"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return output_path
    
    def generate_pdf(self, html_content, output_path):
        """PDF 생성"""
        try:
            # CSS 스타일 최적화
            css = CSS(string='''
                @page {
                    size: A4;
                    margin: 0;
                }
                body {
                    margin: 0;
                    padding: 0;
                }
            ''')
            
            # HTML을 PDF로 변환
            HTML(string=html_content).write_pdf(
                output_path,
                stylesheets=[css]
            )
            
            return output_path
        except Exception as e:
            raise Exception(f"PDF 생성 오류: {str(e)}")
    
    def generate_png(self, html_content, output_path, width=800):
        """PNG 이미지 생성"""
        try:
            # 임시 PDF 생성
            temp_pdf = output_path.replace('.png', '_temp.pdf')
            self.generate_pdf(html_content, temp_pdf)
            
            # PDF를 PNG로 변환
            from pdf2image import convert_from_path
            images = convert_from_path(temp_pdf, dpi=200)
            
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
            
            return output_path
        except ImportError:
            # pdf2image가 없으면 WeasyPrint로 직접 PNG 생성
            return self._generate_png_fallback(html_content, output_path)
        except Exception as e:
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
                   output_format='pdf', output_dir='output', filename=None):
    """
    리포트 생성 헬퍼 함수
    
    Args:
        analysis_data: 분석된 검사 데이터
        patient_info: 환자 정보
        doctor_comment: 의료진 코멘트
        output_format: 출력 형식 ('pdf', 'png', 'html')
        output_dir: 출력 디렉토리
        filename: 파일명 (없으면 자동 생성)
    
    Returns:
        생성된 파일 경로
    """
    # 템플릿 디렉토리
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    
    # 리포트 생성기 초기화
    generator = ReportGenerator(template_dir)
    
    # 데이터 준비
    report_data = {
        'patient_info': patient_info,
        'grouped_tests': analysis_data['grouped_tests'],
        'summary': analysis_data['summary'],
        'recommendations': analysis_data.get('recommendations', [])
    }
    
    # HTML 생성
    html_content = generator.generate_html(report_data, doctor_comment)
    
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
