import os
import json

def process_all_images(json_dir, image_dir, output_dir):
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

    os.makedirs(output_dir, exist_ok=True)  # 출력 폴더 생성

    for json_file in json_files:
        json_path = os.path.join(json_dir, json_file)
        image_file = os.path.join(image_dir, os.path.splitext(json_file)[0] + '.jpg')  # 이미지 파일 경로 생성

        convert_to_yolo_format(json_path, image_file, output_dir)

def convert_to_yolo_format(json_path, image_path, output_dir):
    with open(json_path, 'r') as f:
        data = json.load(f)

    # JSON 데이터 구조 확인
    if 'Annotation' not in data:
        print(f"Error: 'Annotation' field not found in {json_path}")
        return

    annotations = data['Annotation']

    yolo_labels = []

    for ann in annotations:
        class_name = ann['class_name']
        bbox = ann['data']

        # 클래스 이름에 대한 클래스 ID 매핑
        class_id = class_name_to_id.get(class_name)
        if class_id is None:
            continue

        # 경계 상자 좌표
        xmin, ymin, xmax, ymax = bbox
        x_center = (xmin + xmax) / 2 / data['image_size'][0]  # 이미지 너비로 나누기
        y_center = (ymin + ymax) / 2 / data['image_size'][1]  # 이미지 높이로 나누기
        width = (xmax - xmin) / data['image_size'][0]  # 이미지 너비로 나누기
        height = (ymax - ymin) / data['image_size'][1]  # 이미지 높이로 나누기

        # YOLO 형식의 라벨 생성
        yolo_label = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
        yolo_labels.append(yolo_label)

    # YOLO 라벨 파일 쓰기
    label_file_name = os.path.basename(image_path).replace('.jpg', '.txt')
    label_file_path = os.path.join(output_dir, label_file_name)
    print(f"Saving labels to {label_file_path}")  # 파일 경로 출력
    try:
        with open(label_file_path, 'w') as label_file:
            label_file.write("\n".join(yolo_labels))
        print(f"Labels saved successfully for {os.path.basename(image_path)}")
    except Exception as e:
        print(f"Error saving labels for {os.path.basename(image_path)}: {e}")

# 클래스 이름을 클래스 ID로 매핑하는 딕셔너리
class_name_to_id = {
    "car": 0,
    "bus": 1,
    "truck": 2,
    "special vehicle": 3,
    "motorcycle": 4,
    "bicycle": 5,
    "personal mobility": 6,
    "person": 7,
    "Traffic_light": 8,
    "Traffic_sign": 9
}

# 입력 및 출력 디렉토리 설정
json_dir = "/home/gpuadmin/2022811007/project/dataset/auto_dataset/val/labels"
image_dir = "/home/gpuadmin/2022811007/project/dataset/auto_dataset/val/images"
output_dir = "/home/gpuadmin/2022811007/project/dataset/auto_dataset/val/labels_output"  # 모든 라벨을 저장할 폴더

# 전체 이미지 및 JSON 파일 처리
process_all_images(json_dir, image_dir, output_dir)