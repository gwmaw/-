#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 줄바꿈 테스트
comment = """정기 검진 결과 일부 항목에서 주의가 필요합니다.
생활습관 개선과 함께 3개월 후 재검사를 권장합니다.

추가 관찰이 필요한 항목:
- 당화혈색소(HbA1c)
- HDL 콜레스테롤"""

print("=== 원본 텍스트 ===")
print(repr(comment))
print("\n=== 출력 텍스트 ===")
print(comment)

# 엑셀 파일로 리포트 생성 테스트
from excel_parser import parse_excel_file
from report_analyzer import analyze_test_results
from report_generator import generate_report

excel_file = '/home/user/uploaded_files/전성우_검체검사결과_20260123.xlsx'

print("\n=== 리포트 생성 테스트 ===")
tests = parse_excel_file(excel_file)
print(f"검사 항목: {len(tests)}개")

analysis = analyze_test_results(tests)
print(f"정상: {analysis['summary']['normal']}개, 주의: {analysis['summary']['abnormal']}개")

patient_info = tests[0].get('patient_info', {}) if tests else {}

output_file = generate_report(
    analysis_data=analysis,
    patient_info=patient_info,
    doctor_comment=comment,
    output_format='pdf',
    output_dir='output'
)

print(f"\nPDF 생성: {output_file}")
import os
print(f"파일 크기: {os.path.getsize(output_file) / 1024:.1f} KB")
