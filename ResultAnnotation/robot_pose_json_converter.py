import json
import os
import shutil

# 설정: 폴더 경로와 파일 목록 설정
input_folder_path = './saved'  # 입력 파일들이 위치한 폴더 (현재 실행 위치의 하위 폴더)
output_folder_path = './out'  # 출력 파일을 저장할 폴더 (현재 실행 위치의 하위 폴더)

# output 폴더가 없다면 생성
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

files = os.listdir(input_folder_path)
json_files = [f for f in files if f.endswith('.json')]
image_files = [f for f in files if f.endswith('.jpg') or f.endswith('.png')]

# 조인트 이름 매핑
joint_name_mapping = {
    "nose": "Nose",
    "neck_01": "Neck",
    "upperarm_r": "RShoulder",
    "lowerarm_r": "RElbow",
    "hand_r": "RWrist",
    "upperarm_l": "LShoulder",
    "lowerarm_l": "LElbow",
    "hand_l": "LWrist",
    "thigh_r": "RHip",
    "calf_r": "RKnee",
    "foot_r": "RAnkle",
    "thigh_l": "LHip",
    "calf_l": "LKnee",
    "foot_l": "LAnkle"
}

# out.json 구조 초기화
output_data = {
    "annotations": [],
    "joint_names": ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist", "RHip", "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle"],
    "joint_parents": [1, -1, 1, 2, 3, 1, 5, 6, 1, 8, 9, 1, 11, 12],
    "num_images": len(json_files),
    "num_joints": 14
}

# 각 JSON 파일 처리
for json_file in json_files:
    file_path = os.path.join(input_folder_path, json_file)
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # 이미지 파일명 생성 및 복사
    image_number = json_file.split('.')[0]
    image_filename = f"{image_number}.jpg"  # JSON 파일과 동일한 번호의 이미지 파일
    image_source_path = os.path.join(input_folder_path, image_filename)
    image_dest_path = os.path.join(output_folder_path, image_filename)
    shutil.copy(image_source_path, image_dest_path)

    # 조인트 데이터 추출 및 매핑
    joints = data["jointStruct"]
    key_points = []
    for joint in joints:
        joint_name = joint["jointName"]
        if joint_name in joint_name_mapping:
            idx = output_data["joint_names"].index(joint_name_mapping[joint_name])
            x, y = joint["x"], joint["y"]
            key_points.append([x, y, 1.0])  # 조인트 좌표를 한 줄에 씀

    # key_points 정렬 (output_data["joint_names"] 순서에 맞게 정렬)
    sorted_key_points = [None] * 14
    for joint in joints:
        joint_name = joint["jointName"]
        if joint_name in joint_name_mapping:
            idx = output_data["joint_names"].index(joint_name_mapping[joint_name])
            x, y = joint["x"], joint["y"]
            sorted_key_points[idx] = [x, y, 1.0]  # 조인트 좌표를 한 줄에 씀

    # annotations에 추가
    output_data["annotations"].append({
        "img": image_filename,
        "key": sorted_key_points
    })

# JSON 파일로 결과 출력
out_file_path = os.path.join(output_folder_path, 'out.json')
with open(out_file_path, 'w') as out_file:
    json.dump(output_data, out_file, indent=3)

print(f"Created 'out.json' with {len(json_files)} annotations in the 'out' folder.")
