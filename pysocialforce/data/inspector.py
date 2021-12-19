from .parameters import DataIndex as Index
# json파일 형식 체크하는 함수

## start_time이랑 visible 변수 체크
def check_visible(json_data):    
    check = True
    for data in json_data.values():
        start_time = data.get(Index.start_time.name)
        visible = data.get(Index.visible.name)
        if start_time is 0 and visible is not 1:            
            check = False
            break        
        if start_time is not 0 and visible is not 0:
            check = False
            break
    return check

## 겹치는 id가 있는지 체크
def check_id(json_data):
    key_data = [key for key in json_data.keys()]
    id_data = [value.get(Index.id.name) for value in json_data.values()]
    return len(json_data) == len(key_data) and len(json_data) == len(id_data)
    
        

