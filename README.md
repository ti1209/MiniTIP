# MiniTIP Project

### 1. DB Modeling  
![](https://github.com/ti1209/MiniTIP/blob/master/db_relation.PNG)
  
### 2. 각 모델의 models.py 정의
  
### 3. 데이터 동기화  
2. 에서 정의한 대로 DB 생성 후, 각 모델 안에 sync.py를 생성하여 각 모델별로 데이터 동기화  
최상단 위치에서는 각 모델 안에 있는 sync.py를 호출하여 한번에 동기화가 진행되도록 함

### 4. 대시보드에서 각 portlet에 들어가는 데이터들을 ORM으로 정의(Dashboard > views.py)

### 5. Bootstrap을 이용하여 UI / UX Design (html, css, jquery)

### 6. template tag를 이용하여 DB 데이터 나타내기
  
### 7. jquery를 사용하여 Datatable 및 그래프들 나타내기
  
### 8. Django REST API를 사용하기 위해 portlet 별 Serializer 생성(device > serializers.py)
  
### 9. viewsets.py에 기존에 views.py에서 개발했던 내용들 모두 옮기기

### 10. 제대로 생성되었는지 확인  
![](https://github.com/ti1209/MiniTIP/blob/master/rest_api.PNG)  
  
### Result
#### Device Dashboard  
![](https://github.com/ti1209/MiniTIP/blob/master/device.PNG)
  
#### Globallist Dashboard  
![](https://github.com/ti1209/MiniTIP/blob/master/globalist.PNG)
