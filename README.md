---

# 🚀 Mini NPU Simulator

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-99%25%20Complete-orange.svg)

> **부동소수점 오차를 극복한 고정밀 MAC 연산 및 성능 분석 시뮬레이터**  
> 본 프로젝트는 NPU(Neural Processing Unit)의 핵심 연산인 MAC을 시뮬레이션하고, 데이터 검증 및 하드웨어적 성능 지표를 산출합니다.

---

## 📑 목차
1. [주요 특징](#-주요-특징)
2. [시스템 구조](#-시스템-구조)
3. [핵심 기술 설명](#-핵심-기술-설명)
4. [설치 및 실행 방법](#-설치-및-실행-방법)
5. [리포트 샘플](#-리포트-샘플)

---

## ✨ 주요 특징

- **고정밀 MAC 연산**: `1e-9` 오차 허용 범위를 적용하여 부동소수점 연산의 정확도 확보.
- **동적 스키마 검증**: 정규표현식을 이용해 패턴명에서 $N$값을 추출하고, 행렬 크기를 재귀적으로 검증.
- **성능 프로파일링**: 연산 크기별 실행 시간 측정 및 **MAC Ops** (Operations Per Second) 계산.
- **유연한 데이터 입력**: `JSON` 기반 대량 테스트 및 사용자 `Interactive` 수동 입력 모드 지원.
- **모듈화된 설계**: 연산, 검증, 리포트, 입력 로직을 분리하여 유지보수성 극대화.

---

## 🏗 시스템 구조

```text
.
├── main.py                 # 프로그램 실행 엔트리 포인트
├── data.json               # 테스트용 데이터셋 (5x5, 13x13, 25x25)
├── srcs/
│   ├── core/               # 핵심 비즈니스 로직
│   │   ├── utils_cal.py    # MAC 연산 및 성능 측정 엔진
│   │   ├── utils_input.py  # 데이터 로드 및 사용자 입력 처리
│   │   ├── utils_report.py # 리포트 생성 및 터미널 출력 UI
│   │   └── prompt.py       # 메인 메뉴 루프 및 예외 처리
│   └── specs/              # 명세 및 검증 로직
│       ├── constants.py    # 필터 명칭 및 기호 매핑 테이블
│       ├── data_spec.py    # 데이터 구조 정의 (Schema)
│       ├── regex_utils.py  # N값 추출용 정규식 유틸리티
│       └── validate.py     # 재귀적 데이터 타입/크기 검증기
└── README.md               # 프로젝트 문서
```

---

## 🛠 핵심 기술 설명

### 1. MAC (Multiply-Accumulate) Logic
NPU의 기본 연산 단위를 시뮬레이션합니다.
$$\text{Result} = \sum_{i=0}^{N-1} \sum_{j=0}^{N-1} (\text{Input}_{i,j} \times \text{Filter}_{i,j})$$
*   **오차 판정**: 결과값이 기대값과 다를 경우, `abs(diff) < 1e-9` 조건을 통해 부동소수점 반올림 오차인지 실제 오답인지 판별합니다.

### 2. Recursive Schema Validation
데이터의 무결성을 보장하기 위해 다음과 같은 검증 프로세스를 거칩니다.
1.  **Context Extraction**: 패턴 키(예: `size_5_1`)에서 $N=5$를 추출.
2.  **Recursive Check**: `dict`, `list` 구조를 타고 내려가며 데이터 타입 확인.
3.  **Size Constraint**: 추출된 $N$을 전파하여 모든 행렬이 $N \times N$인지 확인.

### 3. Performance Analysis
하드웨어 성능 측정을 위해 1,000회 반복 연산을 수행합니다.
*   **Average Time**: 연산에 소요된 평균 시간(ms) 측정.
*   **Sorting**: 리포트 출력 시 $N$ 크기순으로 정렬하여 데이터 스케일에 따른 성능 추이 가시화.

---

## 🏃 설치 및 실행 방법

### 요구 사항
*   Python 3.8 이상

### 실행
```bash
# 저장소 클론
git clone https://github.com/your-repo/mini-npu-sim.git

# 디렉토리 이동
cd mini-npu-sim

# 시뮬레이터 실행
python main.py
```

---

## 📊 리포트 샘플

프로그램 실행 시 다음과 같은 분석 결과가 제공됩니다.

### ✅ Case Analysis
| Pattern Name | Status | Result | Expected | Match |
|:---|:---:|:---:|:---:|:---:|
| size_5_1 | PASS | 125.0 | 125.0 | Filter A |
| size_13_1 | FAIL | 412.5 | 500.0 | UNDECIDED |

### 🚀 Performance Table
| Matrix Size (N) | Avg Time (ms) | MAC Ops (per sec) |
|:---:|:---:|:---:|
| 5 x 5 | 0.0012 | 20,833,333 |
| 13 x 13 | 0.0085 | 19,882,352 |
| 25 x 25 | 0.0310 | 20,161,290 |

---g