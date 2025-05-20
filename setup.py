import nltk
import os

def setup_environment():
    print("Starting environment setup...")
    
    # NLTK 데이터 다운로드
    print("Downloading NLTK data...")
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    
    # 필요한 디렉토리 생성
    directories = [
        'data/papers',
        'data/news',
        'data/patents',
        'data/investments',
        'data/analysis',
        'outputs/figures',
        'outputs/reports'
    ]
    
    print("Creating necessary directories...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory already exists: {directory}")

    print("Environment setup completed!")

if __name__ == "__main__":
    setup_environment()
