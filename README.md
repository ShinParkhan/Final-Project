# :notebook_with_decorative_cover: README

## :busts_in_silhouette: 팀원

| 이름         | 팀원 정보   | 역할      | 업무 분담           |
| ------------ | ----------- | --------- | ------------------- |
| 신승호       | 영문학 전공 | front-end | db 구축 / templates |
| 박홍은(팀장) | 통계학 전공 | back-end  | db 구축 / 기능구현  |



## :film_projector: 진행상황

### 11/22

- Movie, Genre, Rating 모델링

### 11/23

- Actor 모델링

### 11/24

- Actor 모델링 마무리
- 소셜 로그인(카카오, 구글)
- Youtube 예고편 삽입
- templates 틀 만들기

### 11/25

- 비동기 처리(like, follow)
- 추천 알고리즘 구현
- 좋아요한 배우 리스트 기능 구현
- 좋아요한 영화 리스트 기능 구현

### 11/26

- 인덱스 호버 카드 덱(완성)
- 장르 호버 카드 덱 with scroll
- 추천 알고리즘(로그인/좋아요 여부로) 분기
- 관리자 : 리뷰 삭제 / 영화 등록, 수정 및 삭제
- 관리자 template : 유저 삭제
- 유저 디테일 페이지

### 11/27

- 리뷰 수정 기능 구현
- like_actor_list.html
- like_movie_list.html
- genre_movie_list.html
- adminpage.html
- userdetail.html

### 11/28

- index.html
- detail.html
- intro.html
- font 설정

## :full_moon: 모델링(ERD)

![bonomovie](C:\Users\park\Downloads\bonomovie.png)

## :star: 핵심 기능

### "좋아요"한 영화 기반 추천 알고리즘

- 좋아요 한 영화를 기반으로 해당 영화 장르들 중 하나를 랜덤으로 가져와 그 장르의 영화들을 랜덤으로 5개 보여준다.

## 배포 서버 URL

http://bonomovie.mtpppimcwz.ap-northeast-2.elasticbeanstalk.com/movies/

## 느낀점

- css 가 생각대로 되지 않아 "CSS is awesome" 을 다시 한 번 느꼈다.
- API를 이용해 원하는 데이터를 가져와 처리하는 작업이 가장 중요하다는 것을 알게 되었다.
- JS 공부가 많이 부족했다